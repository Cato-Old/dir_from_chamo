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
            call_nrs = [x.text for x in call_nrs_raw]
        else:
            call_nrs = ""
        self.result.append(call_nrs)

    def get_data(self):
        self.get_marc_fields()
        self.get_call_nrs()

class MARCFormatter:

    def __init__(self, fields):
        self.fields = fields

    def author_format(self):
        authorraw = self.fields[0][3:self.fields[0].find('$', 1)]
        if ',' in authorraw:
            names = authorraw.split(', ', 1)
            last_name, first_names = names
            initials = ''.join(x for x in first_names if x.isupper())
            author = last_name + ', ' + initials
        elif '. ' in authorraw:
            author = authorraw.replace('. ', '')
        elif authorraw[-1] == ' ':
            author = authorraw[:-1]
        return author

    def title_format(self):
        titleraw = self.fields[1][3:self.fields[1].find('$', 1)]
        if ' / ' in titleraw:
            title = titleraw.replace(' / ', '')
        elif '. ' in titleraw:
            title = titleraw.replace('. ', '')
        title_ls = title.split(' ')
        if len(title_ls) > 5:
            title = ' '.join(title_ls[:6]) + ' (...)'
        return title

    def call_nrs_format(self):
        call_nrsraw = self.fields[2]
        if call_nrsraw == "":
            call_nrs = ""
        else:
            call_nrs = ', '.join(x if 'BUW' in x else 'BUW ' + x for x in call_nrsraw)
        return call_nrs

    def data_format(self):
        return ' '.join((self.author_format() + ',', self.title_format(), '(' + self.call_nrs_format() + ')'))
