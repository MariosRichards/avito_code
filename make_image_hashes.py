

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 
import datetime
from datetime import datetime
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
start = datetime.now()
print(start)
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

#from subprocess import check_output
import os
print(os.listdir("../avito_data"))
#print(check_output(["ls", "../avito_data"]).decode("utf8"))

# Any results you write to the current directory are saved as output.

# Using the code from http://blog.iconfinder.com/detecting-duplicate-images-using-python/

import zipfile
import os
import io
from PIL import Image
#os.chdir('/home/run2/avito')
os.chdir('../avito_data')
#import pandas as pd

def dhash(image,hash_size = 16):
    image = image.convert('LA').resize((hash_size+1, hash_size), Image.ANTIALIAS)
    mat = np.array(
        list(map(lambda x: x[0], image.getdata()))
    ).reshape(hash_size, hash_size+1)
    
    return ''.join(
        map(
            lambda x: hex(x)[2:].rjust(2,'0'),
            np.packbits(np.fliplr(np.diff(mat) < 0))
        )
    )
    
dataset_size = 0
zip_list = [0,1,2,3,4,5,6,7,8,9]
test_length = 100000

current = datetime.now()

for zip_counter in zip_list:
    imgzipfile = zipfile.ZipFile('Images_'+str(zip_counter)+'.zip')
    print ('Doing zip file ' + str(zip_counter))
    
    print(current,datetime.now()-current)
    current = datetime.now()
    namelist = imgzipfile.namelist()
    # Comment this line below and uncomment the above line when you do for the whole set
    dataset_size += len(imgzipfile.namelist())
    # namelist = imgzipfile.namelist()[:test_length]
    print ('Total elements ' + str(len(namelist)))

    img_id_hash = []
    counter = 1
    for name in namelist:
        #print name
        try:
            imgdata = imgzipfile.read(name)
            if len(imgdata) >0:
                img_id = name[:-4]
                stream = io.BytesIO(imgdata)
                img = Image.open(stream)
                img_hash = dhash(img)
                img_id_hash.append([img_id,img_hash])
                counter+=1
            # Uncomment the lines below to get an idea of progress when you do for the whole set
            #if counter%10000==0:
            #    print 'Done ' + str(counter) , datetime.datetime.now()
        except:
            print ('Could not read ' + str(name) + ' in zip file ' + str(zip_counter))
    df = pd.DataFrame(img_id_hash,columns=['image_id','image_hash'])
    df.to_csv('image_hash_' + str(zip_counter) + '.csv')

# to get the average dataset_size, divide through by number of zips
average_dataset_size = dataset_size / len(zip_list)
    
finish = datetime.now()
duration = finish - start
print(finish)
print( duration, average_dataset_size, test_length )
print( duration * average_dataset_size / test_length )