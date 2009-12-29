#!usr/bin/python
from lxml import html
import yaml

tree = html.fromstring(open('/tmp/iron-blogger.html').read())

who = {}
for tr in list(tree.xpath('//tr'))[1:]:
    username = str(tr.xpath('td[1]/tt/text()')[0])
    links = tr.xpath('td[2]/a')
    links = [(l.text, l.attrib['href']) for l in links]
    start = str(tr.xpath('td[3]/text()')[0]).strip()
    who[username] = dict(links=links, start=start)

print yaml.safe_dump(who)
