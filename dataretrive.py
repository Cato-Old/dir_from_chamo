import requests
from lxml import html


class ChamoRequest:
    CHAMO = 'https://chamo.buw.uw.edu.pl/'

    def __init__(self, sys_nr):
        self.link = self.CHAMO + 'search/query?match_1=PHRASE&field_1=control&term_1=' + sys_nr + '&theme=system'

    def get_link(self):
        resp = requests.get(self.link, verify=False)
        tree = html.fromstring(resp.content)
        titles = tree.xpath('//a[@class="title"]')
        if titles == 1:
            return self.CHAMO + titles[0].attrib['href'][3:]
        else:
            raise ValueError('More then 1 record for system number')
