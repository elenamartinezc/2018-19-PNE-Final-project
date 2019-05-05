import http.client
import json

PORT = 8000
SERVER = 'localhost'

print("\nConnecting to server: {}:{}\n".format(SERVER, PORT))

# Connect with the server
conn = http.client.HTTPConnection(SERVER, PORT)

# Send the request mesage using the GET method
conn.request("GET", "/listSpecies?limit=10&json=1")
r1 = conn.getresponse()
print("/listSpecies:")
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)

conn.request("GET", "/karyotype?specie=mouse&json=1")
r1 = conn.getresponse()
print("/karyotype ")
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)

conn.request("GET", "/chromosomeLength?specie=mouse&chromo=18&json=1")
r1 = conn.getresponse()
data1 = r1.read().decode("utf-8")
print("/chromosomeLength ")
response = json.loads(data1)
print (response)

conn.request("GET", "/geneSeq?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("/geneSeq")
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)

conn.request("GET", "/geneInfo?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("/geneInfo:")
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)

conn.request("GET", "/geneCalc?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("/geneCalc:")
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)


conn.request("GET", "/geneList?chromo=1&start=0&end=30000&json=1")
r1 = conn.getresponse()
print("/geneList:")
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)