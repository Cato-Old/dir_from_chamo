from unittest import TestCase

from src.main.python.dataretrive import ChamoRequest


class TestChamoRequest(TestCase):
    test_request = ChamoRequest('zz2006875306')

    def test_get_link(self):
        test_exp = r'https://chamo.buw.uw.edu.pl/lib/item?id=chamo:1479525&fromLocationLink=false&theme=system'
        link = 'https://chamo.buw.uw.edu.pl/search/query?match_1=PHRASE&field_1=control&term_1=xx004450974&theme=system'
        self.assertEqual(self.test_request.get_link(link), test_exp)

    def test_get_data(self):
        self.test_request.get_data()
        test_exp = ['$a Augustyn $c (św. ; $d 354-430). ', '$a Wyznania / $c Święty Augustyn ; przeł. Zygmunt Kubiak. ', 'BUW W.14892 a, BUW 1252696, BUW 514507, BUW W.XVIIIb.270 d, BUW 514509, BUW 540240']
        self.assertEqual(self.test_request.result, test_exp)