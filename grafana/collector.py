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
            start = time.time()
            r = requests.get(target)
            end = time.time()

            if(r.status_code != 200 or not  ('application/json' in r.headers.get('content-type'))):
                print('response: failed')
                time.sleep(300)
                raise Exception(r.status_code, r.headers.get('content-type')) 
            
            data = r.json()
            delay = (int)(1000*(end -start))
            delay_string = str(delay)
            if("middleware" in target):
                data["no_middleware_request_delay"] = delay
                delay_string += " middleware"
            else:
                data["request_delay"] = delay

            if(delay>500):
                print(time.ctime() + " - " + str(r.status_code) + " - [" + delay_string + "]")

            self.db.execute(data)
                
        except (Exception) as error:
            print("Exception:", error)
            time.sleep(300)
        finally:
            threading.Timer(interval, self.start_interval, [target, interval]).start()


