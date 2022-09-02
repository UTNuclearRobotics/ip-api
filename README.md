# IP-API

This is a simple API to interact with a MongoDB database to store and lookup IP addresses based on a machine's hostname. This is intended for storing and querying ROS IPs to make remote connections easier to set up.

## Setup

First install any required packages:

`pip install -r requirements.txt`

Next enter your MongoDB data API endpoint URL and API key in `config.yaml`

```
IP_API_ENDPOINT: 'your API endpoint'
IP_API_KEY: 'your API Key'
```

The following are useful to add to your .bashrc script:

```
export IP_API_DIR="THIS_DIRECTORY"

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

For the onboard machine:
```
ipupdate # update robot's hostname and ip in database
export ROS_MASTER_URI=http://$(iplocal):11311
export ROS_IP=$(iplocal)
```

## Usage
If you set up the bash aliases, the following commands are available to you:

`iplocal` returns your local ip address without any other information

`iplist` lists all hostnames and ip addresses in the database

`iplookup {hostname}` returns the ip address of the specified hostname if it is stored in the database

`ipupdate` updates your hostname and ip address in the database

These can be used with other commands, for example:
`ping $(iplookup ROBOT_HOSTNAME)`
