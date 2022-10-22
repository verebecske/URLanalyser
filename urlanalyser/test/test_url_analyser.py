import unittest
from unittest.mock import MagicMock
from src.URLAnalyser import URLAnalyser

class TestClass(unittest.TestCase):
    def setUp(self):
        logger = MagicMock()
        config = {}
        self.analyser = URLAnalyser(config=config, logger=logger)

    def test_valid_url(self):
        test_dict = {
            "test_1": {
                "url": "https://napszemuveg.be",
                "excepted": True,
            },
            "test_2": {
                "url": "http://www.example.com",
                "excepted": True,
            },
            "test_3": {
                "url": "http://www.sub.domain.com",
                "excepted": True,
            },
            "test_4": {
                "url": "www.example.com",
                "excepted": True,
            },
            "test_5": {
                "url": "example.com",
                "excepted": True,
            },
            "test_6": {
                "url": "https://example.com",
                "excepted": True,
            },
            "test_7": {
                "url": "http://www.sub?.domain.com",
                "excepted": False,
            },
            "test_8": {
                "url": "http://www.sub5-sub6.domain.com",
                "excepted": True,
            },
            "test_9": {
                "url": "http://www.sub5_sub6.domain.com",
                "excepted": False,
            },
             "test_10": {
                "url": "https://www.example.com/open=1234",
                "excepted": True,
            },
            "test_11": {
                "url": "https://www.example.com/?open=1234&id=Fi!&?*23",
                "excepted": True,
            },
        }


        for test_case, value in test_dict.items():
            res = self.analyser.valid_url(value["url"])
            self.assertEqual(res, value["excepted"], msg=f"Error in {test_case}")

        
if __name__ == '__main__':
    unittest.main()