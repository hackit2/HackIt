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

# Install some utilities for interactive usage
RUN yum -y install less mongodb which

# Start all of the servers
COPY bin/hackit.sh /usr/local/bin/hackit.sh
RUN chmod +x /usr/local/bin/hackit.sh
CMD ["/usr/local/bin/hackit.sh"]

# Let the adoring public see our HackIT stuff
EXPOSE 5000/tcp
EXPOSE 27017/tcp