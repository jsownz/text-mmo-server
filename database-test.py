#!/usr/bin/env python3
import psycopg2
import configparser

def connect():
  conn = None

  config = configparser.ConfigParser()
  config.read('database.ini')

  try:

    print('Connecting...')
    conn = psycopg2.connect(host=config['postgresql']['host'],database=config['postgresql']['database'], user=config['postgresql']['user'], password=config['postgresql']['password'], port=config['postgresql']['port'])

    cur = conn.cursor()

    print('DB Ver:')
    cur.execute('SELECT version()')

    db_version = cur.fetchone()
    print(db_version)

    cur.close()
  except (Exception, psycopg2.DatabaseError) as error:
    print('error: %s', error)
  finally:
    if conn is not None:
      conn.close()
      print('DB conn closed')


if __name__ == '__main__':
  connect()