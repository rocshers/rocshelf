import json
import os
import re
import shutil
import sys
from os.path import join

from . import config as cf
from .structure import st


class SearchShelf(object):

    place = str
    search = bool
    name = str
    path = str
    def __init__(self, place, full_name):

        self.place = path = pros = place
        folders = list(filter(None, re.split(r'[\.\/]', full_name)))

        for fold in folders:
            pros = os.path.abspath(join(pros,fold)) + '/'

        path = self.__search(path, folders[0])
        if path != False:
            for fold in folders[1:]:
                path = join(path, fold) + '/'
                if not os.path.exists(path):
                    path = False
                    break

        self.name = folders.pop()
        if path:
            self.search = True
            self.path = path
        else:
            self.search = False
            self.path = pros


            

    def __search(self, path_s, name):
        path = False
        folders = [path_s]
        while not path:
            if len(folders) == 0:
                path = True
            else:
                for folder in folders:
                    fullpath = join(folder, name) + '/'
                    if os.path.exists(fullpath):
                        path = fullpath
                        break
                    else:
                        folders.remove(folder)
                        for walk_all in os.walk(folder):
                            for walk_dir in walk_all[1]:
                                folder = join(folder, walk_dir) + '/'
                                folders = folders + [ folder ]

        if path == False or path == True:
            return False
        else:
            return path












class Shelf(SearchShelf):


    zone = str
    def __init__(self, zone, name):
        if zone in cf.shelves:
            self.zone = zone
            SearchShelf.__init__(self, cf.path_user(zone), name)
        else:
            exit('error zone - ' , zone)


    def create(self):
        ignore = shutil.ignore_patterns('*.'+cf.setti('ignor_sass'), cf.setti('ignor_sass'))
        shutil.copytree( cf.path_core('layouts') + self.zone, self.path, ignore = ignore )
        for wal in os.walk(self.path):
            for file in wal[2]:
                with open(self.path + file, "r") as newFile:
                    text = newFile.read()
                with open(self.path + file, "w") as newFile:
                    text = st(text, file.split('.')[1]).vs().insert('name', self.name)
                    newFile.write( text )
        return self


    def delite(self):
        shutil.rmtree(self.path)
        return True

















    
    def get(self):

        self.__get_merge()
        self.__get_cut()
        self.__prll_cut()

        return self



    html = script = style = str
    def __get_merge(self):
        path = self.path
        data = {
            'html': str,
            'script': str,
            cf.setti('use_sass'): str,
        }

        for i in data:

            if os.path.isfile(path + i+'.'+i):
                with open( path + i+'.'+i , 'r', encoding='utf-8') as fh:
                    val = fh.read()
            else:
                val = ''
            while st(val, i).sp('import').get():
                name = st(val, i).sp('import').get()
                path_one = path + i + '/' + name + '.' + i
                if os.path.isfile(path_one):
                    with open(path_one, 'r', encoding='utf-8') as fh:
                        mes = fh.read()
                else:
                    if i == 'html': mes = '{import{ '+name+' }not found}'
                    else:           mes = '/* {import{ '+name+' }not found} */'

                val = st(val, i).sp('import').replace(mes)

            data[i] = val

            
        if 'scss' in data:
            data['style'] = data.pop('scss')
        
        self.html = data['html']
        self.script = data['script']
        self.style = data['style']

    prll = {
        'script': str,
        'style': str,
    }
    def __prll_cut(self):
        self.prll['script'] = self.script['prll']
        self.prll['style']  = self.style['prll']
    
    def __get_cut(self):
        
        data = {
            'script': self.script,
            'style': self.style,
        }
        
        new_data = {
            'style': 'prep',
            'script':   'final',
        }

        for lang in new_data:
            isc = new_data[lang]
            new_data[lang] = {}

            code = data[lang]
            for tip in cf.code_marking:
                sth = st(code, lang).sp(tip, True)
                if tip == isc:
                    while sth.get():
                        res = sth.get()
                        for i in res:
                            code = sth.replace(i)
                else:
                    text = ''
                    while sth.get():
                        res = sth.get()
                        for i in res:
                            text = text + '\n\n\n' + i
                            code = sth.replace('')
                    new_data[lang][tip] = text
                    
            new_data[lang][isc] = code


        self.script =   new_data['script']
        self.style = new_data['style']
