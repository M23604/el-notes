#!/usr/bin/env python3

import os
import fnmatch
from pathlib import Path

# prefix components:
space =  '    '
branch = '│   '
# pointers:
tee =    '├── '
last =   '└── '


def tree(dir_path: Path, prefix: str=''):
    """A recursive generator, given a directory Path object
    will yield a visual tree structure line by line
    with each line prefixed by the same characters
    """
    contents = list(filter(lambda path: not "commitments" in str(path) and not ".git" in str(path) and not "README" in str(path) and not ".py" in str(path), dir_path.iterdir()))
    # contents each get pointers that are ├── with a final └── :
    pointers = [tee] * (len(contents) - 1) + [last]
    for pointer, path in zip(pointers, contents):
        yield prefix + pointer + path.name.rstrip(".pdf")
        if path.is_dir(): # extend the prefix and recurse:
            extension = branch if pointer == tee else space
            # i.e. space because last, └── , above so no more |
            yield from tree(path, prefix=prefix+extension)

def drawDirectoryStructure():
    s = ""
    for line in tree(Path(".")):
        s += line + '\n'
    return s

def frontmatter():
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
---""" + cont)

def index():
    dirs = []
    for root,dirnames,filenames in os.walk('.'):
        if  '.git' in root or './commitments' in root or root == '.':
            continue;
        dirs.append((root,[f for f in filenames if f.split('.')[-1] == 'md']))

    for folder,filenames in dirs:
        if os.path.exists(os.path.join(folder,'_index.md')):
            continue;
        with open(os.path.join(folder,'_index.md'),'w') as fp:
            fp.write(f"""
---
title:{os.path.basename(folder)}
---
""")
    return

def main():
    frontmatter()
    index()
    struct = drawDirectoryStructure()
    print(struct)
    with open('README.md','w') as fp:
        fp.write(f"""# EL Notes
If you want, please compile all statistics and data you find in this repository. For EL4131. Additional articles are also appreciated.

## Directory Structure
```
{struct}
```
""")
    with open('tree.txt','w') as fp:
        fp.write(struct)

main()
