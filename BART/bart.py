import requests
import json

'''
CASE A) For BART search request
Option 1) User can input name of station( “Departing from” station ) and BART line. In this case,
the user has information about the specific BART line that he/she want to board.
Input format:  BART    Station name       BART line
This input search will display the time schedule of next BART available from the input BART station for the input BART line (only). For example the input BART Downtown Berkeley Richmond would only display the time schedule of the next BART train from Downtown Berkeley station towards Richmond Line.

Option 2) Users can only input the name of station ( “Departing from” station) without specifying a BART  line
Input format:  BART    Station name
This input search will display a list of time schedules for all BART line from the input BART
station. For example the input BART Richmond will provide the user the time schedules for the next available BART for all lines such as Richmond, Daly City, Warm Springs/South Fremont, Fremont, Pleasanton/Dublin, Pittsburg/Bay Point.

'''


def pretty_print_dict(any_dict=None):
    return json.dumps(any_dict, sort_keys=True, indent=4)


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
        # print(pretty_print_dict(payload_dict))

        # loading json output returns a dictionary"payload_dict" - which comprises of a list of stations - which is further comprised of dict
        #{[{},{},{},{}],[{},{},{},{}],[{},{},{},{}],[{},{},{},{}]}

        station_list = payload_dict['root']['stations']['station']

        station_name_abbr_dict = {}
        '''
            This dictionary converts BART station names to abbreviations used by BART.
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
            name = station_dict['name'].upper()

            # Found a bug in the api where stn name is sometimes Warm Springs
            # and sometimes Warm Springs / South Fremont. We might need to change
            # this if BART fixes it
            if 'warm' in name:
                name = 'warm springs'

            abbr = station_dict['abbr'].upper()

            station_name_abbr_dict[name] = abbr
            station_abbr_name_dict[abbr] = name

        return station_name_abbr_dict, station_abbr_name_dict
        # print(station_name_abbr_dict, station_abbr_name_dict)

    def get_estimated_times(self, origin_station_name='fremont', line_final_station_name=None):
        """get_estimated_times function returns the time after which the user can catch the next BART
        from a input station by specifying a origin station and line"""

        origin_station_name = origin_station_name.upper()

        station_name_abbr_dict, station_abbr_name_dict = self.get_station_name_dict()

        if origin_station_name not in station_name_abbr_dict:
            raise ValueError("No such origin station found - %s" % (origin_station_name))

        origin_station_abbr = station_name_abbr_dict[origin_station_name]

        etd_page = '%s/etd.aspx?cmd=etd&orig=%s&key=%s&json=y' % (
            self.api_prefix, origin_station_abbr, self.api_key)

        response = requests.get(etd_page)

        # This raises a ValueError if status_code is not 200
        if response.status_code != 200:
            raise ValueError(
                "There is some problem with API - Check whether page %s is accessible" % (etd_page))

        payload_dict = json.loads(response.text)
        # print(pretty_print_dict(payload_dict))

        etd_list = payload_dict['root']['station'][0]['etd']

        destination_etd_dict = {}
        '''
            For now, this is of the type
            {
                "Richmond" : [2,4,5]
            }

        '''

        for etd in etd_list:
            key = etd['destination'].upper()
            multiple_trains = etd['estimate']
            value_list = []
            for train in multiple_trains:
                value_list.append(train['minutes'])
                # makes a lsit of all approaching barts for different lines - 3-4 in numbers

            destination_etd_dict[key] = value_list

        if not line_final_station_name:
            return destination_etd_dict

        line_final_station_name = line_final_station_name.upper()

        if line_final_station_name not in destination_etd_dict:
            # raise ValueError("No such line final station found - %s" % (line_final_station_name))
            print("No such line final station found - %s" % (line_final_station_name))
            return destination_etd_dict

        destination_etd_line_dict = {}
        destination_etd_line_dict[line_final_station_name] = destination_etd_dict[line_final_station_name]
        return destination_etd_line_dict


if __name__ == "__main__":

    origin_station_name = input("Enter the name of BART station you want to board from: ")
    line_final_station_name = input("Enter the BART line you want to take: ")

    bart_api = BartApi()

    station_name_abbr_dict, station_abbr_name_dict = bart_api.get_station_name_dict()

    # print('List of all BART stations')
    # for key, value in station_name_abbr_dict.items():
    #     print("%40s: %s" % (key, value))

    # print('\n')

    # for key, value in station_abbr_name_dict.items():
    #     print("%s: %40s" % (key, value))

    # print('\n')

    print('\nETD from {}'.format(origin_station_name.upper()), 'station')

    etd_dict = bart_api.get_estimated_times(origin_station_name=origin_station_name,
                                            line_final_station_name=line_final_station_name)
    for key, value in etd_dict.items():
        print("%20s: %s" % (key, value))

    # print('\nETD from Fremont to Richmond')
    # etd_dict = bart_api.get_estimated_times(origin_station_name=origin_station_name,
    #                                         line_final_station_name=line_final_station_name)
    # for key, value in etd_dict.items():
    #     print("%20s: %s" % (key, value))
