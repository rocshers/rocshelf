import re

from . import config as cf
from .shelves import Shelf
from .structure import st
from .structure import FullProcessingCode as fpc





regular = {}
regular['attrs_one'] = re.compile(r"(?P<full>([\w\-]+)\s*?=\s*?'(?P<attrs>[\s\S]+?)')")
regular['attrs_two'] = re.compile(r'(?P<full>([\w\-]+)\s*?=\s*?"(?P<attrs>[\s\S]+?)")')



















setting_tag = {
    'move': ['static', 'dinamic'],
    'quantity': ['one', 'many'],
}

class Info(object):

    full = tip = tag = name = attrs_t = cont = str
    def __init__(self, reobj):
        data = reobj.groupdict()

        self.tip = data['tip']
        self.name = data['name']
        self.tag  = data['tag']
        
        self.full = data['full']
        self.cont = data['cont']
        
        self.__attrs(data['attrs'])

    setting = {
        'move': 'static'
    }
    attrs = {}
    attrs_ress = []
    def __attrs(self, title):
        if title != None:

            attrs = {}
            for i in ['one', 'two']:
                at = regular['attrs_' + i].findall(title)
                for varsa in at:
                    attrs[varsa[1]] = varsa[2]
                title = regular['attrs_' + i].sub('', title)

            for i in attrs:
                attrs[i] = attrs[i].split()
            self.attrs = attrs

            attrs_ress = title.split()
            for i in setting_tag:
                val = setting_tag[i]
                for ii in val:
                    if ii in attrs_ress:
                        self.setting[i] = ii
                        attrs_ress.remove(ii)
            self.attrs_ress = attrs_ress



zero_tag = zero_tag = Info(cf.sint(r'<t-n></t-n>').tag('t'))







no_repeat = ['class']
only_one = ['href']

class Merge(object):


    name = str
    def __init__(self, MOD, ORIG):
        self.name = MOD.name
        self.__attrs(MOD, ORIG)
        self.__content(MOD, ORIG)
        

    tag = str
    attrs = {}
    attrs_ress = []
    def __attrs(self, MOD, ORIG):
        
        tag = MOD.tag
        if tag == None: tag = ORIG.tag
        if tag == None: tag = False
        self.tag = tag


        attrs = {}
        attrs_help = {
            'orig': ORIG.attrs,
            'mod': MOD.attrs,
        }
        for i in attrs_help:
            for ii in attrs_help[i]:
                if ii in attrs: attrs[ii] = attrs[ii] + attrs_help[i][ii]
                else:           attrs[ii] = attrs_help[i][ii]
        
        for i in attrs:
            if i in no_repeat:
                attrs[i] = cf.helper().clear_list(attrs[i])
            if i in only_one:
                attrs[i] = attrs[i].pop()

        self.attrs = attrs


        attrs_ress = cf.helper().clear_list(ORIG.attrs_ress + MOD.attrs_ress)
        self.attrs_ress = attrs_ress


    old = {}
    cont = {}
    def __content(self, MOD, ORIG):
        self.old = {
            'orig': ORIG.full,
            'mod': MOD.full,
        }
        self.cont = {
            'orig': ORIG.cont,
            'mod': MOD.cont,
        }







    
class Render(Merge):

    name = str
    tag = str

    def __init__(self, MOD, ORIG):
        Merge.__init__(self, MOD, ORIG)

        self.__title()
        self.__content()


    title = bottom = str
    def __title(self):

        if not self.tag:
            self.title = self.bottom = ''
        else:
            tag = self.tag
            attrs = self.attrs
            attrs_ress = self.attrs_ress

            for i in attrs:
                st_help = ''
                for ii in attrs[i]:
                    st_help = st_help + ii + ' '
                straka = i + '="' + st_help.strip() + '"'
                attrs_ress.append(straka)
            
            straka = ''
            for i in attrs_ress:
                straka = straka + i + ' '
            
            straka = straka.strip()
            if straka != '': straka = ' ' + straka

            self.title = '<' + tag + straka + '>'
            self.bottom = '</' + tag + '>'


    def __content(self):
        mod_cont = self.cont['mod']
        orig_cont = self.cont['orig']
        
        if st(self.title, 'html').vs().find('content'):
            self.title = st(self.title, 'html').vs().insert('content', mod_cont)
            self.cont = ''
        elif st(orig_cont, 'html').vs().find('content'):
            orig_cont = st(orig_cont, 'html').vs().insert('content', mod_cont)
            self.cont = orig_cont
        else:
            self.cont = mod_cont


    def render(self):
        self.new = self.title + self.cont + self.bottom
    
    def insert(self, varss):
        self.new = st(self.new, 'html').allvs().insert(varss)

    def prll(self, prll):
        for i in prll:
            if prll[i]:
                for ii in prll[i]:
                    self.new = self.new + '\n' + ii

    def replace(self, html, tip, use_new):
        if use_new: use_new = self.new
        else:       use_new = ""
        
        html = html.replace(self.old[tip], use_new)
        return html


























