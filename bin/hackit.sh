#!/bin/bash
# Start Mongo
/usr/bin/mongod -f /etc/mongod.conf

# Start the backend process
/usr/bin/python3 /var/www/callcenter.py &

# Start the API
/usr/bin/python3 /var/www/WebApi/run.py