#!/usr/bin/python
import yaml
import feedparser
import datetime
import sys
from dateutil.parser import parse
import dateutil.tz as tz

with open('bloggers.yml') as f:
    users = yaml.safe_load(f.read())

try:
    with open('out/report.yml') as f:
        log = yaml.safe_load(f.read())
except IOError:
    log = {}

START = datetime.datetime(2009, 12, 21, 6)

def parse_published(pub):
    return parse(pub).astimezone(tz.tzlocal()).replace(tzinfo=None)

def get_date(post):
    for k in ('published', 'created', 'updated'):
        if k in post:
            return post[k]

def get_link(post):
    return post.link

def parse_feeds(weeks, uri):
    feed = feedparser.parse(uri)
    if not feed.entries:
        print >>sys.stderr, "WARN: no entries for ", uri
    for post in feed.entries:
        date = parse_published(get_date(post))

        if date < START:
            continue
        wn = (date - START).days / 7

        while len(weeks) <= wn:
            weeks.append([])

        post = dict(date=date,
                    title=post.title,
                    url=get_link(post))
        if post['url'] not in [p['url'] for p in weeks[wn]]:
            weeks[wn].append(post)

if len(sys.argv) > 1:
    for username in sys.argv[1:]:
        weeks = log.setdefault(username, [])
        for l in users[username]['links']:
            parse_feeds(weeks, l[2])
else:
    for (username, u) in users.items():
        weeks = log.setdefault(username, [])
        for l in u['links']:
            parse_feeds(weeks, l[2])

with open('out/report.yml', 'w') as f:
    yaml.safe_dump(log, f)
