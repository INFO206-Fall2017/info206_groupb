import unittest
from bart import BartApi


class TestUM(unittest.TestCase):
    def setUp(self):
        self.bart_api = BartApi()
        # At this point, BartApi's __init__() is already executed
        # that means all member variables are initialized

    def test_station_name_abbr_dict(self):
        self.assertEqual(self.bart_api.station_name_abbr_dict["FREMONT"], "FRMT")

    def test_station_abbr_name_dict(self):
        self.assertEqual(self.bart_api.station_abbr_name_dict["RICH"], "RICHMOND")

    # the ouputs for other functions are dynamic in nature. hence, a test was not written for them


if __name__ == '__main__':
    unittest.main()
