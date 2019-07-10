#coding=utf-8
import os
from PIL import Image
from PIL import ImageGrab
import pytesseract
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import re


DEFAULT_WIDTH = 768
DEFAULT_HEIGHT = 1366


def main():
    # 768*1366分辨率坐标
    left = 25
    top = 200
    right = 1000
    bottom = 1300
    # 1.安卓截图
    os.system('adb shell screencap -p /sdcard/answer.png')
    os.system('adb pull /sdcard/answer.png answer.png')


    # 2. 截取题目并文字识别
    image = Image.open('answer.png')
    crop_img = image.crop((left,top,right,bottom))
    crop_img.save('crop.png')
    text = pytesseract.image_to_string(crop_img, lang='chi_sim')#text为从图片中提取出来的题目和答案


    # 3. 去百度知道搜索
    breakpos = text.index('?')
    nextque = text[breakpos+1:]
    question = text[3:breakpos]  # 获得题目并去掉题号
    '''
    #获取三个答案选项
    ans = nextque.split('\n\n')
    ans1 = ans[1]
    ans2 = ans[2]
    ans3 = ans[3]
    '''
    print(question+'\n')#题目
    #print(ans1,ans2,ans3)#3个答案
    
    wd = urllib.request.quote(question)
    #url = 'https://www.baidu.com/s?wd={}'.format(wd)
    url = 'https://zhidao.baidu.com/search?ct=17&pn=0&tn=ikaslist&rn=10&fr=wwwt&word={}'.format(wd)
    #print(url)
    result = urlopen(url)
    body = BeautifulSoup(result.read(), 'html5lib')
    good_result_div = body.find(class_='list-header').find('dd')
    if good_result_div is not None:
        global good_result
        good_result = good_result_div.get_text()
        print(good_result.strip()+'\n')
        '''
        if ans1 in good_result or ans2 in good_result or ans3 in good_result:
            time1 = good_result.count(ans1)
            time2 = good_result.count(ans2)
            time3 = good_result.count(ans3)
            group = [time1,time2,time3]
            maxtime = max(group)
            positionmax = group.index(maxtime)
            if positionmax == 0:
                bestans = ans1
            if positionmax == 1:
                bestans = ans2
            if positionmax == 2:
                bestans = ans3
                '''

    second_result_div = body.find(class_='list-inner').find(class_='list')
    if second_result_div is not None:
        global second_result
        second_result = second_result_div.find('dl').find('dd').get_text()
        print(second_result.strip()+'\n')
        '''
        if ans1 in second_result or ans2 in second_result or ans3 in second_result:
            time1 = second_result.count(ans1)
            time2 = second_result.count(ans2)
            time3 = second_result.count(ans3)
            group = [time1,time2,time3]
            maxtime = max(group)
            positionmax = group.index(maxtime)
            if positionmax == 0:
                bestans = ans1
            if positionmax == 1:
                bestans = ans2
            if positionmax == 2:
                bestans = ans3

    print('最佳参考答案为:'+bestans)
    '''
        
if __name__ == '__main__':
    main()
