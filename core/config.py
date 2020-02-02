# basic 
import os
import sys
import re
from os.path import abspath as path
import json
import random
import copy
from .structure import st


shelves = ['basic', 'page', 'tag']
user_dir = ['basic', 'page', 'tag', 'static', 'template']

class ClassConfig(object):

    

    config = {}
    user_config = {}
    def __init__(self):

        users_cfg = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] + '/config.json'
        
        if os.path.isfile(users_cfg):
            with open( users_cfg, 'r', encoding='utf-8') as fh:
                self.user_config = json.load(fh)
        else:
            newFile = open( users_cfg , 'w')
            newFile.close()
            exit("Заполните файл конфигурации")



        self.__path()
        self.__path_build()

        self.__setting()
        self.__route()

        self.__create_json()

    


    def __setting(self):
        sett = self.user_config['setting']
        
        [a, c] = ['sass', 'scss']
        if a in sett:
            if sett[a] == a:
                [a, c] = [c, a]
                del sett[c]
            else:
                del sett[a]
        [sett['use_sass'], sett['ignor_sass']] = [c, a]

        self.config['setting'] = sett
    
    def __route(self):
        self.config['routs'] =   self.user_config['routs']
    
    


    path = {
        'core': {},
        'user': {},
    }
    def __path(self):
        self.path['core']['core'] = core = os.path.abspath(os.path.dirname(__file__))
        self.path['user']['user'] = os.path.split(os.path.split(core)[0])[0]
        
        self.__path_core()
        self.__path_user()

        self.config['path'] = self.path


    
    def __path_core(self):
        core_folders = {
            'layouts': 'layouts_files',
            'trans': 'transition',
            'pycache': '__pycache__'
        }
        for i in core_folders:
            self.path['core'][i] = self.path['core']['core'] + '/' + core_folders[i]

    def __path_user(self):
        path = self.path        
        user_paths = self.user_config['path']
        for pata in user_dir:
            folders = list(filter(None, user_paths[pata].split('/')))
            path_new = path['user']['user']
            for folder in folders:
                path_new = os.path.abspath(os.path.join(path_new,folder)) + '/'
            
            path['user'][pata] = path_new

        self.path = path


    def __path_build(self):
        for i in ['core', 'user']:
            for name in self.config['path'][i]:
                path = self.config['path'][i][name]
                if not path[len(path)-1] == '/':
                    self.config['path'][i][name] = path + '/'
                if not os.path.exists(path):
                    os.makedirs(path)




    def __create_json(self):
        with open( os.path.abspath(os.path.dirname(__file__)) + '/cfg.json' , 'w', encoding='utf-8') as fh:
            json.dump(self.config, fh, indent=4)




    











def init():
    global cfg
    with open( os.path.abspath(os.path.dirname(__file__)) + '/cfg.json' , 'r', encoding='utf-8') as fh:
        cfg = json.load(fh)

def path_core(name = None):
    if name == None: return cfg['path']['core']
    if name in cfg['path']['core']: return cfg['path']['core'][name]

def path_user(name = None):
    if name == None: return cfg['path']['user']
    if name in cfg['path']['user']: return cfg['path']['user'][name]

def setti(name = None):
    if name == None: return cfg['setting']
    if name in cfg['setting']: return cfg['setting'][name]

def routs():
    return cfg['routs']


    
class helper(object):

    def clear_list(self, listt):
        new_listt = []
        for i in listt:
            if not i in new_listt:
                new_listt.append(i)
        return new_listt

    def merge_dict(self, old, new):
        new_dict = copy.copy(old)
        
        for i in new:
            if i in new_dict:
                if type(new_dict[i]) == type(new[i]):
                    if type(new[i]) == list:
                        new_dict[i] = self.clear_list(new_dict[i] + new[i])
                    elif type(new[i]) == dict:
                        new_dict[i] = self.merge_dict(new_dict[i], new[i])
                    else:new_dict[i] = new[i]
                else:new_dict[i] = new[i]
            else:new_dict[i] = new[i]
            
        return new_dict


black_list_names = ['sass', 'scss', 'js', 'html', 'script', 'style']
code_marking = ['prep', 'prll', 'final']


def replace_id(words, zam):
    rand = random.random()

    if words[0] == 'html':                          comm = ['<!--', '-->']
    elif words[0] == 'style' or words[0] == 'script':    comm = ['/*', '*/']

    for i in words:
        words_str = words_str + i + '-'

    name = comm[0]+ '  {replace{ ' + words_str + str(rand)+' }replace}  ' +comm[1]

    return {name: zam}






class sint(object):

    code = str
    lang = str
    def __init__(self, code, lang = 'html'):
        self.code = code
        self.lang = 'html'

    def tag(self, tip, last = False):
        if last:    last = [r'^[\s\S]*', '?']
        else:       last = ['', '']

        name = r'(?P<name>[\w\.]+)'
        if isinstance(tip, list):
            name = r'(?P<name>'+tip[1]+r')'
            tip = tip[0]
        
        if tip == 'tag' or tip == 't':
            st = last[0] + r'(?P<full><\s*?(?P<tip>' +tip+ r')-' +name+ r'(-(?P<tag>\w+))?(?P<attrs>\s+[\s\S]*?)?>(?P<cont>[\s\S]*' +last[1]+ r')</\s*?' +tip+ r'-([\w\.]+)(-(\w+))?\s*?>)'
        else:
            st = last[0] + r'<\s*?' +tip+ r'\s*?>(?P<cont>[\s\S]*' +last[1]+ r')</\s*?' +tip+ r'\s*?>'

        regulag = re.compile(st)
        s = regulag.search(self.code)
        if s != None:   return s
        else:           return False