#!/bin/bash
/usr/bin/mongod -f /etc/mongod.conf
/usr/bin/python3 /var/www/callcenter.py &
/usr/bin/python3 /var/www/WebApi/run.py