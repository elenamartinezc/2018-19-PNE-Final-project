import http.server
import socketserver
import json
import http.client
from Seq import Seq
PORT = 8000
HOSTNAME = "rest.ensembl.org"
class TestHandler(http.server.BaseHTTPRequestHandler):
    # We create a function so that we can split the paths in order to get the arguments
    def cutting(self,path):
        fDict = dict()
        if '?' in self.path:
            cut1 = path.split('?')[1]
            cut1 = cut1.split(" ")[0]
            cut2 = cut1.split("&")
            # what we get is the parameter equals to its value so we will create a dictionary making the parameter as the key and the value as the value.
            try:
                for elements in cut2:
                    key = elements.split("=")[0]
                    value = elements.split("=")[1]
                    fDict [key] = value
            except IndexError:
                pass
        return fDict


    def do_GET(self):
        status = 200
        jsonresult = False

        if self.path == '/' or self.path == '/index':
            with open ('index.html', 'r') as f:
                contents = f.read()

# BASIC LEVEL
        #Resource for getting the list of species
        elif '/listSpecies' in self.path:
            try:
                # We cut the path in order to get the value of the limit
                cut = self.cutting(self.path)


                if 'limit' in cut:
                    limit = cut['limit']
                    if limit != 0 and (limit.isdigit() == True):
                        limit = int(cut['limit'])

                    elif (limit.isalpha() == True):
                        status = 404
                        f = open('error.html', 'r')
                        contents = f.read()

                    else:
                        limit = 0
                else:
                    limit=0

                print('The limit is:', limit)
                conn = http.client.HTTPConnection(HOSTNAME)
                #Ask for the list of species
                conn.request("GET","/info/species?content-type=application/json")
                #Wait for the server's response
                r1 = conn.getresponse()
                #Print the status
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                #Read the response's body and close
                text_json = r1.read().decode("utf-8")
                result = json.loads(text_json)
                #We are accesing to the key 'species'
                species = result['species']

                # Now we are going to check if the user has clicked on the json option:
                if 'json' in cut:
                    jsonresult = True
                    list1 = species[1:limit]
                    contents = json.dumps(list1)
                else:   # We are going to send the list to the webpage
                    contents= """
                            <html>
                            <body style="background-color: mistyrose;">
                            <FONT FACE="monospace" COLOR = "deeppink">
            <h1>The list of species is:</h1></FONT>
                            <ol>"""

                    #We create the list by reading the key display_name that it's the one that contains the name of the species
                    counter = 0
                    limit = int(limit)
                    for specie in species:
                        contents=contents+"<li>"+specie['display_name']+"</li>"
                        counter += 1

                        if counter == limit:
                            break

                            contents = contents+"""</ol>
                                    </body>
                                    </html>"""


                    conn.close()

             # In case the user enters a string it will show up and error
            except ValueError:
                status = 404
                f = open('error.html', 'r')
                contents = f.read()
            except KeyError:
                status = 404
                f = open('error.html', 'r')
                contents = f.read()



        elif 'karyotype'in self.path:
            try:
                # By splitting the route we get the specie
                cut = self.cutting(self.path)
                specie = cut['specie']
                if 'specie' in cut and cut['specie'] != "":
                    specie = cut ['specie']
                    print('The specie is:', specie)
                    conn = http.client.HTTPConnection(HOSTNAME)
                    # Ask for the list of species
                    conn.request("GET", "/info/assembly/"+specie+"?content-type=application/json")
                    # Wait for the server's response
                    r1 = conn.getresponse()
                    # Print the status
                    print()
                    print("Response received: ", end='')
                    print(r1.status, r1.reason)
                    # Read the response's body and close
                    text_json = r1.read().decode("utf-8")
                    result = json.loads(text_json)
                    # We are accesing to the key 'karyotype'
                    karyotype = result['karyotype']


                    # Now we are going to check if the user has clicked on the json option:
                    if 'json' in cut:
                        jsonresult = True
                        print(karyotype)
                        contents = json.dumps(karyotype)

                    else:
                        jsonresult = False
                        contents = """
                                <html>
                                <body style="background-color: mistyrose;">
                                <FONT FACE="monospace" COLOR = "deeppink">
                <h1>The karyotype is:</h1></FONT>
                                <ul>"""
                        for gene in karyotype:
                            contents = contents + "<li>" + gene + "</li>"
                        contents = contents + """</ul>
                                            </body>
                                            </html>"""

                else:
                    status = 404
                    f = open('error.html', 'r')
                    contents = f.read()

            except KeyError:
                status = 404
                f = open('error.html', 'r')
                contents = f.read()

        elif '/chromosomeLength' in self.path:
            cut = self.cutting(self.path)
            if ('specie' in cut) and ('chromo' in cut) and (cut['specie'] != "") and (cut['chromo'] != ""):
                numberChromo = cut['chromo']
                print('The chromo is:', numberChromo)
                nameSpecie = cut['specie']
                print('The specie is:', nameSpecie)

                conn = http.client.HTTPConnection(HOSTNAME)
                # Ask for the list of species
                conn.request("GET", "/info/assembly/" + nameSpecie + "?content-type=application/json")
                # Wait for the server's response
                r1 = conn.getresponse()
                # Print the status
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                # Read the response's body and close
                text_json = r1.read().decode("utf-8")
                result = json.loads(text_json)
                # We are accesing to the key 'top_level_region' that tells us the properties of the chromosome: the length, cord_system and name.
                if 'top_level_region' in result:
                    top_level_region = result ['top_level_region']
                    length = 0
                    for element in top_level_region:
                        #We are searching for the chromosome the user has told us
                        if element ['name']==str(numberChromo):
                            length = str(element['length'])

                    # Now we are going to check if the user has clicked on the json option:
                    if 'json' in cut:
                        jsonresult = True
                        contents = json.dumps(length)

                    else:
                        jsonresult = False
                        contents = """
                                <html>
                                <body style="background-color: mistyrose;">
                                <FONT FACE="monospace" COLOR = "deeppink"><h1>The length of the chromosome is:</h1></FONT>
                                <ul>"""
                        contents = contents + "<li>" + str(length) + "</li>"
                        contents = contents + """</ul>
                                </body>
                                </html>"""
                else:
                    status = 404
                    f = open('error.html', 'r')
                    contents = f.read()

            else:
                status = 404
                f = open('error.html', 'r')
                contents = f.read()

