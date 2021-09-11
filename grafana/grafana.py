from grafana.collector import Collector
import os
import time

AGENTS=os.getenv('GRAFANA_AGENT_URI').split(',')

def run():
    print('Start grafana collector...')
    collector = Collector()

    for agent in AGENTS:
        print("+ Agent to collect mem usage from:", agent)
        collector.start_interval(agent, 15)
        collector.start_interval(agent + "_without_middleware", 5)
        time.sleep(3)