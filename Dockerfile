FROM centos:7

# Update basic system stuff and install EPEL
RUN yum -y update
RUN yum -y install epel-release

# Install Python
RUN yum -y install python36 python36-pip
RUN pip3 install -U pip

# Install nginx
RUN yum -y install nginx
COPY etc/nginx.conf /etc/nginx/nginx.conf

# Install, configure, and start Mongo
RUN yum -y install mongodb-server
COPY etc/mongod.conf /etc/mongod.conf

# Copy our application
RUN mkdir -p /var/www
COPY HackItSolution/ /var/www

# Install Python dependencies
RUN pip3 install -r /var/www/requirements.txt

# Install some utilities for interactive usage
RUN yum -y install less mongodb which vim tmux

# Make tmux great again
COPY etc/tmux.conf /root/.tmux.conf

# Start Node
RUN yum -y install gcc-c++ make
RUN curl -sL https://rpm.nodesource.com/setup_12.x | bash -
RUN yum -y install nodejs

# Install the dependencies for the frontend application
RUN cd /var/www/WebApi/app/templates && npm install

# Start all of the servers
COPY bin/hackit.sh /usr/local/bin/hackit.sh
RUN chmod +x /usr/local/bin/hackit.sh
CMD ["/usr/local/bin/hackit.sh"]

# Let the adoring public see our HackIT stuff
EXPOSE 80/tcp
EXPOSE 443/tcp
EXPOSE 3000/tcp
EXPOSE 5000/tcp
EXPOSE 27017/tcp