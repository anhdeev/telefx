from grafana.collector import Collector
import os
import time

AGENTS=os.getenv('GRAFANA_AGENT_URI').split(',')

def run():
    print('Start grafana collector...')
    collector = Collector()

    for agent in AGENTS:
        print("+ Agent to collect mem usage from:", agent)
        collector.start_interval(agent, 10)
        time.sleep(3)