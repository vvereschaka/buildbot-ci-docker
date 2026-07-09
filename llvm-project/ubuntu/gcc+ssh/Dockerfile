# syntax=docker/dockerfile:1
#
# llvm-project builder with clang-21/lld-21 packages installed.
#
# To build image for using with docker composer use the following command:
#   cd <repo/root>
#   cp -f llvm-project/ubuntu/gcc+ssh/Dockerfile ./ && \
#   sudo docker build --build-arg WORKERADMIN="<admin name and email>" -t buildbot-worker/llvm-project/ubuntu:gcc+ssh .

FROM ubuntu:24.04

ARG CMAKE_VERSION=3.31.12-0kitware1ubuntu24.04.1

# network address of buildbot master
ARG BUILDMASTER=localhost
# buildmaster port
ARG BUILDMASTER_PORT=9990
ARG BUILDMASTER_PROTOCOL=pb
ARG WORKERNAME=docker-worker
# worker administrator info to put into 'info/admin'
ARG WORKERADMIN="your_name <your_email>"

# findutils - for 'xargs'
RUN apt-get -y update && apt-get install -y ca-certificates gpg wget findutils ssh

# Prepare APT repos
COPY scripts/prepare-apt-repos.sh .
RUN chmod +x prepare-apt-repos.sh && ./prepare-apt-repos.sh

# Installing CMake
RUN apt-get -y update && apt-get install -y --allow-downgrades cmake=${CMAKE_VERSION}

# Installing Python3
RUN apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-wheel \
    python3-venv

# System wide installation of the same modules
#RUN apt install python3-future python3-pexpect python3-psutil python3-setuptools python3-packaging python3-pygments
# lldb project requirements
#RUN apt install swig python3-dev libedit-dev libncurses5-dev libxml2-dev

# Installing build tools
RUN apt install -y build-essential ninja-build ccache git gcc g++ liblzma-dev libz-dev libxml2-dev net-tools

COPY extra-packages.txt .
RUN cat extra-packages.txt | xargs apt-get install -y 

# Installing python packages (including buildbot-worker)
COPY worker/requirements.txt .
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

# Clean up APT database to reduce result image size.
RUN rm -rf /var/lib/apt/lists/*

#
# buildbot worker installation and execution
#
RUN useradd -c "Buildbot Worker" --user-group --groups=cdrom,sudo,dip,plugdev --shell=/bin/bash --home-dir=/home/buildbot --create-home buildbot

# SSH settings for the buildbot account
COPY --chown=buildbot:buildbot ./ssh /home/buildbot/.ssh
RUN chmod 0700 /home/buildbot/.ssh
RUN chmod 0600 /home/buildbot/.ssh/id_ed25519
RUN chmod 0644 /home/buildbot/.ssh/id_ed25519.pub
RUN chmod 0600 /home/buildbot/.ssh/known_hosts

USER buildbot

RUN mkdir -p /home/buildbot/worker

WORKDIR /home/buildbot/worker
RUN mkdir info
RUN cat /etc/lsb-release | grep DISTRIB_DESCRIPTION | cut -d '=' -f 2 | sed 's/\"//g' > info/host
RUN echo ${WORKERADMIN} > info/admin

# Supported environment variables:
# -----------------------------------------------------------
ENV BUILDMASTER=$BUILDMASTER
ENV BUILDMASTER_PORT=$BUILDMASTER_PORT
ENV BUILDMASTER_PROTOCOL=$BUILDMASTER_PROTOCOL
ENV WORKERNAME=$WORKERNAME

#Note: we don't run `buildbot-worker create-worker` here.
# The 'buildbot.tac' already has all required settings inside and uses the environment variables
# to get the custom settings.
COPY worker/buildbot.tac .

ENTRYPOINT ["/usr/local/bin/buildbot-worker"]
CMD ["start", "--nodaemon"]

#CMD ["twistd", "-ny", "buildbot.tac"]