#MEDIUM LEVEL
        elif '/geneSeq' in self.path:
            try:# We have to get the ID associated to the gene the user has entered (The database works with IDs, not names)
                cut = self.cutting(self.path)
                gene = cut['gene']
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request("GET", "/homology/symbol/human/" +gene+ "?content-type=application/json")
                # Wait for the server's response
                r1 = conn.getresponse()
                # Print the status
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                # Read the response's body and close
                text_json = r1.read().decode("utf-8")
                result = json.loads(text_json)
                ID = result ['data'][0]['id']

                conn.request("GET", "/sequence/id/" + ID + "?content-type=application/json")
                # Wait for the server's response
                r1 = conn.getresponse()
                # Print the status
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                # Read the response's body and close
                text_json = r1.read().decode("utf-8")
                result = json.loads(text_json)
                seq = result['seq']

                # Now we are going to check if the user has clicked on the json option:
                if 'json' in cut:
                    jsonresult = True
                    contents = json.dumps(seq)

                else:
                    jsonresult = False
                    contents = """
                                    <html>
                                    <body style="background-color: mistyrose;">
                                    <FONT FACE="monospace" COLOR = "deeppink"><h1>The sequence of the human chromosome:</h1></FONT>
                                    <ul>"""
                    contents = contents + "<li>" + seq + "</li>"
                    """</ul>
                    </body>
                    </html>"""

            except KeyError:
                status = 404
                f = open('error.html', 'r')
                contents = f.read()

        elif '/geneInfo' in self.path:
            try:
                # We have to get the ID associated to the gene the user has entered (The database works with IDs, not names)
                cut = self.cutting(self.path)
                gene = cut ['gene']
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
                # Wait for the server's response
                r1 = conn.getresponse()
                # Print the status
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                # Read the response's body and close
                text_json = r1.read().decode("utf-8")
                result = json.loads(text_json)
                ID = result['data'][0]['id']

                conn.request("GET", "/overlap/id/" + ID + "?feature=gene;content-type=application/json")
                # Wait for the server's response
                r1 = conn.getresponse()
                # Print the status
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                # Read the response's body and close
                text_json = r1.read().decode("utf-8")
                result = json.loads(text_json)
                start = result[0]['start']
                end = result[0]['end']
                # We cannot have the length directly so we'll calculate it by substracting end minus start
                length = end-start+1
                # We add 1 because the end and the start are included
                chromo = result[0]['seq_region_name']

                # Now we are going to check if the user has clicked on the json option:
                if 'json' in cut:
                    jsonresult = True
                    dict1 = {'Start': start, 'End': end, "Length": length, "Chromo": chromo}
                    contents = json.dumps(dict1)


                else:
                    jsonresult = False
                    contents = """
                                                <html>
                                                <body style="background-color: mistyrose;">
                                                <FONT FACE="monospace" COLOR = "deeppink"><h1>The parameters of the gene introduced:</h1></FONT>
                                                <ul>"""
                    contents = contents + "<li>" + "<h4> ID: </h4>" + ID + "</li>"
                    contents = contents + "<li>" + "<h4> Start: </h4>" + str(start) + "</li>"
                    contents = contents + "<li>" + "<h4> End: </h4>" + str(end) + "</li>"
                    contents = contents + "<li>" + "<h4> Length: </h4>" + str(length) + "</li>"
                    contents = contents + "<li>" + "<h4> Chromosome: </h4>" + chromo + "</li>"
                    """</ul>
                    </body>
                    </html>"""

            except KeyError:
                status = 404
                f = open('error.html', 'r')
                contents = f.read()


        elif '/geneCalc' in self.path:
            try:
                # We have to get the ID associated to the gene the user has entered (The database works with IDs, not names)
                cut = self.cutting(self.path)
                gene = cut['gene']
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
                # Wait for the server's response
                r1 = conn.getresponse()
                # Print the status
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                # Read the response's body and close
                text_json = r1.read().decode("utf-8")
                result = json.loads(text_json)
                ID = result['data'][0]['id']

                conn.request("GET", "/sequence/id/" + ID + "?content-type=application/json")
                # Wait for the server's response
                r1 = conn.getresponse()
                # Print the status
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                # Read the response's body and close
                text_json = r1.read().decode("utf-8")
                result = json.loads(text_json)
                seq = result['seq']

                # We create the object Seq
                seq1 = Seq(seq)

                # Now we are going to check if the user has clicked on the json option:
                if 'json' in cut:
                    jsonresult = True
                    length = str(len(seq))
                    perA = seq1.perc('A')
                    perC = seq1.perc('C')
                    perG = seq1.perc('G')
                    percT = seq1.perc('T')
                    dict1 = {"Length": length, "PercA": perA, "PerC": perC, "PercG": perG, "PercT": percT}
                    contents = json.dumps(dict1)
                    # ERROR

                else:
                    jsonresult = False
                    contents = """
                                                            <html>
                                                            <body style="background-color: mistyrose;">
                                                            <FONT FACE="monospace" COLOR = "deeppink"><h1>The calculations of the gene introduced:</h1></FONT>
                                                            <ul>"""
                    contents = contents + "<li>" + "<h4> Length: </h4>" + str(len(seq)) + "</li>"
                    contents = contents + "<li>" + "<h4> Percentage of As: </h4>" + str(seq1.perc('A')) +'%' + "</li>"
                    contents = contents + "<li>" + "<h4> Percentage of Cs: </h4>" + str(seq1.perc('C')) +'%' + "</li>"
                    contents = contents + "<li>" + "<h4> Percentage of Gs: </h4>" + str(seq1.perc('G')) +'%' + "</li>"
                    contents = contents + "<li>" + "<h4> Percentage of Ts: </h4>" + str(seq1.perc('T')) +'%' + "</li>"
                    """</ul>
                    </body>
                    </html>"""

            except KeyError:
                status = 404
                f = open('error.html', 'r')
                contents = f.read()


        elif '/geneList' in self.path:
            try:
                cut = self.cutting(self.path)
                numberStart = cut['start']
                print('The start is:', numberStart)
                nameChromo = cut['chromo']
                print('The chromo is:', nameChromo)
                numberEnd = cut['end']
                print('The end is:', numberEnd)
                conn = http.client.HTTPConnection(HOSTNAME)
                conn.request("GET", "/overlap/region/human/" + str(nameChromo) + ":" + str(numberStart) + "-" + str(
                    numberEnd) + "?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon")
                r1 = conn.getresponse()
                # Print the status
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                # Read the response's body and close
                text_json = r1.read().decode("utf-8")
                result = json.loads(text_json)

                if 'json' in cut:
                    jsonresult = True
                    contents = json.dumps(result)

                else:
                    jsonresult = False
                    contents = """
                                                                                   <html>
                                                                                   <body style="background-color: mistyrose;">
                                                                                   <FONT FACE="monospace" COLOR = "deeppink"><h1>The calculations of the gene introduced:</h1></FONT>
                                                                                   <ul>"""
                    for element in result:
                        if element['feature_type'] == "gene": # We are doing this in order to put only genes
                            contents = contents + "<li>" + (
                                        element['id'] ) + "</li>"
                    """</ul>
                                </body>
                                </html>"""

            # TypeError occurs when the user does not enter an integer
            except TypeError:
                status = 404
                f = open('error.html', 'r')
                contents = f.read()



        else:
            with open('error.html', 'r') as f:
                contents = f.read()

        self.send_response(status)



        if jsonresult:
            self.send_header('Content-Type', 'application/json')
        else:
            self.send_header('Content-Type', 'text/html')


        self.send_header('Content-Length', len(str.encode(contents)))

        self.end_headers()

        self.wfile.write(str.encode(contents))

        return


Handler = TestHandler
socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)


    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()

print("")
print("Server Stopped")