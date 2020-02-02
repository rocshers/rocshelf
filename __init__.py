"""
	rocshelf v 0.1 ( Pre-Alpha )
	Заложен фундамент принципа работы и инструменты для разработки.
"""

import click
from core import rocshelf as core
from core import core_clear

@click.group()
def cli():
    pass

@click.command()
@click.option('--action', 	'-a', default = False, help='Действие ( create / delite )')
@click.option('--shelf', 	'-s', default = False, help='Тип ( page , tag , basic ) ')
@click.option('--name', 	'-n', default = False, help='Название')
def shelf(action, shelf, name):
	if not action:	exit('Введите действие -a !')
	if not shelf:	exit('Введите тип элемента -s !')
	if not name:	exit('Введите имя элемента -n !')
	core().shelf(shelf, name, action)

@click.command()
def start():
	core().start()

@click.command()
def training():
	core().training()

@click.command()
def clear():
	core_clear()

cli.add_command(shelf)
cli.add_command(start)
cli.add_command(training)
cli.add_command(clear)

if __name__ == '__main__':
    cli()	