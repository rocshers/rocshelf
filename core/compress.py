import json
import os
import re
import shutil
import sys
from os.path import join

from . import config as cf
from .structure import st




class Packing(object):

    def __init__(self, page):
        trans = cf.path_core('trans') + page.name + '/'
        if not os.path.isdir(trans):
            os.mkdir(trans)


        with open(trans + 'page.html', "w") as newFile:
            code = page.code
            newFile.write( code )

        with open(trans + 'style.' + cf.setti('use_sass'), "w") as newFile:
            code = page.code
            newFile.write( code )

        with open(trans + 'script.js', "w") as newFile:
            code = page.code
            newFile.write( code )
        

        shutil.rmtree(trans)



    

class Compress(object):
    

    def __init__(self, page):
        Packing(page)

        code = ""
        code = self.__final(code)


    
    def __final(self, code):
        self.final = {}
        sp_code = st(code, 'html').sp('final', True)
        while sp_code.get(True):
            h = cf.replace_id('html', 'replace', 'final', sp_code.get(True))
            self.final.update(h)
            for i in h: code = sp_code.replace(i)
        return code