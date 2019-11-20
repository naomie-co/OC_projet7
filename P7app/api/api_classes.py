import requests



API_KEY = "AIzaSyDDyWtczDEZ7MtHtNXVdXcWb7TjFEusJF0"

class GoogleMapsApi:
	def __init__(self, place):
		self.place = place
		self.url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"

	def request(self):
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
			data = ['Paris, France', 48.856614, 2.3522219, 'OK']
			print("KeyError. Résultat par défault!")
		except IndexError:
			data = ['Paris, France', 48.856614, 2.3522219, 'OK']
			print("IndexError. Résultat par défault!")
		return data


class WikiGlobal:
	"""To set up the WikiApi class"""
	def __init__(self):
		self.api_url = "http://en.wikipedia.org/w/api.php" #Default language in english

	def language(self, lang="fr"):
		"""Set up the language of the requests"""
		self.api_url = "http://" + lang.lower() + ".wikipedia.org/w/api.php"
		

	def w_request(self, params):
		"""Make a request on wikipedia's API"""
		data = requests.get(self.api_url, params=params)
		return data.json()

	def w_geosearch(self, latitude, longitude, title=None, results=10, radius=1000):
		geosearch_params = {
		'list': 'geosearch',
		'gsradius': radius,
		'gscoord': '{0}|{1}'.format(latitude, longitude),
		'gslimit': results,
		'format': 'json',
		'action': 'query',
		}
		if title:
			geosearch_params['titles'] = title

		data_result = self.w_request(geosearch_params)
		search_pages = data_result['query'].get('pages', None)
		if search_pages:
			search_results = [v['title'] for k, v in search_pages.items() if k != '-1']
		else:
			search_results = [d['title'] for d in data_result['query']['geosearch']]

		return search_results

	def wiki_summary(self, title, sentence=0, char=0):
		params = {
			'prop': 'extracts',
			'explaintext': '',
			'titles': title,
			'format': 'json',
			'action': 'query',
		}

		if sentence:
			params['exsentences'] = sentence
		elif char:
			params['exchars'] = char
		else:
			params['exintro'] = ''

		request = self.w_request(params)
		summary = request['query']['pages']
		for k, v in summary.items():
			result = v['extract']

		return result

	def get_coordinate(self, title):
		params = {
			"action": "query",
			"format": "json",
			"titles": title,
			"prop": "coordinates"
		}
		request = self.w_request(params)
		pages = request['query']['pages']
		for k, v in pages.items():
			print("Latitute: " + str(v['coordinates'][0]['lat']))
			print("Longitude: " + str(v['coordinates'][0]['lon']))




class WikiApi:
	def __init__(self, latitude, longitude, title):
		self.latitude = latitude
		self.longitude = longitude
		self.title = title

	def wiki_request(self):
		r = WikiGlobal()
		r.language("fr")
		data = r.w_geosearch(self.latitude, self.longitude, 
		title=self.title, results=1, radius=(1000))
		result = r.wiki_summary(data[0], sentence=0, char=0)
		return result

	def wiki_coordinates(self):
		r = WikiGlobal()
		r.language("fr")
		result = r.get_coordinate(self.title)
		return result

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
