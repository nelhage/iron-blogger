import yaml
from dateutil.parser import parse
import datetime
import dateutil.tz as tz
import sys

START = datetime.datetime(2009, 12, 21, 6)

with open('out/report.yml') as r:
    report = yaml.safe_load(r)

with open('bloggers.yml') as f:
    users = yaml.safe_load(f)

week = (parse(sys.argv[1], default=START) - START).days / 7
week_start = START + (week * datetime.timedelta(7))
week_end   = START + ((week + 1) * datetime.timedelta(7))


for (name, weeks) in report.items():
    user_start = parse(users[name]['start'], default=START)
    if user_start > week_start:
        print "SKIP %s" % (name,)
        continue
    elif len(weeks) <= week or not weeks[week]:
        print "LAME %s" % (name,)
    else:
        print "OK %s" % (name,)
