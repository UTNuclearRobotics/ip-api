import yaml
import requests
import os
import sys
import subprocess
from socket import gethostname

with open("config.yaml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
        data_source = config['CLUSTER']
        database = config['DATABASE']
        collection = config['COLLECTION']
        url_prefix = config['DATA_API_ENDPOINT'] + '/action/'
        api_key = config['DATA_API_KEY']
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit(1)

headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}


def request(action, data):
    return requests.post(url_prefix+action, headers=headers, json=data)


def local():
    return subprocess.getoutput("ifconfig | grep -A 1 'w' | tail -1 | cut -c 14- | cut -d ' ' -f 1")


def list():
    data = {
        "dataSource": data_source,
        "database": database,
        "collection": collection,
        "sort": {"name": 1}
    }
    response = request("find", data)

    if response.status_code == 200:
        for item in response.json()['documents']:
            print(item['name'], ':', item['ip'])


def lookup(hostname):
    data = {
        "dataSource": data_source,
        "database": database,
        "collection": collection,
        "filter": {"name": hostname}
    }
    response = request("findOne", data)
    if response.status_code == 200:
        if (response.json()['document']):
            print(response.json()['document']['ip'])


def update():
    hostname = gethostname()
    ip = local()
    data = {
        "dataSource": data_source,
        "database": database,
        "collection": collection,
        "filter": {"name": hostname},
        "update": {
            "name": hostname,
            "ip": ip
        },
        "upsert": True
    }

    response = request("updateOne", data)
    if response.status_code == 200:
        print("Updated lookup table with", hostname, ":", ip)


if __name__ == '__main__':
    if (len(sys.argv) > 1):
        command = os.path.basename(sys.argv[1])

        if command == 'local':
            print(local())
        elif command == 'list':
            list()
        elif command == 'lookup':
            if len(sys.argv) > 2:
                lookup(sys.argv[2])
        elif command == 'update':
            update()
        else:
            print("Invalid command")
