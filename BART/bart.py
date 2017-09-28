import requests
import json


class BartApi(object):
    def __init__(self):
        self.api_key = 'MW9S-E7SL-26DU-VV8V'
        self.api_prefix = 'https://api.bart.gov/api'

    # This can be used to find all stations and corresponding abbr (required for page request)
    def get_station_name_list(self):
        station_list_page = '%s/stn.aspx?cmd=stns&key=%s&json=y' % (self.api_prefix, self.api_key)
        r = requests.get(station_list_page)
        payload_dict = json.loads(r.text)
        station_list = payload_dict['root']['stations']['station']

        station_dict = {}
        '''
            For now, this is of the type
            {
                "Union City" : "UCTY"
            }
        '''

        station_abbr_dict = {}
        '''
            For now, this is of the type
            {
                "UCTY" : "Union City"
            }
        '''

        for station in station_list:
            key = station['name']

            # Found a bug in the api where stn name is sometimes Warm Springs
            # and sometimes Warm Springs / South Fremont. We might need to change
            # this if BART fixes it
            if 'Warm' in key:
                key = 'Warm Springs'

            value = station['abbr']
            station_dict[key] = value

            station_abbr_dict[value] = key

        return station_dict, station_abbr_dict


bart_api = BartApi()
station_dict, station_abbr_dict = bart_api.get_station_name_list()

print('List of all BART stations')
for key, value in station_dict.items():
    print("%40s: %s" % (key, value))

print('\n')
