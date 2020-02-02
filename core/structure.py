
import re
import json
from . import config as cf

import pprint


structure_tip = {
    'insert':   ['simple', ['insert',   'i']    ],
    'import':   ['simple', ['import',   'imp']  ],
    'name':     ['simple', ['name',     'n']    ],

    'place_prep': ['complex', ['place', 'prep'] ],
    'place_final':['complex', ['place', 'final']],

    'vars':     ['normal', ['vars',     'vs']   ],
    'merge':    ['normal', ['merge',    'm']    ],
    'src':      ['normal', ['src']              ],
    'prep':     ['normal', ['prep']             ],
    'prll':     ['normal', ['parallel', 'prll'] ],
    'final':    ['normal', ['final']            ],

    'if':       ['normal', ['if']               ],
    'for':      ['normal', ['for']              ],
    'condition':['simple', ['condition','con']  ],
}

def strer(name, lang, last = False):

    if last:    last = r'^[\s\S]*'
    else:       last = ''

    comm = [r'/\*\s*?', r'\s*?\*/']

    st_cont = r'(?P<cont>[\s\S]*?)'
    if isinstance(name, list):
        st_cont = name[1].replace('.', r'\.')
        name = name[0]

    val = structure_tip[name]


    ss = []

    if lang == 'html':
        if val[0] == 'simple':
            for i in val[1]:
                sh =    last + r'(?P<full>{\s*?' +i+ r'\s*?{\s*?' +st_cont+ r'\s*?}\s*?(' +i+ r')?\s*?})'
                ss.append(sh)
        elif val[0] == 'complex':
            sh =        last + r'(?P<full>{\s*?' +val[0][0]+ r'\s*?{\s*?' +st_cont+ r'\s*?}\s*?' +val[0][1]+ r'\s*?})'
            ss.append(sh)
        else:
            for i in val[1]:
                sh =    last + r'(?P<full>{\s*?' +i+ r'\s*?{' + st_cont + r'}\s*?' +i+ r'\s*?})'
                ss.append(sh)
                
    elif lang == 'style' or lang == 'script':
        if val[0] == 'simple':
            for i in val[1]:
                sh =    last + r'(?P<full>' +comm[0]+ r'{\s*?' +i+ r'\s*?{\s*?' +st_cont+ r'\s*?}\s*?(' +i+ r')?\s*?}' +comm[1]+ r')'
                ss.append(sh)
            for i in val[1]:
                sh =    last + r'(?P<full>{\s*?' +i+ r'\s*?{\s*?' +st_cont+ r'\s*?}\s*?(' +i+ r')?\s*?})'
                ss.append(sh)
        elif val[0] == 'complex':
            sh =        last + r'(?P<full>' +comm[0]+ r'{\s*?' +val[0][0]+ r'\s*?{\s*?' +st_cont+ r'\s*?}\s*?' +val[0][1]+ r'\s*?}' +comm[1]+ r')'
            ss.append(sh)
            sh =        last + r'(?P<full>{\s*?' +val[0][0]+ r'\s*?{\s*?' +st_cont+ r'\s*?}\s*?' +val[0][1]+ r'\s*?})'
            ss.append(sh)
        else:
            for i in val[1]:
                sh =    last + r'(?P<full>' +comm[0]+ r'{\s*?' +i+ r'\s*?{' + comm[1] + st_cont + comm[0] + r'}\s*?' +i+ r'\s*?}' +comm[1]+ r')'
                ss.append(sh)

    rers = []
    for i in ss:
        rer = re.compile(i)
        rers.append(rer)
    return rers







    






class allvs(object):

    code = str
    lang = str
    def __init__(self, code, lang):
        self.code = code
        self.lang = lang
    
    def insert(self, varss):
        code = self.code
        lang = self.lang
        
        for i in varss:
            val = varss[i]
            if type(val) == str:
                code = vs(code, lang).insert(i, val)
            elif type(val) == dict:
                for ii in val:
                    vall = val[ii]
                    if type(vall) == str:
                        code = vs(code, lang).insert(i+'.'+ii, vall)
                    elif type(vall) == dict:
                        for iii in vall:
                            valll = val[iii]
                            if type(valll) == str:
                                code = vs(code, lang).insert(i+'.'+ii+'.'+iii, valll)
                            elif type(valll) == dict:
                                print('error dict keys')
                                print('dict - ', varss)
                                print('key - ', i+'.'+ii+'.'+iii)
        self.code = code
        self.lang = lang
        
        return code




class sp(object):

    code = str
    lang = str
    rers = []
    def __init__(self, code, lang, name, last = False):
        self.code = code
        self.lang = lang
        self.rers = strer(name, lang, last)

    def get(self, first = False):
        res = []
        code = self.code
        for i in self.rers:
            ser = i.search(code)
            if ser != None:
                res.append(ser.group('cont').strip())
                code = code.replace(ser.group('full'), '')
        
        if first:
            if len(res)>0: return res[0]
            else: return False
        else: return res

    def replace(self, zam = '', first = False):
        for i in self.rers:
            ser = i.search(self.code)
            if ser != None:
                self.code = self.code.replace(ser.group('full'), zam)
                if first: return self.code
        return self.code

    def getrepl(self, zam = '', first = False):
        res = []
        for i in self.rers:
            ser = i.search(self.code)
            if ser != None:
                res.append(ser.group('cont').strip())
                self.code = self.code.replace(ser.group('full'), zam)
                if first: return [res[0], self.code]

        if first:
            if len(res)>0: return [res[0], self.code]
            else: return [False, self.code]
        else: return [res, self.code]







