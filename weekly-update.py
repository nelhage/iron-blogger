#!/usr/bin/python
import render
import os
import sys
import xmlrpclib
import subprocess

XMLRPC_ENDPOINT = 'http://iron-blogger.mit.edu/xmlrpc.php'
USER            = 'nelhage'
BLOG_ID         = 1

try:
    subprocess.call(['stty', '-echo'])
    passwd = raw_input("Password for %s: " % (USER,))
    print
finally:
    subprocess.call(['stty', 'echo'])

x = xmlrpclib.ServerProxy(XMLRPC_ENDPOINT)

with open('ledger', 'a') as f:
    f.write("\n")
    f.write(render.render_template('templates/ledger', sys.argv[1]))

subprocess.check_call(["git", "commit", "ledger",
                       "-m", "Update for %s" % (sys.argv[1],)])

text = render.render_template('templates/week.tmpl', sys.argv[1])

lines = text.split("\n")
title = lines[0]
body  = "\n".join(lines[1:])

page = dict(title = title,
            description = body)

x.metaWeblog.newPost(BLOG_ID, USER, passwd, page, True)

p = subprocess.Popen(['mutt', '-H', '/dev/stdin'],
                     stdin=subprocess.PIPE)
p.communicate(render.render_template('templates/email.txt', sys.argv[1]))
