#!/usr/bin/python

import render
import os
import sys
import xmlrpclib
import subprocess

text = render.render_template('templates/users.tmpl')

XMLRPC_ENDPOINT = 'http://iron-blogger.mit.edu/xmlrpc.php'
USER            = 'nelhage'
BLOG_ID         = 1
PAGE_ID         = 16

try:
    subprocess.call(['stty', '-echo'])
    passwd = raw_input("Password for %s: " % (USER,))
    print
finally:
    subprocess.call(['stty', 'echo'])

x = xmlrpclib.ServerProxy(XMLRPC_ENDPOINT)
page = x.wp.getPage(BLOG_ID, PAGE_ID, USER, passwd)

page['description'] = text

x.wp.editPage(BLOG_ID, PAGE_ID, USER, passwd, page, True)

# Parameters
# int blog_id
# int page_id
# string username
# string password
# struct content
#   string wp_slug
#   string wp_password
#   int wp_page_parent_id
#   int wp_page_order
#   int wp_author_id
#   string title
#   string description (content of post)
#   string mt_excerpt
#   string mt_text_more
#   int mt_allow_comments (0 = closed, 1 = open)
#   int mt_allow_pings (0 = closed, 1 = open)
#   datetime dateCreated
#   array custom_fields
#     struct
#       string id
#       string key
#       string value
# bool publish
