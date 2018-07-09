#!/bin/python3

import http.client
import urllib.parse
import ssl

username = ""
password = ""

#h1 = http.client.HTTPSConnection("localhost", 8080, context=ssl._create_unverified_context())
#h1.set_tunnel("sandhills.mrooms3.net")
h1 = http.client.HTTPSConnection("sandhills.mrooms3.net")
h1.request("GET", "/login/index.php")
r1 = h1.getresponse()

samlreq = ''
heads = r1.getheaders()
#print(heads)
data = r1.read()
data = list(data)
moodleSessList = list(heads[3])
moodleSessList = list(moodleSessList[1])
moodleSess = ''
i = 0
while moodleSessList[i] != ";":
    moodleSess += moodleSessList[i]
    i += 1

samlSessList = list(heads[7])
samlSessList = list(samlSessList[1])
samlSess = ''
i = 0
while samlSessList[i] != ";":
    samlSess += samlSessList[i]
    i += 1

i = 0
while i < len(data):
    data[i] = chr(data[i])
    i += 1

i = 0

while i < len(data):
    if data[i] == "S":
        if data[i + 1] == "A":
            if data[i + 2] == "M":
                if data[i + 3] == "L":
                    if data[i + 4] == "R":
                        if data[i + 5] == "e":
                            j = i + 20
                            while data[j] != "\"":
                                samlreq += data[j]
                                j += 1
    i += 1

samlreq = "SAMLRequest=" + urllib.parse.quote_plus(samlreq)
samlreq += "&RelayState=https%3A%2F%2Fsandhills.mrooms3.net%2Fauth%2Fsaml2%2Flogin.php"

#h2 = http.client.HTTPConnection("localhost", 12345)
#h2 = http.client.HTTPSConnection("localhost", 8080, context=ssl._create_unverified_context())
#h2.set_tunnel("sccidp.sandhills.edu")
h2 = http.client.HTTPSConnection("sccidp.sandhills.edu")
h2.putrequest("POST", "/idp/profile/SAML2/POST/SSO")
h2.putheader('Content-Type', "application/x-www-form-urlencoded")
h2.putheader("Content-Length", str(len(samlreq)))
h2.endheaders()
h2.send(samlreq.encode())
r2 = h2.getresponse()
heads = r2.getheaders()
data = r2.read()

location = ""
locationList = list(str(heads[2]))
i = 14

while locationList[i] != "'":
    location += locationList[i]
    i+=1
#print(location)
i = 11
jsession = ""
jsessionlist = list(heads[0])
jsessionlist = list(str(jsessionlist[1]))

while jsessionlist[i] != ";":
    jsession += jsessionlist[i]
    i +=1

#print(jsession)
endOfURL = ''
i = len(location)  - 15
while i < (len(locationList) - 2):
    endOfURL += locationList[i]
    i += 1
#this is laziness
urllist = endOfURL.split("?")
endOfURL = urllist[1]
#h3 = http.client.HTTPSConnection("localhost", 8080, context=ssl._create_unverified_context())
#h3.set_tunnel("sccidp.sandhills.edu")
h3 = http.client.HTTPSConnection("sccidp.sandhills.edu")
h3.putrequest("GET", "/idp/profile/SAML2/POST/SSO?" + endOfURL)
h3.putheader('Cookie', "JSESSIONID=" + jsession)
h3.endheaders()
r3 = h3.getresponse()
data = r3.read()
#print(data)
#print("\n*****\n")

password = urllib.parse.quote_plus(password)
content = "donotcache=1&j_username=" + username + "&j_password=" + password + "&_eventId_proceed="

#h4 = http.client.HTTPSConnection("localhost", 8080, context=ssl._create_unverified_context())
#h4.set_tunnel("sccidp.sandhills.edu")
h4 = http.client.HTTPSConnection("sccidp.sandhills.edu")
h4.putrequest("POST", "/idp/profile/SAML2/POST/SSO?" + endOfURL)
h4.putheader('Content-Length', str(len(content)))
h4.putheader('Content-Type', "application/x-www-form-urlencoded")
h4.putheader('Referer', "https://sccidp.sandhills.edu/idp/profile/SAML2/POST/SSO?" + endOfURL)
h4.putheader('Cookie', 'JSESSIONID=' + jsession)
h4.endheaders()
h4.send(content.encode())
r4 = h4.getresponse()
data = r4.read()

#print(data)
#print("\n*********\n")
data = list(data)
i = 0 

while i < len(data):
    data[i] = chr(data[i])
    i += 1

i = 0
samlreq2 = ""
while i < len(data):
    if data[i] == "S":
        #print("in the first if")
        if data[i + 1] == "A":
            if data[i + 2] == "M":
                if data[i + 3] == "L":
                    if data[i + 4] == "R":
                        if data[i + 5] == "e":
                            #print("in the last if")
                            j = i + 21
                            while data[j] != "\"":
                                samlreq2 += data[j]
                                j += 1
    i += 1

samlreq2 = urllib.parse.quote_plus(samlreq2)
content = "RelayState=https%3A%2F%2Fsandhills.mrooms3.net%2Fauth%2Fsaml2%2Flogin.php&SAMLResponse=" + samlreq2

