# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import pyodbc
import csv

################################################################################
## what to do where
_driver='{SQL Server Native Client 11.0}'
_server='localhost'
_database='DATABASENAME'
_trusted_connection='yes'

queries = queries = [ ('name1', 'SELECT 1 as n'), ('name2', 'SELECT 2 as n')]


################################################################################
## logging setup
def getmodname():
    return __name__ or 'pull_raw_sql.py'

logfile = os.path.join(*[os.getcwd(), 'data', 'raw', getmodname()+'.csv'])

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
logger = logging.getLogger(getmodname())

################################################################################
## Functions
def getconn():
    connstr = "driver='%s',server='%s', database='%s',trusted_connection='%s'" % (_driver,_server,_database,_trusted_connection)
    logger.debug('connecting using connstr: ' + connstr)
    return pyodbc.connect(driver=_driver,server=_server,database=_database,trusted_connection=_trusted_connection)

def queryToCsv(qname, sql, filename, include_headers=True):
    logger.info('running query '+qname)
    logger.debug(sql)
    conn = getconn()
    crsr = conn.cursor()
    rows = crsr.execute(sql)
    logger.info('saving file ' + filename)
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if include_headers:
            writer.writerow([x[0] for x in crsr.description])  # column headers
        for row in rows:
            writer.writerow(row)

#assume run from project base dir
def getrawname(name):
    return os.path.join(*[os.getcwd(), 'data', 'raw', name+'.csv'])

################################################################################
## main
@click.command()
def main():
    """ pulls data from sql server   """
    logger = logging.getLogger(getmodname())
    logger.info('running queries')

    for name,sql in queries:
        queryToCsv(name, sql, getrawname(name))


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(getmodname()), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