class MAINTAG(object):


    page = str
    MOD = ORIG = Info
    def __init__(self, html):
        
        self.page = html
        if  self.__FIND_tag():
            self.name = self.shelf.name

            self.cont = {
                'orig': self.ORIG.cont,
                'mod': self.MOD.cont,
            }
            self.__clear_1_tag()

            fpc_orig = fpc(self.cont['orig'], 'html').act_varss().act_prll(self.shelf)
            
            fpc_mod = fpc(self.cont['mod'], 'html').act_varss()
            fpc_mod.varss = cf.helper().merge_dict(fpc_mod.varss, fpc_orig.varss)
            fpc_mod.act_prll(self.shelf, fpc_orig.prll)
            
            self.cont['orig'] = fpc_orig.code
            self.cont['mod'] = fpc_mod.code
            
            self.__FIND_t()
            self.__clear_2_tag()

            self.ORIG.cont = self.cont['orig']
            self.MOD.cont  = self.cont['mod']

            new_tag = Render(self.MOD, self.ORIG)
            new_tag.render()

            fpc_mod.code = new_tag.new
            fpc_mod.insert()

            new_tag.new = fpc_mod.code
            self.prll = fpc_mod.prll
            
            new_tag.prll(self.prll)


            self.page = new_tag.replace(self.page, 'mod', True)


            







    

    shelf = Shelf
    name = str
    def __FIND_tag(self):
        ret = False
        MOD = ORIG = zero_tag

        mod_reobj = cf.sint(self.page).tag('tag', True)
        if mod_reobj:
            MOD = Info(mod_reobj)
            shelf = Shelf('tag', MOD.name).get()
            if shelf.search:
                self.shelf = shelf
                orig_reobj = cf.sint(shelf.html).tag('tag', False)
                if orig_reobj:
                    ORIG = Info(orig_reobj)
                else:
                    print('Элемент Tag с именем '+ MOD.name +' не подходит форматом')
            else:
                print('Не найден элемент Tag с именем '+ MOD.name)
            ret = True

        if MOD:     self.MOD = MOD
        if ORIG:    self.ORIG = ORIG
        return ret
        
    

    def __FIND_t(self):
        cont = self.cont
        while cf.sint(cont['orig']).tag( 't', True):
            orig_reobj = cf.sint(cont['orig']).tag( 't', True)
            ORIG = Info(orig_reobj)

            mod_reobj = cf.sint(cont['mod']).tag( ['t', ORIG.name], True)
            if mod_reobj:   MOD = Info(mod_reobj)
            else:           MOD = zero_tag

            new_tag = Render(MOD, ORIG)
            new_tag.render()
            
            if ORIG.setting['move'] == 'static':
                h = [True, False]
            elif ORIG.setting['move'] == 'dinamic':
                h = [False, True]
            
            cont['orig'] = new_tag.replace(cont['orig'],'orig', h[0])
            cont['mod'] =  new_tag.replace(cont['mod'], 'mod',  h[1])
        self.cont = cont




    
    def __clear_1_tag(self):
        self.clear_list = {'mod': {},'orig': {},}
        for i in self.cont:
            [self.cont, self.clear_list[i]] = delite_tag(self.cont[i])

    def __clear_2_tag(self):
        for i in self.cont:
            for ii in self.clear_list[i]:
                self.cont[i] = self.cont[i].replace(ii, self.clear_list[i][ii])

    



    def __varss(self):
        varss = {}
        cont = self.cont
        for i in cont:
            s = st(cont[i], 'html').vs()
            varss.update(s.get())
            cont[i] = s.code
        self.cont = cont
        return varss





def delite_tag(code):
    clear_list = {}
    while cf.sint(code).tag('tag', True):
        full = cf.sint(code).tag('tag', True).group('full')
        h = cf.replace_id(['html', 'replace', 'tag'], full)
        
        clear_list.update(h)
        for ii in h:
            code = code.replace(h[ii], ii)
    return code, clear_list
    










    



















