# -*- coding: utf-8 -*-
import os
import click
import logging
from dotenv import find_dotenv, load_dotenv
import pyodbc
import csv

logger = logging.getLogger(__name__ or 'pull_raw_sql')

def getconn():
    return pyodbc.connect(driver='{SQL Server Native Client 11.0}',server='localhost',database='dddmdb2',trusted_connection='yes')

def queryToCsv(sql, filename, include_headers=True):
    logger.info('running query '+sql)

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
def getexternalname(name):
    return os.path.join(*[os.getcwd(), 'data', 'raw', name+'.csv'])

#queries = [ ('name', 'sql') ]
queries = [ ('one', 'select 1 as one') ]

@click.command()
def main():
    """ pulls data from sql server   """
    logger = logging.getLogger(__name__ or 'pull_raw_sql')
    logger.info('running queries')
    for name,sql in queries:
        queryToCsv(sql, getexternalname(name))


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = os.path.join(os.path.dirname(__file__ or 'make_dataset'), os.pardir, os.pardir)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
