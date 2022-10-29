import unittest
from unittest.mock import MagicMock
from src.api_connector import APIConnector


class MockGeoIp:
    self.url = "example.com"
    self.result = "{'ip': '93.184.216.34', 'success': True, 'type': 'IPv4', 'continent': 'North America', 'continent_code': 'NA', 'country': 'United States', 'country_code': 'US', 'region': 'Virginia', 'region_code': 'VA', 'city': 'Ashburn', 'latitude': 39.0437567, 'longitude': -77.4874416, 'is_eu': False, 'postal': '20147', 'calling_code': '1', 'capital': 'Washington D.C.', 'borders': 'CA,MX', 'flag': {'img': 'https://cdn.ipwhois.io/flags/us.svg', 'emoji': '🇺🇸', 'emoji_unicode': 'U+1F1FA U+1F1F8'}, 'connection': {'asn': 15133, 'org': 'NETBLK-03-EU-93-184-216-0-24', 'isp': 'Edgecast Inc.', 'domain': 'edgecast.com'}, 'timezone': {'id': 'America/New_York', 'abbr': 'EDT', 'is_dst': True, 'offset': -14400, 'utc': '-04:00', 'current_time': '2022-10-29T12:51:03-04:00'}}"

    def get(self, url):
        if url == self.url:
            return self.result
        else:
            return "{}"


class TestAPIConnector(unittest.TestCase):
    def setUp(self):
        logger = MagicMock()
        self.api_connector = APIConnector({}, logger)

    def test_get_ip(self):
        url = "https://www.example.com/test1"
        excepted_result = "93.184.216.34"
        result = self.api_connector.get_ip(url)
        self.assertEqual(excepted_result, result)

    def test_get_geoip(self):
        url = "https://www.example.com/test1"
        excepted_result = "United States"
        result = self.api_connector.get_geoip(url)
        self.assertEqual(excepted_result, result)


if __name__ == "__main__":
    unittest.main()
