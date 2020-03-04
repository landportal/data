import requests
import time

url = 'https://landgov.donorplatform.org/ajax/map/get-programs-details'
resp = requests.get(url=url)
data = resp.json() # Check the JSON Response Content documentation below

timestr = time.strftime("%Y%m%d-%H%M%S")
filename_output = timestr+"-get-programs-details.txt"

with open(filename_output, 'w') as file:
    file.write(data["html"].encode('utf8'))

with open("programs-details.txt", 'w') as file:
    file.write(data["html"].encode('utf8'))