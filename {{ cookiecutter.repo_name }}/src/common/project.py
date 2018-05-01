# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
from datetime import datetime
from datetime import timedelta
from pandas.tseries.offsets import *
from dateutil import relativedelta
import csv
import calendar
import pandas as pd
import numpy as np
from pprint import pprint
import sys
from sys import argv

debug = False

################################################################################
## imports
try:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
except:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), '..', '..')))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), '..')))

################################################################################
## logging setup
logger = logging.getLogger(__name__ or 'project.py')

################################################################################
## functions

def tryRemove(removeable):
    try:
        removeable.remove(np.nan)
    except ValueError:
        pass
    return removeable

def getdatafilename(name, subdir):
    return os.path.join(*[os.getcwd(), 'data', subdir, name])

