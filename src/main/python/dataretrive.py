import requests
from lxml import html


class ChamoRequest:
    CHAMO = 'https://chamo.buw.uw.edu.pl/'

    def __init__(self, sys_nr):
        link = self.CHAMO + 'search/query?match_1=PHRASE&field_1=control&term_1=' + sys_nr + '&theme=system'
        self.result = []
        self.tree = self.get_itemlink(self.get_link(link))

    def get_link(self, link):
        resp = requests.get(link)
        tree = html.fromstring(resp.content)
        titles = tree.xpath('//a[@class="title"]')
        if len(titles) == 1:
            return self.CHAMO + titles[0].attrib['href'][3:]
        else:
            raise ValueError('More then 1 record for system number')

    def get_itemlink(self, link):
        resp = requests.get(link)
        return html.fromstring(resp.content)

    def get_marc_fields(self):
        xpath_query = '(//div[@class="marcTag" and contains(text(),"{MARC_field}")]/following-sibling::div/div[@class="newMarcData"])[1]'
        xpath = lambda x: xpath_query.format(MARC_field=x)
        for MARC_field in (100, 245):
            if len(self.tree.xpath(xpath(MARC_field))) == 1:
                field = self.tree.xpath(xpath(MARC_field))[0].text
            else:
                field = ""
            self.result.append(field)

    def get_call_nrs(self):
        call_nrs_raw = self.tree.xpath('//div[@id="tabContents-1"]/*/table/tbody/tr/td[3]/div[text()]')
        if len(call_nrs_raw) > 0:
            call_nrs = ', '.join('BUW ' + x.text if 'BUW' not in x.text else x.text for x in call_nrs_raw)
        else:
            call_nrs = ""
        self.result.append(call_nrs)

    def get_data(self):
        self.get_marc_fields()
        self.get_call_nrs()
