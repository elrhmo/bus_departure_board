import requests

api_key = 'df0a46654d724e80b29e1f275b0de82a'
stop_point_id = '490011922E'


def get_bus_data():    
    url = f'https://api.tfl.gov.uk/StopPoint/{stop_point_id}/Arrivals'

    headers = {'Accept': 'application/json', 'Authorization': f'Api-Key {api_key}'}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        departures = response.json()

        # Sort departures by 'timeToStation' in ascending order
        sorted_departures = sorted(departures, key=lambda x: x['timeToStation'])
        
        #create an empty list to store departure information
        departure_list = []  
        for counter, departure in enumerate(sorted_departures): # the enumerate() function adds a counter as the key of the enumerate object.
            if departure['timeToStation']/60 < 1: 
                info= [f"{counter + 1}", f"{departure['lineName']}", f"{departure['destinationName'].split(',')[0]}", f"due"]

            else:
                info = [f"{counter + 1}", f"{departure['lineName']}", f"{departure['destinationName'].split(',')[0]}", f"{str(int(departure['timeToStation']/60))}min"]

            departure_list.append(info)  # Append the information to the list

    else:
        print(f"Error: {response.status_code} - {response.text}")
    
    return departure_list