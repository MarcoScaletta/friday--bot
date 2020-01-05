import json 

class GTTStop:

    @staticmethod
    def parse_departures(departures_info):
        departures_info_json = json.loads(departures_info)
        response_message = ""
        if len(departures_info_json) == 0:
            response_message += "Non sono previste partenze da questa fermata."
        else:
            for line in departures_info_json:
                response_message += "LINEA " + str(line['name']) +'\n'
                # response_message += "INFO " + line['longName']  +'\n'
                if line['departures'] is None or len(line['departures']) == 0:
                    response_message += "Non sono previste partenze per questa linea."
                else:
                    for departure in line['departures']:
                        response_message += departure['time'] 
                        if departure['rt']:
                            response_message += "*" 
                        response_message += ", "
                    response_message = response_message[:-2]
                    response_message += "\n"
                        
            
        return response_message

