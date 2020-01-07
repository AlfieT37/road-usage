import pandas as pd
from numpy import array, asarray, vstack, transpose, zeros, float, uint8
import numpy as np
import matplotlib
from matplotlib import dates
import matplotlib.pyplot as plt
from datetime import datetime
from skimage import img_as_float64
from glob import glob
from PIL import Image
import time
from tqdm import tqdm
import warnings


from skimage.measure import compare_ssim
import imutils

import os

import cv2  # Need to install


warnings.filterwarnings("ignore")

def image_difference(path1, path2):
    # Processes 2 input pictures and outputs the vehicle type

    # -- Uses OpenCV to open images at each file path --
    imageA = cv2.imread(path1)
    imageB = cv2.imread(path2)

    # -- Resize --
    # Reduces resolution of images to remove false positive changes
    scale_percent = 50  # percent of original size
    width = int(imageA.shape[1] * scale_percent / 100)
    height = int(imageA.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    imageA = cv2.resize(imageA, dim, interpolation=cv2.INTER_AREA)
    imageB = cv2.resize(imageB, dim, interpolation=cv2.INTER_AREA)

    # -- Detect differences --

    # convert the images to gray-scale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the conto67urs
    rect_list_size = []
    rect_list_pos = []

    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        if w > 10:
            cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
            rect_size = (w, h)
            rect_pos = y
            rect_list_size.append(rect_size)
            rect_list_pos.append(rect_pos)

        else:
            continue
    # show the output images
    # cv2.imshow("Original", imageA) # need to uncomment other line
    #cv2.imshow("Modified", imageB)
    # cv2.imshow("Diff", diff)
    # cv2.imshow("Thresh", thresh)
    #cv2.waitKey(0)

    # -- Vehicle recognition --
    # Works out vehicle type from rectangle size
    vehicle_list = []
    if len(rect_list_size) <= 5:
        for i in range(len(rect_list_size)):
            rect_size = rect_list_size[i]
            # print('rect_size full', rect_size)
            # print('rect_size', rect_size[1])
            if 10 < rect_size[1] <= 50:
                vehicle = 'pedestrian'
            elif rect_size[1] > 50:
                vehicle = 'car'
            else:
                vehicle = 'uncertain'
            vehicle_list.append(vehicle)
    else:
        vehicle = 'detection error'
        vehicle_list.append(vehicle)

    return vehicle_list


def reformatting(df):
    #df = pd.read_csv('data.csv')
    df2 = df.dropna(axis=0, how='any', thresh=1)
    weather = df2.loc[:, "Weather"]
    noise_thres = df2.loc[:, "Noise Threshold"]

    my_list = []
    for i in range(len(weather)):
        x = weather[i]
        x = x[1:-1]
        x = x.split(',')
        y = x[0]
        my_list.append(y)

    df2["Weather Type"] = my_list

    my_list = []
    for i in range(len(df2.loc[:, "Weather"])):
        x = weather[i]
        x = x[1:-1]
        x = x.split(',')
        y = x[1]
        my_list.append(y)

    df2["Weather Code"] = my_list

    my_list = []
    for i in range(len(df2.loc[:, "Weather"])):
        x = weather[i]
        x = x[1:-1]
        x = x.split(',')
        y = x[2]
        my_list.append(y)

    df2["Temperature"] = my_list

    my_list = []
    for i in range(len(df2.loc[:, "Weather"])):
        x = weather[i]
        x = x[1:-1]
        x = x.split(',')
        y = x[3]
        my_list.append(y)

    df2["Humidity"] = my_list

    my_list = []
    for i in range(len(df2.loc[:, "Weather"])):
        x = noise_thres[i]
        x = x[1:-1]
        my_list.append(x)

    df2["Noise Threshold"] = my_list

    return df2


# ----------------------------------
# Time windowing
# Groups data by given periods of time
# Used for plotting

def time_windowing(df, window_unit, window_size):
    datetime_list = df.loc[:, "Datetime"]
    date_list = df.loc[:, "Datetime Date"]
    time_list = df.loc[:, "Datetime Time"]

    date_list_focus = []
    time_list_focus = []

    # grouping function
    def grouping(data_list,datetime_list, max_value, min_value):
        group_list = []  # will fill with grouping numbers - 0, 1, 2
        comp_val = int(data_list[0])  # group 1 starts with the first value
        for j in range(max_value):  # Group number - 31 is max possible groups
            for i in range(len(datetime_list)):  # Loops though every value in the list
                val = int(data_list[i])  #
                if val == comp_val:
                    group_list.append(j)  # Append the group number to list
                else:
                    continue
            if comp_val >= max_value:
                comp_val = min_value  # resets value
            else:
                comp_val = comp_val + 1
        return group_list

    if window_unit == 'D':
        for i in range(len(date_list)):
            x = date_list[i]
            x = x[0] + x[1]
            date_list_focus.append(x)
        group_list = grouping(date_list_focus, datetime_list, 31, 1)

    elif window_unit == 'H':
        for i in range(len(time_list)):
            x = time_list[i]
            x = x[0] + x[1]
            time_list_focus.append(x)
        group_list = grouping(time_list_focus, datetime_list, 23, 0)

    else:  # Just default to day
        print('Assuming default window unit - Day')
        for i in range(len(date_list)):
            x = date_list[i]
            x = x[0] + x[1]
            date_list_focus.append(x)
        group_list = grouping(date_list_focus, datetime_list, 31, 1)

    #f["Group"] = group_list
    return group_list


# ---------------------------------------------------------
# Adding up total number of entries in each groups
def tot_num_groups(group_list):
    total_groups = group_list[-1]  # Max number of groups
    sum_val_list = []  # List containing total number of elements for each group

    for j in range(total_groups):
        sum_val = 0
        for i in range(len(group_list)):
            if group_list[i] == j:
                sum_val += 1
            else:
                continue
        sum_val_list.append(sum_val)

    return sum_val_list


# ----------------------------------------------------
# Image averaging

def averaging(path, a, filename, pic_num, imlist):
    # Access all PNG files in directory
    imlist_analysis = []
    a = a - 3 # safety margin
    count = 0
    for i in range(pic_num):
        # for however many pics taken in the hour
        imlist_analysis.append(imlist[a-i])

    # Assuming all images are the same size, get dimensions of first image
    w, h = Image.open(imlist_analysis[0]).size

    # Create a numpy array of floats to store the average (assume RGB images)
    arr = zeros((h, w, 3), float)
    n = len(imlist_analysis)

    # Build up average pixel intensities, casting each image as an array of floats
    for i in range(len(imlist_analysis)):
        count += 1
        #im = imlist_analysis[i]
        imarr = array(Image.open(imlist_analysis[i]), dtype=np.float)
        arr = arr + imarr/n# Mean average across analysis

    arr = array(np.round(arr), dtype= np.uint8)
    # Generate, save and preview final image
    out = Image.fromarray(arr, mode="RGB")
    #out = Image.open(imlist_analysis[0])
    out.save('%s' % path + '\\%s_Average.jpg' % filename)
    out_name = '%s' % path + '\\%s_Average.jpg' % filename
    return out_name

# -------------------------------------------------------------------------------------
# Running

# ---------------------------------------
# init
data_df = pd.read_csv('data.csv')
data_df = reformatting(data_df)

datetime_list = data_df['Datetime']
noise_level_list = data_df['Noise Level']
noise_thres_list = data_df['Noise Threshold']
datetime_list_date = data_df['Datetime Date']
datetime_list_time = data_df['Datetime Time']

# ----------------------
# Grouping function
window_unit = 'H' # Days, hours, minutes ect
window_size = 1 # Number of each per group
group_list = time_windowing(data_df, window_unit, window_size)
#data_df["Grouping"] = group_list

# ----------------------------------------
# Plot time vs number of vehicles passing

sum_val_list = tot_num_groups(group_list)
arr1 = array(range(len(sum_val_list)))
arr2 = asarray(sum_val_list)

arr_group = vstack((arr1, arr2))
arr_group = transpose(arr_group)

#print(arr)

# Plotting
plt.plot(arr1, arr2)
plt.gcf().autofmt_xdate()
plt.xlabel('')
plt.ylabel('')
#plt.show()

# ---------------------------
# Testing 2

path = 'C:\\Users\\Alfie\\OneDrive - Imperial College London\\DE4\\Internet of things\\Project files\\Images'
path1 = '%s' % path + '\\img1.jpg'

# -- Image average init --
allfiles = os.listdir(path)
imlist = [filename for filename in allfiles if filename[-4:] in [".jpg", ".JPG"]]  # List all files ending in .jpg
imlist2 = []  # init image list 2
for i in range(len(imlist)):
    imlist[i] = '%s' % path + '\\%s' % imlist[i]
    imlist2.append(imlist[i])

# -- Initialise empty lists --
vehicle_list_full = []
path_list = []
pic_num = 0

# -- Main Loop --
for i in tqdm(range(1, len(datetime_list))):  # Loop through all date times from the csv, tqdm is progress
    datetime_date = str(datetime_list_date[i])
    datetime_time = str(datetime_list_time[i])
    datetime_time_1 = str(datetime_list_time[i-1])

    # Splits weather report into other columns
    year = datetime_date[6:10]
    month = datetime_date[3:5]
    day = datetime_date[0:2]
    hour = datetime_time[0:2]
    hour_1 = datetime_time_1[0:2]
    minute = datetime_time[3:5]
    sec = datetime_time[6:8]

    # -- Changing filename to the formatting of pictures --
    # '2019-12-30 18_20_21.131027'
    filename = '%s' % year + '-%s' % month + '-%s ' % day + '%s_' % hour + '%s_' % minute + '%s' % sec

    # -- Changes path1 to an average image across an hour --
    if hour_1 == str(int(hour)-1):  # If the hour has changed update reference image
        path1 = averaging(path, i, filename, pic_num, imlist2)
        pic_num = 0  # counter is reset
    else:
        pic_num += 1 # Only updates the counter if the pic exists

    # -- Update the photo that the average photo is compared to --
    path2 = glob('%s' % path + '\\%s*.jpg' % filename)

    # -- Exec vehicle detection --
    # Tries to detect vehicles but if there is no matching image, the csv is marked
    try:
        vehicle_list = image_difference(path1, path2[0])
        vehicle_list_full.append(vehicle_list)
    except IndexError:
        vehicle_list = float('NaN')
        vehicle_list_full.append(vehicle_list)
        continue

 # -- Export CSV from the data_frame --
vehicle_list_full = ['NA'] + vehicle_list_full
data_df["Vehicle Type"] = vehicle_list_full
print('Exporting!')
data_df.to_csv(r'C:\Users\Alfie\PycharmProjects\Siot\Data_export.csv')
data_df2 = data_df.dropna(axis=0, how='any')
data_df2.to_csv(r'C:\Users\Alfie\PycharmProjects\Siot\Data_export2.csv')
print('Complete!')
plt.show()