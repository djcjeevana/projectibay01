import json


def readJson(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
        
def get_country():
    """ GET COUNTRY SELECTION """
    filepath = './static/data/countries_states_cities.json'
    all_data = readJson(filepath)
    
    all_countries = [('-----', '---Select a Country---')]
    
    for x in all_data:
          y = (x['name'], x['name'])
          all_countries.append(y)
          
    return all_countries

    def return_state_by_country(country):
        """ GET STATE SELECTION BY COUNTRY INPUT """
        filepath = './static/data/countries_states_cities.json'
        all_data = readJson(filepath)
        
    all_states = []
    
    
    for x in all_data:
         if x['name'] == country:
             if 'states' in x:
                for state in x['states']:
                    y = (state['name'], state['name'])
                    all_states.append(state['name'])
             else:
                 all_states.append(country)
                 
    return all_states