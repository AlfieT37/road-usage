# USAGE
# python image_diff.py --first images/original_01.png --second images/modified_01.png

# import the necessary packages
from skimage.measure import compare_ssim
import imutils
import cv2

# Delete later
from data_processing import reformatting
from numpy import array, asarray, vstack, transpose


# --------------------------------------------------
# def image_difference(filename1, filename2):
def image_difference(filename1, path2):
	# Processes 2 input pictures and outputs the vehicle type
	path1 = r'C:\Users\Alfie\OneDrive - Imperial College London\DE4\Internet of things\Project files\Images\%s.jpg' %filename1
	#path2 = r'C:\Users\Alfie\OneDrive - Imperial College London\DE4\Internet of things\Project files\Images\%s.jpg' %filename2
	imageA = cv2.imread(path1)
	imageB = cv2.imread(path2)

	# ----------------------------------------
	# Resize
	# Reduces resolution of images to remove false positive changes

	scale_percent = 50 # percent of original size
	width = int(imageA.shape[1] * scale_percent / 100)
	height = int(imageA.shape[0] * scale_percent / 100)
	dim = (width, height)
	# resize image
	imageA = cv2.resize(imageA, dim, interpolation = cv2.INTER_AREA)
	imageB = cv2.resize(imageB, dim, interpolation = cv2.INTER_AREA)

	# --------------------------------------
	# Detect differences
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
	cv2.imshow("Modified", imageB)
	# cv2.imshow("Diff", diff)
	# cv2.imshow("Thresh", thresh)
	cv2.waitKey(0)
	# arr1 = asarray(rect_list_pos)
	# arr2 = asarray(rect_list_size)
	# rect_list = vstack((arr1, arr2))
	# rect_list = transpose(rect_list)

	# ---------------------
	# Works out vehicle type from rectangle size
	vehicle_list = []
	if len(rect_list_size) <= 5:
		for i in range(len(rect_list_size)):
			rect_size = rect_list_size[i]
			print('rect_size full', rect_size)
			print('rect_size', rect_size[1])
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
		# Run reset
	return vehicle_list
# ----------------------------
# Testing

#def reset_base_image():


# for i in range(28):
# 	a = 'img1'
# 	b = 'img%i' %(i+2)
# 	vehicles = image_difference(a, b)
# 	print(vehicles)


# ---------------------------
# Testing 2
data_df = pd.read_csv('data.csv')
df = reformatting(data_df)
datetime_list = data_df['Datetime']
datetime_date_list = data_df.loc[:, "Datetime Date"]
datetime_time_list = data_df.loc[:, "Datetime Time"]

vehicle_list_full = []

for i in range(len(datetime_list)):
	#filename = '2019-12-30 18_20_21.131027'
	datetime_date = str(datetime_date_list[i])
	year = datetime_date[6:9]
	print(year)
	#filename = ''

	#image_difference(a,b)

	#vehicle_list_full.append(vehicle_list)
