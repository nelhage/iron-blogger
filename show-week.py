#!/usr/bin/python
import yaml
from dateutil.parser import parse
import datetime
import dateutil.tz as tz
import sys
import os
from mako.template import Template

if len(sys.argv) < 2:
    print >>sys.stderr, "Usage: %s TEMPLATE [WEEK]" 
    sys.exit(1)

template = sys.argv[1]
START = datetime.datetime(2009, 12, 21, 6)

if len(sys.argv) == 3:
    week = parse(sys.argv[2], default=START)
else:
    week = START

with open('out/report.yml') as r:
    report = yaml.safe_load(r)

with open('bloggers.yml') as f:
    users = yaml.safe_load(f)

week = (week - START).days / 7
week_start = START + (week * datetime.timedelta(7))
week_end   = START + ((week + 1) * datetime.timedelta(7))

good = []
lame = []
skip = []
userlist = []

class User(object):
    pass

for (un, rec) in users.items():
    u = User()
    u.username = un
    u.links = rec['links']
    u.start = rec['start']
    u.weeks = report.get(un, [])

    userlist.append(u)

def user_key(u):
    return (u.start, u.username)

userlist.sort(key=user_key)

for u in userlist:
    user_start = parse(u.start, default=START)
    if user_start > week_start:
        skip.append(u)
    elif len(u.weeks) <= week or not u.weeks[week]:
        lame.append(u)
    else:
        good.append(u)

print Template(filename=template, output_encoding='utf-8').render(
    week=week, week_start=week_start,week_end=week_end,
    good=good, lame=lame, skip=skip, userlist=userlist)
