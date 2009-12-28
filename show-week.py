import yaml
from dateutil.parser import parse
import datetime
import dateutil.tz as tz
import sys
from mako.template import Template

START = datetime.datetime(2009, 12, 21, 6)

with open('out/report.yml') as r:
    report = yaml.safe_load(r)

with open('bloggers.yml') as f:
    users = yaml.safe_load(f)

week = (parse(sys.argv[1], default=START) - START).days / 7
week_start = START + (week * datetime.timedelta(7))
week_end   = START + ((week + 1) * datetime.timedelta(7))

good = []
lame = []
skip = []


for (name, weeks) in report.items():
    user_start = parse(users[name]['start'], default=START)
    if user_start > week_start:
        skip.append(name)
        continue
    elif len(weeks) <= week or not weeks[week]:
        lame.append(name)
    else:
        good.append(name)

print Template(filename=sys.argv[2], output_encoding='utf-8').render(
    week=week, week_start=week_start,week_end=week_end,
    good=good, lame=lame, skip=skip, users=users, report=report)
