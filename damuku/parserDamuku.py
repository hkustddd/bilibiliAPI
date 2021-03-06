# -*- coding: utf-8 -*-
# @Author: Jingyuexing
# @Date:   2020-04-30 15:48:44
# @Last Modified by:   Jingyuexing
# @Last Modified time: 2020-05-20 23:57:53

import xml.etree.ElementTree as ET

class Danmaku:
    """弹幕类
    ```xml
    <d p="16.67500,1,25,16777215,1588305968,0,b00ca606,32067442918293507">借你吉言</d>
    ```
    第一个 是stime 0 然后是mode 1  再是size 2 再是color 3 再是date 4 再是pool 5 再是uhash 6 再是dmid 7
    """
    __color__:int = None
    __date__:int = None
    __dmid__:int = None
    __pool__:int = None
    __stime__:float = None
    __mode__:int = None
    __text__:str = ''
    __uhash__:str = ''
    __size__:int = None
    data:list = []

    def __init__(self,data):
        if(data!=''):
            root = ET.parse(data)
            rootEle = root.getroot()
            for ele in rootEle.findall('d'):
                tempdict = {}
                attribList = ele.attrib['p'].split(',')
                tempdict['uhash'] = attribList[6]
                tempdict['date'] = int(attribList[4])
                tempdict['pool'] = int(attribList[5])
                tempdict['color'] = int(attribList[3])
                tempdict['size'] = int(attribList[2])
                tempdict['dmid'] = attribList[7]
                tempdict['mode'] = int(attribList[1])
                tempdict['stime'] = float(attribList[0])
                self.data.append(tempdict)

    def getDanmu(self, index=0):
        data = self.data[index]
        danmu = Danmaku("")
        danmu.__uhash__ = data['uhash']
        danmu.__date__ = data['date']
        danmu.__pool__ = data['pool']
        danmu.__size__ = data['size']
        danmu.__dmid__ = data['dmid']
        danmu.__mode__ = data['mode']
        danmu.__stime__ = data['stime']
        danmu.__color__ = data['color']
        return danmu

