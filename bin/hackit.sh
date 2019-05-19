#!/bin/bash
# Start Mongo
/usr/bin/mongod -f /etc/mongod.conf

# Start our web server
nginx

# Start the backend process
cd /var/www && /usr/bin/python3 /var/www/callcenterV2.py &

# Start the frontend site (React)
cd /var/www/WebApi/app/templates && npm start &

# Start the API
/usr/bin/python3 /var/www/WebApi/run.py