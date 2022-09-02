#!./bin/python

import linecache
import re

SRC_DIR = '.'
DEST_DIR = '.'
GENERATE_FILE_NAME = 'cats.py'
SRC_FILE_LIST = [
    'conf.py',
    'scenarios.py',
    'cat.py',
    'callchain.py',
]
IMPORTS = """
import argparse
import copy
import datetime
import logging
import json
import random
import time
import os
import requests
import re
import csv
import graphviz
from tabulate import tabulate
import jsonpath_ng as jp
import pandas as pd
from bs4 import BeautifulSoup
"""

IMPORT_STATEMENTS = [
    re.compile('^import .*$'),
    re.compile('^from .* import .*$'),
]

if __name__ == '__main__':
    with open('{0}/{1}'.format(DEST_DIR, GENERATE_FILE_NAME)) as f:
        f.write(IMPORTS)
        for file_name in SRC_FILE_LIST:
            lines = linecache.getlines('{0}/{1}'.format(SRC_DIR, file_name))
            for line in lines:
                if any([re.match(regexp, line.strip(' \r\n\t')) for regexp in IMPORT_STATEMENTS]):
                    continue
                f.write(line)

