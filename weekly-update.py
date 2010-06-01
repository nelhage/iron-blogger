#!/usr/bin/python
import render
import os
import sys
import xmlrpclib
import subprocess
import datetime
import yaml

XMLRPC_ENDPOINT = 'http://iron-blogger.mit.edu/xmlrpc.php'
USER            = 'nelhage'
BLOG_ID         = 1

dry_run = False

args = sys.argv[1:]
if args[0] == '-n':
    dry_run = True
    args = args[1:]

date = args[0]
today = str(datetime.date.today())

with open('ledger', 'a') as f:
    f.write("\n")
    f.write(render.render_template('templates/ledger', date))

subprocess.check_call(["git", "commit", "ledger",
                       "-m", "Update for %s" % (date,)])

debts = render.get_debts()
punt = []

with open('ledger', 'a') as f:
    f.write("\n")
    for (user, debt) in debts:
        if debt < 30: continue
        punt.append(user)
        f.write("""\
%(today)s Punt
  Pool:Owed:%(user)s  $-%(debt)s
  User:%(user)s
""" % {'user': user, 'debt': debt, 'today': today})


if not dry_run:
    text = render.render_template('templates/week.tmpl', date, punt=punt)

    lines = text.split("\n")
    title = lines[0]
    body  = "\n".join(lines[1:])

    page = dict(title = title, description = body)

    try:
        subprocess.call(['stty', '-echo'])
        passwd = raw_input("Password for %s: " % (USER,))
        print
    finally:
        subprocess.call(['stty', 'echo'])

    x = xmlrpclib.ServerProxy(XMLRPC_ENDPOINT)
    x.metaWeblog.newPost(BLOG_ID, USER, passwd, page, True)

email = render.render_template('templates/email.txt', date, punt=punt)

if dry_run:
    print email
else:
    p = subprocess.Popen(['mutt', '-H', '/dev/stdin'],
                         stdin=subprocess.PIPE)
    p.communicate(email)

if punt:
    with open('bloggers.yml') as b:
        bloggers = yaml.safe_load(b)
    for p in punt:
        if 'end' not in bloggers[p]:
            bloggers[p]['end'] = today
    with open('bloggers.yml','w') as b:
        yaml.safe_dump(bloggers, b)

    subprocess.check_call(["git", "commit", "ledger", "bloggers.yml",
                           "-m", "Punts for %s" % (today,)])
