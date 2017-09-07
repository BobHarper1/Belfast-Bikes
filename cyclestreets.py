import requests
import json
import time
import ast
from requests.auth import HTTPBasicAuth

url = "http://www.cyclestreets.net/api/journey.json?"
key = "cbdaf0c08a59d194"
mode = 'balanced'

stationCoords = ["-5.9308289,54.5971826","-5.9240327,54.5982034","-5.922009,54.6014465","-5.9164541,54.5953307","-5.9236798,54.5952546","-5.9255467,54.5921715","-5.9211082,54.5972712","-5.933532,54.5893166","-5.9331231,54.5948186","-5.9343639,54.5934652","-5.9298436,54.5993582","-5.9333409,54.6021241","-5.92928,54.6036469","-5.932833,54.6049929","-5.9255068,54.602433","-5.9282212,54.6007847","-5.9315184,54.5926926","-5.9348201,54.5974308","-5.9363085,54.5997012","-5.9172403,54.6039495","-5.9215345,54.6049485","-5.9274273,54.5947014","-5.9355202,54.5881623","-5.9313084,54.6013191","-5.9258501,54.6014233","-5.9226342,54.5912531","-5.9298788,54.5958433","-5.9276633,54.597573","-5.9193029,54.5953696","-5.9297209,54.6026064","-5.9112898,54.6057386","-5.9367269,54.5843803","-5.9328105,54.5839495","-5.9399419,54.5865476","-5.9584722,54.5899034","-5.9410258,54.6085425","-5.9444044,54.6036798","-5.9490879,54.5953157","-5.9475845,54.5994268","-5.942153,54.6119039","-5.9367534,54.6124284","-5.8905673,54.5983217"]

stationCodes = [3902,3903,3904,3905,3906,3907,3908,3909,3910,3911,3912,3913,3914,3915,3916,3917,3918,3919,3920,3921,3922,3923,3924,3925,3926,3927,3928,3929,3930,3931,3932,3933,3934,3935,3936,3937,3938,3940,3941,3942,3943,3944]

stationNames = ["City Hall","Victoria Square / Victoria Street","Donegall Quay","Central Station / Mays Meadow","St George's Market / Cromac Square","Gasworks (Cromac Street)","Waterfront","Botanic Avenue / Shaftesbury Square","Europa Bus Station / Blackstaff Square","Great Victoria Street / Hope Street","Castle Place / Royal Avenue","Smithfield / Winetavern Street","Cathedral Gardens / York Street","Carrick Hill / St Patricks Church","Dunbar Link / Gordon Street","North Street / Waring Street","Bankmore Square / Dublin Road","College Square East","Millfield / Divis Street","Odyssey / Sydenham Road","Corporation Square","Alfred Street / St Malachy's Church","Bradbury Place","Royal Avenue / Castlecourt","Cotton Court / Waring Street","Gasworks (Lagan Towpath)","Linenhall Street / Donegall Square South","Arthur Street / Chichester Street","Central Station / East Bridge Street","Writer's Square / St Anne's Cathedral","Titanic Quarter","Queens University / University Road","Queens University / Botanic Gardens","Belfast City Hospital / Lisburn Road","Royal Victoria Hospital","Mater Hospital / Crumlin Road","Shankill Leisure Centre","Grosvenor Road / Servia Street","Falls Road / Twin Spires","Girdwood Community Hub","Duncairn Centre / Antrim Road","CS Lewis Square"]

with open('cycleroutes.json', 'w', encoding="utf8") as myFile:
    myFile.write('{\n\t"type": "FeatureCollection",\n\t"features": [\n')
    for o in range(0,len(stationCodes)):
        origin = stationCoords[o]
        oName = stationNames[o]
        for d in range(0,len(stationCodes)):
            if d != o:
                dest = stationCoords[d]
                dName = stationNames[d]
                fullName = oName + ' to ' + dName
                fullCode = str(stationCodes[o]) + str(stationCodes[d])
                points = origin + ',' + oName + '|' + dest + ',' + dName
                query = {'itinerarypoints': points, 'plan': mode, 'key': key}
                resp = requests.get(url, query)
                print(resp.url)
                json_result = resp.json()
                route = json_result['marker'][0]['@attributes']['coordinates'].replace(" ","],[")
                route = ast.literal_eval(''.join(('[',route,']')))
                grammesCO2saved = json_result['marker'][0]['@attributes']['grammesCO2saved']
                distance = json_result['marker'][0]['@attributes']['length']
                seconds = json_result['marker'][0]['@attributes']['time']
                calories = json_result['marker'][0]['@attributes']['calories']
                elevation = int(json_result['marker'][0]['@attributes']['elevations'][-1]) - int(json_result['marker'][0]['@attributes']['elevations'][0])
                feature = {
                        "properties": {
                                "name": fullName,
                                "origin": oName,
                                "destination": dName,
                                "origin_code": stationCodes[o],
                                "destination_code": stationCodes[d],
                                "origin_point": route[0],
                                "destination_point": route[-1],
                                "code": fullCode,
                                "distance": int(distance),
                                "grammesCO2saved": int(grammesCO2saved),
                                "time": int(seconds),
                                "calories": int(calories),
                                "elevation": int(elevation)
                        },
                        "type": "Feature",
                        "geometry" : {
                                "type": "LineString",
                                "coordinates":
                                    route
				}
                        }
                json.dump(feature, myFile, indent = 4, separators = (', ',': '))
                myFile.write(',\n')
                time.sleep(3)
                continue
    mtFile.write('\n]}')
