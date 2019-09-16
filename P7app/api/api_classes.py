import requests

API_KEY = "YOUR_GOOGLE_API_KEY"
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
		for key, val in result.items():
			if key == "formatted_address" or key == "location" or key == "status":
				data.append((key, val))
				print(data)
		return result["location"]["lat"]
		
