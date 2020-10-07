#coding=utf-8
import sys
import json
from zipfile import ZipFile

from bs4 import BeautifulSoup

def utf8escape(str):
    ret = '';
    for char in str:
       ret += '&#' + hex(ord(char))[1:] + ';'
    return ret

def notehtml(str):
    str = BeautifulSoup(str, "html.parser").text
    sline = str.split("\n")
    ret = "".join([ '<p>' + rr + '</p>' for rr in sline ])
    return ret

def totext(node,elements): # {'title':'TEXT', 'link':'LINK', 'note','NOTE'}
    rets = ['<node']
    retend = []
    for i in elements.keys():
        if i in node and not node[i] == None and len(node[i]) > 1:
            if i in [ 'note' ]:
                tmp = '<richcontent TYPE="NOTE"><html><head></head><body>' + notehtml(node[i]) + '</body></html></richcontent>'
                retend += [ tmp ]
            else:
                if i in [ 'title00' ]:
                    tmp = node[i]
                else:
                    tmp = utf8escape(node[i])
                tmp = elements[i] + "='" + tmp + "'"
                rets += [ tmp ]
    rets += [ '>' ]
    if len(rets) > 2:
        if len(retend) > 0:
            rets += retend
#        print rets
        return " ".join(rets)
    else:
        return ""

def process(nodes):
    ret = ''
    eles = {'title':'TEXT', 'link':'LINK', 'note':'NOTE'}
    for node in nodes:
        ret += totext(node,eles)
        if node['children']:
            ret += process(node['children'])
        ret += '</node>\n'
    return ret

mindfile = ZipFile(sys.argv[1], 'r').open('map.json').read()
data = json.loads(mindfile)

export = '<map version="1.0.1">'
export += process([data['root']])
export += '</map>'

exportfile = open(sys.argv[2], 'wb+')
exportfile.write(export.encode('utf-8'))

with open(sys.argv[2] + ".json","w") as ffout:
    ffout.write(json.dumps(data,separators=(',',':'),indent=4) + "\n")
