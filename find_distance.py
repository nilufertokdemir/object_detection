import urllib.request
import json

bingMapsKey = "Ajlc9FeCH2OGYiNdqYQAZAdHkuEVx61ZrNvNzM2SA8ksjTyKdzJwuyItDffHsW0U"

longitude = -122.019943
latitude = 37.285989
destination = "1427 Alderbrook Ln San Jose CA 95129"

encodedDest = urllib.parse.quote(destination, safe='')

routeUrl = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + str(latitude) + "," + str(longitude) + "&wp.1=" + encodedDest + "&key=" + bingMapsKey + "&optmz=time"

request = urllib.request.Request(routeUrl)
response = urllib.request.urlopen(request)

r = response.read().decode(encoding="utf-8")
result = json.loads(r)

itineraryItems = result["resourceSets"][0]["resources"][0]["travelDistance"]

print(itineraryItems)