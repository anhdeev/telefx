#!/usr/bin/python
import psycopg2
from db.config import config

class MyPostgres(object):
    def __init__(self):
        try:
            print('Connecting to the PostgreSQL database...')
            params = config()
            self.conn = psycopg2.connect(**params)
            print('Connected!')
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def execute(self, object):
        try:
            cur = self.conn.cursor()
            cmd = self._build_sql(object)
            cur.execute(cmd)
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            self.conn.rollback()
            cur.close()

    def _build_sql(self, object):
        table_name = 'mem_usage'
        columns = list(object.keys())
        values = list(object.values())

        sql_string = 'INSERT INTO {} '.format( table_name )
        sql_string += "(" + ', '.join(columns) + ")\nVALUES "
        sql_string += "(" + ', '.join(str(v) for v in values) + ");"
        return sql_string

        

