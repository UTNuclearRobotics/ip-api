# IP-API

This is a simple API to interact with a MongoDB database to store and lookup IP addresses based on a machine's hostname. This is intended for storing and querying ROS IPs to make remote connections easier to set up (specifically when robot IPs are not static). This uses MongoDB Data API endpoints; the setup will assume you have a MongoDB collection set up with a Data API endpoint and key (see https://www.mongodb.com/docs/atlas/app-services/data-api/generated-endpoints/ for more information)

NOTE: If multiple machines have the same hostname there will be conflicts. Right now this only supports having unique hostnames.

## Setup

First install any required packages:

`pip install -r requirements.txt`

Next enter your MongoDB database information in `config.yaml` (NRG users see: https://wikis.utexas.edu/x/l47xFg)

```
CLUSTER: 'your cluster name'
DATABASE: 'your database name'
COLLECTION: 'your collection name'
DATA_API_ENDPOINT: 'your API endpoint'
DATA_API_KEY: 'your API Key'
```

The following are useful to add to your .bashrc script (please modify the directory path to where you clone this repository):

```
export IP_API_DIR='THIS_DIRECTORY_PATH'

alias iplocal='python ${IP_API_DIR}/ip-api.py local'
alias iplist='python ${IP_API_DIR}/ip-api.py list'
alias iplookup='python ${IP_API_DIR}/ip-api.py lookup'
alias ipupdate='python ${IP_API_DIR}/ip-api.py update'
```

For the remote machine:
```
export ROS_MASTER_URI=http://$(iplookup ROBOT_HOSTNAME):11311
export ROS_IP=$(iplocal)
```

For the onboard machine (recommended to put this in a startup script):
```
ipupdate # update robot's hostname and ip in database
export ROS_MASTER_URI=http://$(iplocal):11311
export ROS_IP=$(iplocal)
```

## Usage
If you set up the bash aliases, the following commands are available to you:

`iplocal` returns your local ip address without any other information. Equivalent to `python ip-api.py local`.

`iplist` lists all hostnames and ip addresses in the database. Equivalent to `python ip-api.py list`

`iplookup (hostname)` returns the ip address of the specified hostname if it is stored in the database. Equivalent to `python ip-api.py lookup (hostname)`.

`ipupdate` updates your hostname and ip address in the database. Equivalent to `python ip-api.py update`.

These can be used with other commands, for example:
`ping $(iplookup hostname)`
