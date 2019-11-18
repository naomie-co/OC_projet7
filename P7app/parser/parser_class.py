import string

from .stop_words import STOP_WORDS

class Parser_search:
	"""Enter a sentence and transform it to keep the essential elements to make
	a search """

	def __init__(self, user_sentence):
		self.user_sentence = user_sentence.lower()
		
	def off_punctuation(self):
		"""Remove the punctuation from the sentence passed in object instantiation"""
		for punct in string.punctuation:
			self.user_sentence = self.user_sentence.replace(punct, " ")
		return self.user_sentence


	def filter_parser(self):
		"""Remove the stop words of a sentence passed in object instantiation"""
		final_sentence = []
		for i, word in enumerate(self.user_sentence.split(" ")):
			if word not in STOP_WORDS and word != "":
				final_sentence.append(word)
		return final_sentence
