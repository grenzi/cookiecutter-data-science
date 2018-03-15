# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import csv
import pandas as pd
import numpy as np
import sys
debug = False


################################################################################
## logging setup
modname = __name__ or 'MODNAME'
logfile = os.path.join(*[os.getcwd(), 'data', 'interim', MODNAME+'.csv'])

try:
    os.remove(logfile)
except OSError:
    pass

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s,%(name)s,%(levelname)s,"%(message)s"',
                    datefmt='%m-%d %H:%M',
                    filename= logfile,
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logger = logging.getLogger(modname)


################################################################################
## imports
try:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
except:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), '..', '..')))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), '..')))
from common.project import *

################################################################################
## main
@click.command()
def main():
    logger = logging.getLogger('main')
    logger.info('Starting')

    dfoutput = pd.DataFrame()

    outputname = getdatafilename(FILENAME, SUBDIR)
    logger.info('Saving generated opp lines to ' + outputname)
    dfoutput.to_excel(outputname, index_label='lineinopp')

if __name__ == '__main__':
    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__ or modname+'.py'), os.pardir, os.pardir)
    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())
    main()
