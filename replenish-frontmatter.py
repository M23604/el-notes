#!/usr/bin/env python3

import os
import fnmatch

matches = []
for root,dirnames,filenames in os.walk('.'):
    for filename in fnmatch.filter(filenames,'*.md'):
        if filename == 'README.md': continue
        matches.append([os.path.join(root,filename),filename])

for filedir,filename in matches:
    with open(filedir,'r') as f:
        cont = f.read()
        if '---\n' not in cont:
            with open(filedir,'w') as fp:
                fp.write(f"""
---
title: {filename[:-3]}
---
""" + cont)
