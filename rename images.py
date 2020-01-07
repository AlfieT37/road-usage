import os

def image_rename():
    path = 'C:\\Users\\Alfie\\OneDrive - Imperial College London\\DE4\\Internet of things\\Project files\\Images'
    # path1 = '%s' % path + '\img1.jpg'

    for filename in os.listdir(path):
        src = '%s' % path + '\\%s' % filename  # Source file
        dst = '%s' % path + '\\%s' % filename
        print(len(filename))
        if len(filename) == 30:
            dst = dst[:-11] + '.jpg'
        dst = path + dst
        print(dst)
        #os.rename(src, dst)
    return


image_rename()
