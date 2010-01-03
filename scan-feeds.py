#!/usr/bin/python
import yaml
import feedparser
import datetime
from dateutil.parser import parse
import dateutil.tz as tz

with open('bloggers.yml') as f:
    users = yaml.safe_load(f.read())

log = {}

START = datetime.datetime(2009, 12, 21, 6)

def parse_published(pub):
    return parse(pub).astimezone(tz.tzlocal()).replace(tzinfo=None)

def get_date(post):
    if 'published' in post:
        return post.published
    return post.updated

def get_link(post):
    return post.link

def parse_feeds(weeks, uri):
    feed = feedparser.parse(uri)
    for post in feed.entries:
        date = parse_published(get_date(post))

        if date < START:
            continue
        wn = (date - START).days / 7

        while len(weeks) <= wn:
            weeks.append([])
        weeks[wn].append(dict(
                date=date,
                title=post.title,
                url=get_link(post)))

for (username, u) in users.items():
    weeks = []
    print "[%s]" % (username)
    for l in u['links']:
        parse_feeds(weeks, l[2])
    log[username] = weeks
    for (i, w) in enumerate(weeks):
        print " [%d]: %s" % (i, w)

with open('out/report.yml', 'w') as f:
    yaml.safe_dump(log, f)
