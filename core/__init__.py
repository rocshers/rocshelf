# basic 
import os
import sys
import re

# download
import sass

# vendor
from .config import ClassConfig
from . import config as cf

from .shelves 	import Shelf

from .render 	import Render
from .compress	import Compress
from .save 		import Save


import shutil


def __yes_noy(mess = False):
	if not mess:
		mess = 'Are you sure to complete this action?'
	print(mess)
	yes = input('[y / n] - ')
	yes = yes.lower()
	if yes == '1' or 'yes' or 'true' or 't':
		return True
	else:
		print('cancel')
		return False

def __print_helper(nuzen, shel):
	if nuzen:
		print('Элемента ' + shel.zone + ' с именем ' + shel.name + ' не существует. Предпологаемый путь - ' + shel.path)
	if not nuzen:
		print('Элемент ' + shel.zone + ' c именем ' + shel.name + ' уже существует по пути ' + shel.path)

















class rocshelf():

	def __init__(self):
		ClassConfig()
		cf.init()
		

	def shelf(self, tip, name, action):
		if tip in cf.shelves and name:

			shel = Shelf(tip, name)

			if action == 'create':
				if not shel.search:
					if not shel.name in cf.black_list_names:
						shel.create()
					else:
						print( shel.name + ' - зарезервированное слово')
				else:
					__print_helper(False, shel)

			elif action == 'delite':
				if shel.search:
					print('Удалить компонент ' + shel.zone + ' по пути - ' + shel.path + ' ?')
					if __yes_noy():
						shel.delite()
				else:
					__print_helper(True, shel)
			
			elif action == 'get':
				if shel.search:
					shel.get()
					print(' Имя - ' + shel.name)
					print(' Тип - ' + shel.zone)
					print(' Расположение - ' + shel.path)
					print(' html - ', shel.html)
					print(' js - ', shel.script)
					print(' sass - ', shel.style)
				else:
					__print_helper(True, shel)

		else:
			print('Введен некоректный тип Элемента ({}) или имя'.format(tip))


	def start(self):
		for route in cf.routs():
			page = Shelf('page', route).get()
			if page.search:
				page = Render(page)
				page = Compress(page)
				page = Save(page)
				exit('coooomplite')
			else:
				__print_helper(True, page)


	def training(self):
		for i in ['basic', 'page', 'tag']:
			shel = Shelf(i, i + '_example')
			shel.create()

	
def core_clear():

	rocshelf()
	
	hc = ['pycache', 'trans']
	hu = ['static', 'template']

	if __yes_noy('Удалить папки BASIC, PAGES, TAGS?'):
		hu = hu + ['basic', 'page', 'tag']
		
	if __yes_noy():
		for i in hc:
			h = cf.path_core(i)
			if os.path.exists(h):
				shutil.rmtree(h)
		for i in hu:
			h = cf.path_user(i)
			if os.path.exists(h):
				shutil.rmtree(h)