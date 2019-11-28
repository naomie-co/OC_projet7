import requests
import os



API_KEY = os.getenv("API_KEY")

class GoogleMapsApi:
	"""GoogleMpasApi class allows to interact with the google maps API. 
	It needs a API_KEY.
	Initiate the class with a place key-word and call the request method to find:
		-an address
		-GPS coordinates
		-verify the status code
	"""
	def __init__(self, place):
		self.place = place
		#API's request link
		self.url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

	def request(self):
		"""Method to find an address, the GPS coordinates, and to verify the status code of the self.place instantiation variable
		Return a list"""
		parameters = {
			"query": self.place,
			"inputtype": "textquery",
			"key": API_KEY
		}
		request = requests.get(self.url, params=parameters)
		result = request.json()
		data = []
		try:
			data.append(result["results"][0]["formatted_address"])
			data.append(result["results"][0]["geometry"]["location"]["lat"])
			data.append(result["results"][0]["geometry"]["location"]["lng"])
			data.append(result["status"])
		except KeyError:
			#Default values in case of KeyError
			data = ['Paris, France', 48.856614, 2.3522219, 'OK']
			print("KeyError. Résultat par défault!")
		except IndexError:
			#Default values in case of IndexError
			data = ['Paris, France', 48.856614, 2.3522219, 'OK']
			print("IndexError. Résultat par défault!")
		print(data)
		return data


class WikiGlobal:
	"""Class to configure wikipedia queries so its can be used in the WikiApi class"""
	def __init__(self):
		#API's request link
		self.api_url = "http://en.wikipedia.org/w/api.php" #Default language in english

	def language(self, lang="fr"):
		"""Set up the request language"""
		self.api_url = "http://" + lang.lower() + ".wikipedia.org/w/api.php"
		

	def w_request(self, params):
		"""Send a request to the wikipedia API with the arguments passed in parameters"""
		data = requests.get(self.api_url, params=params)
		return data.json()

	def w_geosearch(self, latitude, longitude, title=None, results=1, radius=1000):
		geosearch_params = {
		'list': 'geosearch',
		'gsradius': radius,
		'gscoord': '{0}|{1}'.format(latitude, longitude),
		'gslimit': results,
		'format': 'json',
		'action': 'query',
		'titles': title,
		}

		data_result = self.w_request(geosearch_params)
		search_pages = data_result['query'].get('pages', None)
		if search_pages:
			search_results = [v['title'] for k, v in search_pages.items() if k != '-1']
		else:
			geosearch_params["titles"] = "None"
			data_result = self.w_request(geosearch_params)
			search_pages = data_result['query'].get('pages', None)
			if search_pages:
				search_results = [v['title'] for k, v in search_pages.items() if k != '-1']

			#search_results = [d['title'] for d in data_result['query']['geosearch']]
		return search_results

	def wiki_summary(self, title, char=550):
		"""Get the article summary and the link to the wikipedia page"""
		params = {
			'prop': 'extracts',
			'explaintext': '',
			'titles': title,
			'format': 'json',
			'action': 'query',
		}

		if char:
			params['exchars'] = char
		else:
			params['exintro'] = ''

		request = self.w_request(params)
		summary = request['query']['pages']
		for k, v in summary.items():
			try:
				result = [v['extract'], "https://fr.wikipedia.org/wiki?curid=" + str(v['pageid'])]
			except KeyError:
				result = ["T'as recherche est folle! Je n'ai pas d'anecdote sur ce lieu. J'en perds mon latin... tu peux cliquer sur le lien pour en savoir plus sur Paris!", "https://fr.wikipedia.org/wiki?curid=681159" ]
		return result

	def get_coordinate(self, title):
		"""Find the GPS coordinates linked to the page search in parameters"""
		params = {
			"action": "query",
			"format": "json",
			"titles": title,
			"prop": "coordinates"
		}
		request = self.w_request(params)
		pages = request['query']['pages']
		for k, v in pages.items():
			try:
				w_coordinates = ((v['coordinates'][0]['lat']), (v['coordinates'][0]['lon']))
			except KeyError:
				print ("get_coordinate KeyError!")
				continue
			return w_coordinates




class WikiApi:
	def __init__(self, g_latitude, g_longitude, title):
		self.g_latitude = g_latitude
		self.g_longitude = g_longitude
		self.title = title
		self.w_latitude = 0
		self.w_longitude = 0

	def wiki_geo_request(self):
		"""Use this method to find a wikipedia summary, with GPS coordinates
		self.w_latitude and self.w_longitude souldn't be equal to 0"""
		r = WikiGlobal()
		r.language("fr")
		data = r.w_geosearch(self.w_latitude, self.w_longitude, 
		title=self.title, results=1, radius=(1000))
		print( "in wiki_request", data)
		try:
			result = r.wiki_summary(data[0], char=550) #char=550 to reduce the summary
		except IndexError:
			result = "T'as recherche est folle! Je n'ai pas d'anecdote sur ce lieu. J'en perds mon latin..."
		return result
	def wiki_summary_request(self):
		"""Use this method to find a wikipedia summary, witout GPS coordinates"""
		r = WikiGlobal()
		r.language("fr")
		try:
			result = r.wiki_summary(self.title, char=550)
		except IndexError:
			result = "T'as recherche est folle! Je n'ai pas d'anecdote sur ce lieu. J'en perds mon latin..."
		return result

	def wiki_coordinates(self):
		r = WikiGlobal()
		r.language("fr")
		result = r.get_coordinate(self.title)
		print(result)
		if result != None:
			self.w_latitude = result[0]
			self.w_longitude = result[1]
			return True

	def compare_coordinates(self):
		"""Compare google and wikipedia gps coordinates for a given search. If the difference is smaller than X%, 
		the wikipedia page search is launch"""
		g_lat = self.g_latitude
		g_long = self.g_longitude
		w_lat = self.w_latitude
		w_long = self.w_longitude
		if ((g_lat - w_lat)/w_lat)*100 > 10 or ((g_long - w_long)/w_long)*100 > 10:
			print("trop grande difference")
			self.w_latitude = 0
			self.w_longitude = 0
			return False

#Paris = 48.856614, 2.3522219
#Lyon = 45.764942, 4.898393 
"""
if __name__ == "__main__":
	search = "Lyon"
	test = GoogleMapsApi(search)
	r_google = test.request() 
	print(r_google)
	w_request = WikiApi(r_google[1], r_google[2], search)
	r = w_request.wiki_request()
	print(r)
"""
