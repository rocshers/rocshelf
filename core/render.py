import json
import re

from bs4 import BeautifulSoup as bs

from . import config as cf
from . import htmltag
from .shelves import Shelf
from .structure import FullProcessingCode as fpc
from .structure import st
import pprint

class Render(object):

    
    

    shelf_list = []

    name = str

    stpage = object

    def __init__(self, page):

        self.name = page.name
        self.code = page.html

        self.prll = {'style': {},'script': {},}
        self.pmf = {
            'prep': {'style': [],'script': []},
            'final': {'style': [],'script': []},
        }

        self.shelf_list.append(page)


        varss = self.__get_varss()
        self.__prll(varss, page)

        self.__merge()
        
        

        
        

        self.__tags()





        self.__src()


    
    def __get_varss(self):
        code_no_tag = htmltag.delite_tag(self.code)
        varss = st(code_no_tag, 'html').get_varss()
        return varss

    def __prll(self, varss, shelf):
        h = st(self.code, 'html')
        self.__prll_merge(h.get_prll(varss, shelf))
        self.code = h.code



    def __merge(self):
        self.basic_name = []

        sppage = st(self.code, 'html', ).sp('merge', True)
        code = sppage.code
        while sppage.get(True):
            name = sppage.get(True)
            code = sppage.replace('', True)

            basic = Shelf('basic', name).get()
            if basic.search:
                
                stspbasic = st(basic.html, 'html').sp('merge', True)
                if stspbasic.get(True):
                    self.shelf_list.append(basic)

                    stspbasic.replace(sppage.code, True)

                    code = stspbasic.code

                    varss = self.__get_varss()
                    self.__prll(varss, basic)

        self.code = code




    tags = []
    def __tags(self):
        code = self.code
        
        while cf.sint(code).tag('tag', True):
            MT = htmltag.MAINTAG(code)
            code = MT.page
            self.__prll_merge(MT.prll)
            self.__pmf_merge(MT.shelf)
            self.tags.append(MT.name)

        self.code = code






    def __src(self):
        src = {
            'script': {'prep': [],'final': [],},
            'style': {'prep': [],'final': [],},
        }

        sp_code = st(self.code, 'html').sp('src', True)
        [code_all, self.code] = sp_code.getrepl()

        for code_vs in code_all:
            src_var = json.loads('{'+code_vs+'}')
            src = cf.helper().merge_dict(src, src_var)

        self.src = src






    def __pmf_merge(self, shelf):

        self.pmf['prep']['script']   =  self.pmf['prep']['script']  + shelf.script['prep']
        self.pmf['prep']['style']    =  self.pmf['prep']['style']   + shelf.style['prep']

        self.pmf['final']['script']  =  self.pmf['final']['script'] + shelf.script['final']
        self.pmf['final']['style']   =  self.pmf['final']['style']  + shelf.style['final']
        
        

    
    def __prll_merge(self, prll):
        for i in prll:
            if prll[i]:
                for ii in prll[i]:
                    self.prll[i][ii] = prll[i][ii]


    