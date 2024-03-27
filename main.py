import json
import random
from json import load
from json import dump
from random import randint

def suggestive_questions(rules):
	questions_list = ['Хотели бы вы посмотреть', 'Вы предпочитаете', 'Вам бы хотелось почитать',
							'Вы любите', 'Вы не прочь полистать']
	user_answer = ''
	i = 0
	j = 0

	# print(rules)
	for rule in rules:
		# print(f'j = {j}')
		if i == 1:
			continue
		elif i == 0:
			user_answer = input(f'{questions_list[random.randint(0, 4)]} {rule} да/нет? ')
			if len(rules) == 1:
				print(rule)
				return rule
			elif len(rules) == 2:
				# print(f'len = 2')
				if user_answer == 'да':
					i = 1
					print(rule)
					return rule
				elif user_answer == 'нет':
					if j == 0:
						i = 1
						print(list(rules.keys())[j + 1])
						return list(rules.keys())[j + 1]
					elif j == 1:
						i = 1
						print(list(rules.keys())[j - 1])
						return list(rules.keys())[j - 1]
			elif len(rules) > 2:
				# print(f'len >  and j = {j}')
				if user_answer == 'да':
					i = 1
					print(rule)
					return rule
				elif user_answer == 'нет':
					# print(f'len = {len(rules) - j}')
					if len(rules) - j == 2:
						i = 1
						print(list(rules.keys())[j + 1])
						return list(rules.keys())[j + 1]
				j += 1

def book_selection(genres_base):
	result = []
	full_genres = []
	for genre in genres_base:
		full_genres.append(genre)
	user_answer = input(f'Выберите предпочитаемые жанры(через запятую, без пробелов) {full_genres}: ')

	user_genres = user_answer.split(',')

	temp = []
	books = []
	for genre in genres_base:
		for book in genres_base[genre]:
			temp.append(book)
	books = list(set(temp))

	count = 0
	books_count = {}
	for book in books:
		if len(user_genres) == 1:
			for genre in user_genres:
				if list(genres_base[genre]).__contains__(book):
					result.append(book)
		elif len(user_genres) > 1:
			for genre in user_genres:
				if list(genres_base[genre]).__contains__(book):
					count += 1
			books_count[f'{book}'] = count
		count = 0

	if len(user_genres) != 1:
		genres_len = len(user_genres)
		i = 1
		while i:
			for book in books_count:
				if books_count[book] == genres_len:
					result.append(book)
			if bool(result):
				i = 0
			else:
				genres_len -= 1

	return result

def user():
	start = 1
	ch = input('\n1.Начать поиск\n2.Назад\n')
	if ch == '2':
		return
	elif ch == '1':
		book_genres_check = ['Юмористическая литература', 'Драма', 'Ужасы', 'Фэнтези', 'Фантастика',
									'Приключения', 'Детектив', 'Поэзия', 'Автобиография', 'Сказка',
									'Исторический роман', 'Мифы', 'Магический реализм', 'Легенды',
									'Эпос', 'Антиутопия', 'Постапокалипсис', 'Война', 'Эпопея']
		rules = {}
		with open('rules.json', encoding="utf-8") as rules_file:
			rules = load(rules_file)

		book_base = rules

		# для остановки перед жанрами
		while start == 1:
			rule = suggestive_questions(book_base)
			book_base = book_base[rule]
			for genre_check in book_genres_check:
				if list(book_base.keys()).__contains__(genre_check):
					start = 0

		print(f'Скорее всего вам подойдут эти книги: {book_selection(book_base)}')
	else:
		print("Выбран несуществующий пункт меню!\n")
		return

def create_rule(rules):
	print('\n')
	for rule in rules:
		print(rule)
	admin_answer = input('\nВыберите правило или введите новое: ')

	return admin_answer

def admin():
	ch = input('\n1.Добавить правила поиска\n2.Назад\n')
	if ch == '2':
		return
	if ch == '1':
		book_genres_check = ['Комедия', 'Драма', 'Ужасы', 'Фэнтези', 'Фантастика',
								 	'Приключения', 'Детектив', 'Поэзия', 'Автобиография', 'Сказка',
								 	'Исторический роман', 'Мифы', 'Магический реализм', 'Легенды',
								 	'Эпос', 'Антиутопия','Постапокалипсис', 'Боевик', 'Эпопея', 'Проза']

		with open('rules.json', encoding='utf-8') as old_json:
			data = json.load(old_json)

		rules_base = data
		# print(data)
		# print(type(data))
		answer = [""]
		start = 1
		while start == 1:
			for genre_check in book_genres_check:
				if list(rules_base.keys()).__contains__(genre_check):
					ch = input(
						"\n1.Добавить элемент списка\n2.Выход\n")
					if ch == '2':
						start = 0
						return
					else:
						# print(rules_base)
						# print(rule)
						print(f'\n{book_genres_check}')
						an_gen = input('Введите жанр: ')
						an = input('Введите элементы списка через запятую: ').split(',')
						print(an)

						rules_base[an_gen] = an

						with open('rules.json', 'w', encoding='utf-8') as new_json:
							json.dump(data, new_json, ensure_ascii=False)

			rule = create_rule(rules_base)
			if rule in rules_base:
				rules_base = rules_base[rule]
			else:
				ch = input("\n1.Добавить правило\n2.Выход, не сохраняя\n3.Выйти и сохранить\n")
				if ch == '2':
					start = 0
				if ch != '2':
					# print( rules_base)
					# print( rule)

					rules_base[rule] = {}

					with open('rules.json', 'w', encoding='utf-8') as new_json:
						json.dump(data, new_json, ensure_ascii=False)
					if ch == '3':
						start = 0

		print(rules_base)

def main():
	while True:
		ch = input("\n1.Пользователь\n2.Администратор\n3.Выход\n")
		if ch == '3':
			return
		elif ch == '1':
			user()
		elif ch == '2':
			admin()
		else:
			print("Выбран несуществующий пункт меню!")

if __name__ == "__main__":
	main()