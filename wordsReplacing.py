# -*- coding:utf-8 -*-

import os

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

def replace(filelist):
    for filePath in filelist:
        with open(filePath, 'r') as file:
          filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('媒体·达人', '媒体')
        filedata = filedata.replace('健康·美食', '养生')
        filedata = filedata.replace('时尚·格调', '时尚')
        filedata = filedata.replace('亲子·家庭', '家庭')
        filedata = filedata.replace('教育·励志', '教育')
        filedata = filedata.replace('数码·科技', '科技')
        filedata = filedata.replace('职场·商业', '职场')
        filedata = filedata.replace('财经·理财', '财经')
        filedata = filedata.replace('搞笑·段子', '搞笑')
        filedata = filedata.replace('生活·情感', '情感')
        filedata = filedata.replace('休闲·旅行', '旅游')
        filedata = filedata.replace('兴趣·爱好', '兴趣')
        filedata = filedata.replace('时事·城市', '城事')
        filedata = filedata.replace('运动·赛事', '体育')
        filedata = filedata.replace('阅读·文学', '美文')
        filedata = filedata.replace('电影·音乐', '影音')
        filedata = filedata.replace('社交·交友', '社交')
        filedata = filedata.replace('娱乐·八卦', '八卦')
        filedata = filedata.replace('房产·汽车', '汽车')


        # Write the file out again
        with open(filePath, 'w') as file:
          file.write(filedata)


print(listdir_fullpath("GHZArticle"))

replace(listdir_fullpath("GHZArticle"))