class vs(object):
    
    code = str
    lang = str
    def __init__(self, code, lang):
        self.code = code
        self.lang = lang

    def find(self, name = False):
        check = sp(self.code, self.lang, 'insert', True).get()
        if name:
            if name in check:   return True
            else:               return False
        return check

    def get(self):
        varss = {}
        [varss_all, self.code] = sp(self.code, self.lang, 'vars').getrepl()
        for vs in varss_all:
            varss.update(json.loads('{'+vs+'}'))
        return varss

    def insert(self, key, val):
        self.code = sp(self.code, self.lang, ['insert', key]).replace(val)
        return self.code

    def check(self, code):
        h = sp(self.code, self.lang, 'insert')
        if h.get():
            return h.get()
        else:
            False






class st(object):
    
    code = str
    lang = str
    def __init__(self, code, lang):
        self.code = code
        self.lang = lang


    def sp(self, name, last = False):
        return sp(self.code, self.lang, name, last)

    def vs(self):
        return vs(self.code, self.lang)

    def allvs(self):
        return allvs(self.code, self.lang)


    def get_varss(self):
        varss = {}
        return varss

    def insert_varss(self, varss):
        pass


    def get_prll(self, varss, shelf = False, merge_prll = False):
        sp_code = sp(self.code, self.lang, 'prll', True)
        [code_all, self.code] = sp_code.getrepl()
        
        if merge_prll:
            prll = merge_prll
        else:
            prll = {'script': {},'style': {},}

        for code in code_all:
            for i in ['style', 'script']:
                stsc = cf.sint(code).tag(i, True)
                if stsc != False:
                    stsc = stsc.group('cont')

                    if len(prll[i]) == 0:
                        prll[i] = cf.replace_id(['html', i, 'prll'], stsc)
                    else:
                        for ii in prll[i]:
                            prll[i][ii] = prll[i][ii] + stsc

        
        if shelf:
            for i in prll:
                for ii in prll[i]:
                    if not merge_prll:
                        prll[i][ii] = shelf.prll[i] + prll[i][ii]
                    prll[i][ii] = allvs(prll[i][ii], self.lang).insert(varss)

        return prll












class FullProcessingCode(object):
    
    code = str
    lang = str
    def __init__(self, code, lang, varss = {}):
        self.code = code
        self.lang = 'html'
        self.varss = varss
        

    

    varss = {}
    def act_varss(self):
        
        code = self.code
        code = sp(code, self.lang, 'merge', True).replace()
        code = sp(code, self.lang, 'prll', True).replace()

        h = vs(code, self.lang)
        self.varss = h.get()
        self.code = h.code
        
        return self
    
    def act_merge(self):
        merge = {
            'name': False,
            'varss': {},
            'key_repl': str,
            'check': False,
        }

        key_repl = ''
        h = cf.replace_id(['html', 'replace', 'merge'], '')
        for i in h: key_repl = i

        [code_all, self.code] = sp(self.code, self.lang, 'merge', True).getrepl(key_repl)
        
        for code in code_all:
            merge['key_repl'] = key_repl
            merge['name'] = sp(code, self.lang, 'name', True).get(True)
            merge['varss'] = cf.helper().merge_dict(merge['varss'], vs(code, self.lang).get())
            merge['check'] = True
        
        self.merge = merge
        return self


    prll = {
        'script': {
            'repl_key': 'repl_val',
        },
        'style': {
            'repl_key': 'repl_val',
        },
    }
    def act_prll(self, shelf = False, prll_plus = False):
        sp_code = sp(self.code, self.lang, 'prll', True)
        [code_all, self.code] = sp_code.getrepl()
        
        if prll_plus:
            prll = prll_plus
        else:
            prll = {'script': {},'style': {},}

        varss = self.varss
        for code in code_all:
            varss = cf.helper().merge_dict(varss, vs(code, self.lang).get())

            for i in ['style', 'script']:
                stsc = cf.sint(code).tag(i, True)
                if stsc != False:
                    stsc = stsc.group('cont')

                    if len(prll[i]) == 0:
                        prll[i] = cf.replace_id(['html', i, 'prll'], stsc)
                    else:
                        for ii in prll[i]:
                            prll[i][ii] = prll[i][ii] + stsc

        
        
        for i in prll:
            for ii in prll[i]:
                if not prll_plus:
                    prll[i][ii] = shelf.prll[i] + prll[i][ii]
                prll[i][ii] = allvs(prll[i][ii], self.lang).insert(self.varss)

        self.prll = prll
        return self


    def fpc_merge_varss(self, fpc_plus):
        self.varss = cf.helper().merge_dict(self.varss, fpc_plus.varss)



    def insert(self, varss = {}):
        varss = cf.helper().merge_dict(self.varss, varss)
        self.code = allvs(self.code, self.lang).insert(varss)