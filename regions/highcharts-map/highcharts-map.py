import urllib, json
url = "https://raw.githubusercontent.com/landportal/js-view-coda/master/js/map_data.js"
response = urllib.urlopen(url)
html=response.read()
html=html.replace('map_data =','')
html=html.replace(';','')
#print html[:10]
#print html[-10:]
data = json.loads(html)
#print data
for country in data:
   print country["id"].encode('utf-8') + ',' +  "\"" + country["name"].encode('utf-8') + "\""
