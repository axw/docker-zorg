# This file is based on the Dockerfile from buildbot, modified to support
# LLVM's zorg framework. See README for instructions.

FROM ubuntu:14.04
MAINTAINER Andrew Wilkins <axwalk@gmail.com>

# Comments below are from the buildbot Dockerfile.

# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members
#
#
# VERSION         1.1
# DOCKER_VERSION  0.6.1-dev
# AUTHOR          Daniel Mizyrycki <daniel@dotcloud.com>
# DESCRIPTION     Build buildbot tutorial into a runnable linux container
#                 with all dependencies installed as a playground sandbox

# Install buildbot and its dependencies, compiler toolchains and build tools.
run /bin/echo -e "\
    deb http://archive.ubuntu.com/ubuntu trusty main universe\n\
    deb http://archive.ubuntu.com/ubuntu trusty-updates main universe" > \
    /etc/apt/sources.list
run apt-get update
run DEBIAN_FRONTEND=noninteractive apt-get install -y python-pip python-dev \
    supervisor sudo ssh subversion git
run DEBIAN_FRONTEND=noninteractive apt-get install -y cmake gcc g++ gccgo
run pip install sqlalchemy==0.7.9 buildbot==0.8.5 buildbot_slave==0.8.5 twisted==12.0.0

# Install Ninja.
run cd /tmp && git clone git://github.com/martine/ninja.git
run cd /tmp/ninja && ./configure.py --bootstrap
run cp /tmp/ninja/ninja /usr/local/bin

# Install Go
run cd /tmp && wget https://storage.googleapis.com/golang/go1.4.2.linux-amd64.tar.gz
run cd /usr/local && tar xzf /tmp/go1.4.2.linux-amd64.tar.gz
run ln -s /usr/local/go/bin/go /usr/local/bin/go

# Set ssh superuser (username: admin   password: admin)
run mkdir /data /var/run/sshd
run useradd -m -d /data/buildbot -p sa1aY64JOY94w admin
run sed -Ei 's/adm:x:4:/admin:x:4:admin/' /etc/group
run sed -Ei 's/(\%admin ALL=\(ALL\) )ALL/\1 NOPASSWD:ALL/' /etc/sudoers

# Create buildbot configuration
run cd /data/buildbot; sudo -u admin sh -c "buildbot create-master master"
run cd /data/buildbot; sudo -u admin sh -c \
    "buildslave create-slave slave localhost:9989 local-slave pass"
copy master.cfg /data/buildbot/master/
copy config /data/buildbot/master/config/
copy zorg /data/buildbot/master/zorg/

# Set supervisord buildbot and sshd processes
copy supervisord-conf/sshd.conf /etc/supervisor/conf.d/sshd.conf
copy supervisord-conf/buildbot.conf /etc/supervisor/conf.d/buildbot.conf

# Setup running docker container buildbot process
# Make host port 8010 match container port 8010
expose :8010
# Expose container port 22 to a random port in the host.
expose 22
cmd ["/usr/bin/supervisord", "-n"]