#h5 = http.client.HTTPSConnection("localhost", 8080, context=ssl._create_unverified_context())
#h5.set_tunnel("sandhills.mrooms3.net")
h5 = http.client.HTTPSConnection("sandhills.mrooms3.net")
h5.putrequest("POST", "/auth/saml2/sp/saml2-acs.php/sandhills.mrooms3.net")
h5.putheader('Content-Length', str(len(content)))
h5.putheader('Content-Type', "application/x-www-form-urlencoded")
h5.putheader('Referer', "https://sccidp.sandhills.edu/idp/profile/SAML2/POST/SSO?" + endOfURL)
h5.putheader('Cookie', moodleSess + "; " + samlSess)
h5.endheaders()
h5.send(content.encode())
r5 = h5.getresponse()
heads = r5.getheaders()
#print(heads)
data = r5.read()
#moodleSessList = list(heads[3])
#moodleSessList = list
samlAuthList = list(heads[6])
samlAuthList = list(samlAuthList[1])
samlAuth = ''
i = 0
while samlAuthList[i] != ";":
    samlAuth += samlAuthList[i]
    i += 1

h6 = http.client.HTTPSConnection("sandhills.mrooms3.net")
#h6 = http.client.HTTPSConnection("localhost", 8080, context=ssl._create_unverified_context())
#h6.set_tunnel("sandhills.mrooms3.net")
h6.putrequest("GET", "/login/index.php")
h6.putheader('Referer', "https://sccidp.sandhills.edu/idp/profile/SAML2/POST/SSO?" + endOfURL)
h6.putheader('Cookie', moodleSess + "; " + samlSess + "; " + samlAuth)
h6.endheaders()
r6 = h6.getresponse()
data = r6.read()
heads = r6.getheaders()

moodleSessList = list(heads[6])
moodleSessList = list(moodleSessList[1])
i = 0
moodleSess = ''
while moodleSessList[i] != ";":
    moodleSess += moodleSessList[i]
    i += 1
moodleIdList = list(heads[8])
moodleIdList = list(moodleIdList[1])
moodleId = ""
i = 0
while moodleIdList[i] != ";":
    moodleId += moodleIdList[i]
    i += 1
#h7 = http.client.HTTPSConnection("localhost", 8080, context=ssl._create_unverified_context())
#h7.set_tunnel("sandhills.mrooms3.net")
h7 = http.client.HTTPSConnection("sandhills.mrooms3.net")
h7.putrequest("GET", "/")
h7.putheader('Referer', "https://sccidp.sandhills.edu/idp/profile/SAML2/POST/SSO?" + endOfURL)
h7.putheader('Cookie', samlSess + ": " + samlAuth + "; " + moodleSess + "; " + moodleId)
h7.endheaders()
r7 = h7.getresponse()
data = r7.read()

h8 = http.client.HTTPSConnection("sandhills.mrooms3.net")
#h8 = http.client.HTTPSConnection("localhost", 8080, context=ssl._create_unverified_context())
#h8.set_tunnel("sandhills.mrooms3.net")
h8.putrequest("GET", "/calendar/view.php?view=month")
h8.putheader('Cookie', samlSess + ": " + samlAuth + "; " + moodleSess + "; " + moodleId)
h8.endheaders()
r8 = h8.getresponse()
data = r8 .read()
#print(data)

data = list(data)

i = 0
while i < len(data):
    data[i] = chr(data[i])
    i += 1

day = 0
i = 0
msg = ''

while i < len(data) - 1:
    try:
        if (((data[i]) + (data[i + 1]) + (data[i + 2]) + (data[i + 3]) + (data[i + 4]) + (data[i + 5]) + (data[i + 6]) + (data[i + 7]) + (data[i + 8]) + (data[i + 9]) + (data[i + 10]) + (data[i + 11])) == "day nottoday") or (((data[i]) + (data[i + 1]) + (data[i + 2]) + (data[i + 3]) + (data[i + 4]) + (data[i + 5]) + (data[i + 6]) + (data[i + 7]) + (data[i + 8])) == "day today"):
            day += 1
            print("Day " + str(day))
            i += 1
            while (((data[i]) + (data[i + 1]) + (data[i + 2]) + (data[i + 3]) + (data[i + 4]) + (data[i + 5]) + (data[i + 6]) + (data[i + 7]) + (data[i + 8]) + (data[i + 9]) + (data[i + 10]) + (data[i + 11])) != "day nottoday") and (((data[i]) + (data[i + 1]) + (data[i + 2]) + (data[i + 3]) + (data[i + 4]) + (data[i + 5]) + (data[i + 6]) + (data[i + 7]) + (data[i + 8])) != "day today"):
                if ((data[i]) + (data[i + 1]) + (data[i + 2]) + (data[i + 3]) + (data[i + 4]) + (data[i + 5]) + (data[i + 6]) + (data[i + 7]) + (data[i + 8]) + (data[i + 9]) + (data[i + 10]) + (data[i + 11]) + (data[i + 12]) + (data[i + 13]) + (data[i + 14]) + (data[i + 15]) + (data[i + 16]) + (data[i + 17]) + (data[i + 18]) + (data[i + 19]) + (data[i + 20])) == "calendar_event_course":
                    count = 0
                    while count < 2:
                        if data[i] == ">":
                            count += 1
                        i += 1
                    msg = ''
                    while data[i] != "<":
                        msg += data[i]
                        i += 1
                    #bug needs fixing
                    if len(msg) > 2:
                        print("\t" + msg)
                else:
                    i += 1
        else:
            i +=1
    except IndexError:
        break;

