# IP-API

This is a simple API to interact with a MongoDB database to store and lookup IP addresses based on a machine's hostname. This is intended for storing and querying ROS IPs to make remote connections easier to set up (specifically when robot IPs are not static). This uses MongoDB Data API endpoints; the setup will assume you have a MongoDB collection set up with a Data API endpoint and key (see https://www.mongodb.com/docs/atlas/app-services/data-api/generated-endpoints/ for more information)

NOTE: If multiple machines have the same hostname there will be conflicts. Right now this only supports having unique hostnames.

## Setup

Clone the repository and install required packages:

```bash
git clone git@github.com:UTNuclearRobotics/ip-api.git
cd ip-api/
sudo apt update
sudo apt install net-tools
pip install -r requirements.txt
```

Next enter your MongoDB database information in `config.yaml` (NRG users see: https://wikis.utexas.edu/x/l47xFg)

```yaml
CLUSTER: 'your cluster name'
DATABASE: 'your database name'
COLLECTION: 'your collection name'
DATA_API_ENDPOINT: 'your API endpoint'
DATA_API_KEY: 'your API Key'
```

Add the following to your `.bashrc` script. Modify the directory path to where you clone this repository and use python instead of python3 if necessary.

```bash
export IP_API_DIR='THIS_DIRECTORY_PATH'

alias iplocal='python3 ${IP_API_DIR}/ip-api.py local'
alias iplist='python3 ${IP_API_DIR}/ip-api.py list'
alias iplookup='python3 ${IP_API_DIR}/ip-api.py lookup'
alias ipupdate='python3 ${IP_API_DIR}/ip-api.py update'
alias ipinvalidate='python3 ${IP_API_DIR}/ip-api.py invalidate'
```

Resource your .bashrc before continuing.

Run these two commands on the onboard machine to automatically update onboard machine's ip on network connections:
```bash
echo -e '#!/bin/sh'"\n/usr/bin/python3 ${IP_API_DIR}/ip-api.py update" | sudo tee /etc/network/if-up.d/ip-api-update
sudo chmod +x /etc/network/if-up.d/ip-api-update
```

For the onboard machine once connected via SSH (this can be added to .bashrc or create an alias with these):
```bash
export ROS_MASTER_URI=http://$(iplocal):11311
export ROS_IP=$(iplocal)
```

For the remote machine (can be added to .bashrc but may require re-sourcing if robot hasn't updated its ip address yet):
```bash
export ROS_MASTER_URI=http://$(iplookup ROBOT_HOSTNAME):11311
export ROS_IP=$(iplocal)
```

## Usage
If you set up the bash aliases, the following commands are available to you:

1. `iplocal` returns your local ip address. Equivalent to `python3 ip-api.py local`.

2. `iplist` lists all hostnames and ip addresses in the database. Equivalent to `python3 ip-api.py list`

3. `iplookup (hostname)` returns the ip address of the specified hostname if available. Equivalent to `python3 ip-api.py lookup (hostname)`.

4. `ipupdate` updates your hostname and ip address in the database. Equivalent to `python3 ip-api.py update`.

5. `ipinvalidate (optional=hostname)` invalidates your hostname (or the one given as an argument) in the database. Equivalent to `python3 ip-api.py invalidate (optional=hostname)`.

These can be used with other commands, for example:
`ping $(iplookup hostname)`
