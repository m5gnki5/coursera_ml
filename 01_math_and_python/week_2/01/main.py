"""
Задание просит найти два предложения из файла, ближайшие по синтаксису
к первому. Близость определяется как минимальное косинусное расстояние.
"""
import re
import numpy as np
from scipy.spatial.distance import cosine


def read_and_tokenize_file(path:str) ->list:
	# считать каждую строку файла и привести содержимое к нижнему регистру
	with open(path) as f:
		sentences = f.read().lower().split("\n")

	# токенизировать 
	tok_sentences = [re.split('[^a-z]', sen) for sen in sentences if sen]

	# оставить только не-пустые строки
	for ts in tok_sentences:
		ts[:] = [t for t in ts if t]
	return tok_sentences


def find_cos_distance(matrix:np.ndarray, n:int) ->str:
	# найти косинусное расстояние первой строки матрицы до всех остальных
	dist = []
	for i in range(1,len(matrix)):
		dist.append((i, cosine(matrix[0], matrix[i])))

	# отсортировать значения по расстоянию
	dist.sort(key=lambda d:d[1])

	# найти n индексов
	ans = []
	for i in range(n):
		ans.append(str(dist[i][0]))
	ans = " ".join(ans)
	return ans


def find_n_closest_sentences(path:str, n:int):
	tok_sentences = read_and_tokenize_file(path)

	# посчитать частоту уникальных слов
	word_count = {}
	for ts in tok_sentences:
		for w in ts:
			if w not in word_count:
				word_count[w] = 0
			word_count[w] += 1

	# все уникальные токены одним списком
	unique_words = [x for x in word_count.keys()]

	# индексировать уникальные токены в виде словаря
	indexed_tokens = {x:unique_words[x] for x in range(len(word_count))}

	# создать матрицу упоминаемости слов (строки) в предложениях (столбцы)
	n_d = np.zeros((len(tok_sentences), len(unique_words)), dtype=int)
	for row in range(len(tok_sentences)):
		for col in range(len(indexed_tokens)):
			if indexed_tokens[col] in tok_sentences[row]:
				n_d[row,col] += 1

	ans = find_cos_distance(n_d, n)

	# записать ответ в файл
	with open("submission-1.txt", "w+") as s:
		s.write(ans)


# find_n_closest_sentences("sentences.txt", 2)
