#!/usr/bin/python
import yaml
from dateutil.parser import parse
import datetime
import dateutil.tz as tz
import sys
import os
import os.path
import subprocess
from mako.template import Template

START = datetime.datetime(2009, 12, 21, 6)
HERE  = os.path.dirname(__file__)

def render_template(path, week=None):
    with open('out/report.yml') as r:
        report = yaml.safe_load(r)

    with open('bloggers.yml') as f:
        users = yaml.safe_load(f)
    if week:
        week = parse(week, default=START)
    else:
        week = START

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

    p = subprocess.Popen(['ledger', '-f', os.path.join(HERE,'ledger'),
                          '-n', 'balance', 'Pool'],
                         stdout=subprocess.PIPE)
    (out, _) = p.communicate()
    pool = int(out.split()[0][1:])

    return Template(filename=path, output_encoding='utf-8').render(
        week=week, week_start=week_start,week_end=week_end,
        good=good, lame=lame, skip=skip, userlist=userlist,
        pool=pool)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print >>sys.stderr, "Usage: %s TEMPLATE [WEEK]"
        sys.exit(1)

    template = sys.argv[1]
    week = None
    if len(sys.argv) > 2: week = sys.argv[2]
    print render_template(template, week)
