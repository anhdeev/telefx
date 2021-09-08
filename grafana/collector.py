#!/usr/bin/python
from configparser import Error
from db.postgres import MyPostgres
import requests
import os
import time, threading

class Collector(object):
    def __init__(self):
        self.db = MyPostgres()

    def start_interval(self, target, interval=10):
        try:
            r = requests.get(target)
            if(r.status_code != 200 or r.headers.get('content-type') != 'application/json'):
                print('response: failed')
                time.sleep(60)
                raise Exception(r.status_code, r.headers.get('content-type')) 
            
            data = r.json()
            self.db.execute(data)
            print(time.ctime())
        except (Exception) as error:
            print(error)
            time.sleep(60)
        finally:
            threading.Timer(interval, self.start_interval, [target, interval]).start()


