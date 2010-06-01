#!/usr/bin/python
import render
import os
import sys
import xmlrpclib
import subprocess

XMLRPC_ENDPOINT = 'http://iron-blogger.mit.edu/xmlrpc.php'
USER            = 'nelhage'
BLOG_ID         = 1

args = sys.argv[1:]
if args[0] == '-n':
    dry_run = True
    args = args[1:]

date = args[0]

try:
    subprocess.call(['stty', '-echo'])
    passwd = raw_input("Password for %s: " % (USER,))
    print
finally:
    subprocess.call(['stty', 'echo'])

with open('ledger', 'a') as f:
    f.write("\n")
    f.write(render.render_template('templates/ledger', date))

subprocess.check_call(["git", "commit", "ledger",
                       "-m", "Update for %s" % (date,)])

text = render.render_template('templates/week.tmpl', date)

lines = text.split("\n")
title = lines[0]
body  = "\n".join(lines[1:])

page = dict(title = title,
            description = body)

if not dry_run:
    x = xmlrpclib.ServerProxy(XMLRPC_ENDPOINT)
    x.metaWeblog.newPost(BLOG_ID, USER, passwd, page, True)

email = render.render_template('templates/email.txt', date)

if dry_run:
    print email
else:
    p = subprocess.Popen(['mutt', '-H', '/dev/stdin'],
                         stdin=subprocess.PIPE)
    p.communicate(email)
