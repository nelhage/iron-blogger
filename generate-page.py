#!/usr/bin/python
import yaml
from mako.template import Template

with open('bloggers.yml') as f:
    users = yaml.safe_load(f.read())

class User(object):
    pass

all = []
for (un, rec) in users.items():
    u = User()
    u.username = un
    u.links = rec['links']
    u.start = rec['start']
    all.append(u)

def user_key(u):
    return (u.start, u.username)

all.sort(key=user_key)

tmpl = Template(filename='templates/iron-blogger.tmpl', output_encoding='utf-8')
print tmpl.render(users=all)
