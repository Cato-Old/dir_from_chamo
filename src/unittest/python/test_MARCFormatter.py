from unittest import TestCase

from src.main.python.dataretrive import MARCFormatter


class TestMARCFormatter(TestCase):
    test_formatter = MARCFormatter(['$a Augustyn $c (św. ; $d 354-430). ', '$a Wyznania / $c Święty Augustyn ; przeł. Zygmunt Kubiak. ', ['W.14892 a', '1252696', '514507', 'W.XVIIIb.270 d', '514509', '540240']])

    def test_data_format(self):
        test_exp = "Augustyn, Wyznania (BUW W.14892 a, BUW 1252696, BUW 514507, BUW W.XVIIIb.270 d, BUW 514509, BUW 540240)"
        self.assertEqual(self.test_formatter.data_format(), test_exp)
