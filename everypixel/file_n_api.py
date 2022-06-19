import requests
import os
from os.path import exists
import shutil
from PIL import Image

CLIENT_ID = 'YiTfUni6Kyo6S7C4KrPWI7Qg'
CLIENT_SECRET = 'Y7Z4qQCXR8fki4rM1OeNZhzABb3B0T4F3hwZsbZIhfcgfnS8'
params = {'num_keywords': 10}
keywords = requests.get('https://api.everypixel.com/v1/keywords', params=params, auth=(CLIENT_ID, CLIENT_SECRET)).json()
kw_arr = []

def readFiles(file):
    global keywords
    for filename in os.listdir('imgcutter-temp'):
        f = os.path.join('imgcutter-temp', filename)
        with open(f, 'rb') as image:
            data = {'data': image}
            keywords = requests.post('https://api.everypixel.com/v1/keywords', files=data, auth=(CLIENT_ID, CLIENT_SECRET)).json()
            if keywords['status'] == "error":
                print(keywords['message'])
            else:
                kw_arr.append(keywords)
    shutil.rmtree('imgcutter-temp')

def cutter(file):
    img = Image.open(file)
    width, height = img.size
    wd = width/4
    hd = height/4

    temp = os.mkdir('imgcutter-temp')
    file_exists = exists('imgcutter-temp')

    count = 0
    if file_exists == True:
        for i in range(4):
            for j in range(4):
                imo = img.crop((wd*j, hd*i, wd*(j+1), hd*(i+1)))
                imo.save('imgcutter-temp/' + str(count) + '.png')
                count += 1
    
    readFiles(file)
