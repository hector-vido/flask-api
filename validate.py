#!/usr/bin/env python3

import sqlite3
from pathlib import Path

db = Path("data.db")
if not db.is_file():
    print('O arquivo data.db não foi encontrado, por favor inicialize o banco de dados.')
    exit(1)

class bcolors:
    OK = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

with sqlite3.connect('data.db') as db:
	db.row_factory = sqlite3.Row
	cursor = db.cursor()
	
	cursor.execute("SELECT * FROM contents WHERE id = 'home_title'")
	row = cursor.fetchone()
	if not row:
		print('{0}O registro "home_title" não foi encontrado{1}'.format(bcolors.FAIL, bcolors.ENDC))
	elif row['content'].lower() == '4linux - sysadmin & apis':
		print('{0}O registro "home_title" está correto!{1}'.format(bcolors.OK, bcolors.ENDC))
	else:
		print('{0}O registro "home_title" está incorreto, encontramos -> {1}{2}'.format(bcolors.FAIL, row['content'], bcolors.ENDC))

	cursor.execute("SELECT * FROM contents WHERE id = 'home_m1_p'")
	row = cursor.fetchone()
	if not row:
		print('{0}O registro "home_m1_p" não foi encontrado{1}'.format(bcolors.FAIL, bcolors.ENDC))
	elif row['content'].lower() == 'django, flask e pyramid são alguns exemplos de frameworks para python. neste caso estamos utilizando o flask por ser o mais simples e prático!':
		print('{0}O registro "home_m1_p" está correto!{1}'.format(bcolors.OK, bcolors.ENDC))
	else:
		print('{0}O registro "home_m1_p" está incorreto, encontramos -> {1}...{2}'.format(bcolors.FAIL, row['content'][0:40], bcolors.ENDC))

	cursor.execute("SELECT * FROM contents_childs WHERE icon = 'ti-game' AND parent = 'home_m1_boxes'")
	row = cursor.fetchone()
	if not row:
		print('{0}O bloco não foi encontrado{1}'.format(bcolors.FAIL, bcolors.ENDC))
	elif row['content'].lower() == 'se eu consegui colocar este bloco no site, significa que entendi como funciona uma api rest!' and row['title'].lower() == 'gamefication' and row['icon'].lower() == 'ti-game':
		print('{0}O bloco está correto!{1}'.format(bcolors.OK, bcolors.ENDC))
	else:
		print('{0}O bloco está incorreto, encontramos:\ntitle: {1}\nicon: {2}\ncontent: {3}...{4}'.format(bcolors.FAIL, row['title'], row['icon'], row['content'][0:40], bcolors.ENDC))
