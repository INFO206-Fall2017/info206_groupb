import requests
import json


class BartApi(object):
    def __init__(self):
        self.api_key = 'MW9S-E7SL-26DU-VV8V'
        self.api_prefix = 'https://api.bart.gov/api'

    # This can be used to find all stations and corresponding abbr (required for page request)
    def get_station_name_dict(self):
        station_list_page = '%s/stn.aspx?cmd=stns&key=%s&json=y' % (self.api_prefix, self.api_key)
        response = requests.get(station_list_page)

        # This raises a ValueError if status_code is not 200
        if response.status_code != 200:
            raise ValueError(
                "There is some problem with API - Check whether page %s is accessible" % (station_list_page))

        payload_dict = json.loads(response.text)
        # json output returns a dictionary - which comprises of a list of stations which is further comprised of dict
        station_list = payload_dict['root']['stations']['station']

        station_name_abbr_dict = {}
        '''
            For now, this dictionary is of the type
            {
                "Union City" : "UCTY"
            }
        '''

        station_abbr_name_dict = {}
        '''
            For now, this dictionary is of the type
            {
                "UCTY" : "Union City"
            }
        '''

        for station_dict in station_list:
            # note- station_dict is a dict which is a part of list - station_list
            name = station_dict['name']

            # Found a bug in the api where stn name is sometimes Warm Springs
            # and sometimes Warm Springs / South Fremont. We might need to change
            # this if BART fixes it
            if 'Warm' in name:
                name = 'Warm Springs'

            abbr = station_dict['abbr']

            station_name_abbr_dict[name] = abbr
            station_abbr_name_dict[abbr] = name

        return station_name_abbr_dict, station_abbr_name_dict


bart_api = BartApi()

station_name_abbr_dict, station_abbr_name_dict = bart_api.get_station_name_dict()

print('List of all BART stations')
for key, value in station_name_abbr_dict.items():
    print("%40s: %s" % (key, value))

print('\n')

for key, value in station_abbr_name_dict.items():
    print("%s: %40s" % (key, value))
