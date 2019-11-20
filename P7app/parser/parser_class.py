import string

from .stop_words import STOP_WORDS

class Parser_search:
	"""Enter a sentence and transform it to keep the essential words for a 
	futur request a search """

	def __init__(self, user_sentence):
		self.user_sentence = user_sentence.lower()
		
	def off_punctuation(self):
		"""Remove the punctuation from the sentence passed in object instantiation"""
		for punct in string.punctuation:
			self.user_sentence = self.user_sentence.replace(punct, " ")
		#return self.user_sentence


	def filter_parser(self):
		"""Remove the stop words of a sentence passed in object instantiation"""
		sentence = []
		for i, word in enumerate(self.user_sentence.split(" ")):
			if word not in STOP_WORDS and word != "":
				sentence.append(word)
				final_sentence = " ".join(sentence)
				self.user_sentence = final_sentence
		#return self.user_sentence

	def focus_search(self):
		"""Method to get the essential words for a futur request"""
		self.off_punctuation()
		self.filter_parser()
		return self.user_sentence