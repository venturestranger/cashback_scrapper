import nltk
from bs4 import BeautifulSoup
from textdistance import jaro_winkler
from presets import cards, objectives
from utils import AhoCorasick
from nltk.tokenize import word_tokenize
import numpy as np


class ContentRetriever:
	# initialize Aho-Corasick algorithm for string matching
	def __init__(self):
		self.tree = AhoCorasick()
		for card_name in cards:
			self.tree.add_pattern(card_name.lower())

		self.tree.create_fail_links()

	@staticmethod
	def string_similarity(s1, s2):
		return jaro_winkler(s1, s2)

	# retrieve information about available cashback from a given web-page element
	def retrieve_info_from_element(self, el):
		foll = []
		prev = []
		
		cur = el.parent
		for i in range(4):
			try:
				foll.append(cur.get_text())
				cur = cur.next_element
			except:
				pass

		cur = el.parent
		for i in range(4):
			try:
				prev.append(cur.get_text())
				cur = cur.previous_element
			except:
				pass
		
		return '. '.join(prev[::-1]) + '. ' + '. '.join(foll)

	# retrieve a type of a credit card from a given web-page element
	def retrieve_card_from_element(self, el):
		cards = self.tree.match_words(el.get_text().lower())
		
		try:
			ret = cards[0]

			for i in range(1, len(cards)):
				if cards[i].startswith(cards[i - 1]):
					ret = cards[i]
				else:
					break
		except:
			return None
		else:
			return ret

	# retrieve cashback percent cashback from a given web-page element
	def retrieve_percent_from_element(self, el):
		data = el.get_text().lower().translate({ord(i): None for i in 'йцукенгшщзхъфывапролджэячсмитьбюqwertyuiopasdfghjlkzxcvbnm/\'";][{}+=_-)(*&^%$#@!'})

		for i in data.split():
			if i.replace(',', '0').isdigit() and len(i.replace(',', '.').split('.')[-1]) < 3 and i != '0':
				return i + '%'
		return None

	# retrieve a type of good that cashback is given for from a given web-page element
	def retrieve_objective_from_text(self, text):
		rank = np.zeros(len(objectives))
		context_match = np.zeros(len(objectives))

		text = word_tokenize(text.lower())
		text = [i for i in text if i not in ',./\'"']

		for i in range(len(text)):
			for j in range(len(objectives)):
				for target in objectives[j]:
					sim = self.string_similarity(' '.join(text[i:i+len(target.split())]), target)
					rank[j] = max(rank[j], sim)
					context_match[j] += (sim > 0.7)
		
		if np.max(rank) < 0.7:
			return None
		else:
			return np.argmax(rank)
