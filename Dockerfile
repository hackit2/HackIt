FROM centos:7

# Update basic system stuff and install EPEL
RUN yum -y update
RUN yum -y install epel-release

# Install Python
RUN yum -y install python36 python36-pip
RUN pip3 install -U pip

# Install, configure, and start Mongo
RUN yum -y install mongodb-server
COPY etc/mongod.conf /etc/mongod.conf

# Copy our application
RUN mkdir -p /var/www
COPY HackItSolution/ /var/www

# Install Python dependencies
RUN pip3 install -r /var/www/requirements.txt

# Start all of the servers
CMD ["/usr/bin/mongod", "-f", "/etc/mongod.conf"]
CMD ["/usr/bin/python3", "/var/www/WebApi/run.py"]

# Let the adoring public see our HackIT stuff
EXPOSE 5000