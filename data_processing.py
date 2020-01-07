import pandas as pd
from numpy import array, asarray, vstack, transpose
import matplotlib
from matplotlib import dates
import matplotlib.pyplot as plt
from image_diff import image_difference
from datetime import datetime


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

def timewindowing(df,window_unit,window_size):
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



# --------------------------------------------------------

# E
data_df = pd.read_csv('data.csv')
data_df = reformatting(data_df)
datetime_list = data_df['Datetime']
noise_level_list = data_df['Noise Level']
noise_thres_list = data_df['Noise Threshold']
datetime_list_date = data_df['Datetime Date']
datetime_list_time = data_df['Datetime Time']

# plt.plot(datetime_list, noise_level_list)
# plt.gcf().autofmt_xdate()
# plt.show()
#
# plt.plot(datetime_list_time,)
# plt.gcf().autofmt_xdate()
# plt.show()

# ----------------------
# Grouping function
window_unit = 'H' # Days, hours, minutes ect
window_size = 1 # Number of each per group
group_list = timewindowing(data_df, window_unit, window_size)
data_df["Grouping"] = group_list

# -----------------------------------------------
# Adding up total number of entries in each groups
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

#print(data_df.head())
# conversion to datetime object
#datetime_object_list = [datetime.strptime(str(datetime_list[i]), '%H %M %S') for i in range(len(datetime_list))]
#dates_converted = matplotlib.dates.date2num(datetime_object_list)
#print(dates_converted)

# ----------------------------------------
# Plot time vs number of vehicles passing
#arr1 = array(range(23))
arr1 = array(range(len(sum_val_list)))
arr2 = asarray(sum_val_list)

print(arr1)
print(arr2)

array = vstack((arr1, arr2))
array = transpose(array)
print(array)

plt.plot(arr1, arr2)
plt.gcf().autofmt_xdate()
plt.show()
