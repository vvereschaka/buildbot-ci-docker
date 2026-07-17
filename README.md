
A collection of Docker files for the llvm-project Buildbot Workers 
==================================================================

This is a brief description who to configure and build the docker containers for
the buildbot workers.

(!) Note: this is a very first instruction and it will be dramatically changed later.

## Clean up Docker builder cache

After many experiments it is optimal to clean up the builder cache. That could avoid a lot of the problems.

```bash
sudo docker builder prune -a -f
sudo systemctl restart docker
```

## Getting the Docker and Composser files. 

```bash
cd /var/opt
sudo git clone https://github.com/vvereschaka/buildbot-ci-docker.git
cd buildbot-ci-docker
```

## Build content preparation.

Because of security reasons, we have access only to the content in the same folder (and subfolder) as rooted `Dockerfile` file. So, we need to do some preparation before build the container image and copy and create all necessary file at the root of the repo (todo:?)

```bash
sudo mkdir -p .build-context && cd .build-context && sudo rm -rf *
sudo cp -f ../llvm-project/ubuntu/gcc+ssh/* ./

sudo cp -R ../scripts/ ./
sudo cp -R ../worker/ ./

# for +ssh containers
sudo mkdir ssh
sudo nano ssh/id_ed25519
<add id_ed25519 key data>

sudo nano ssh/id_ed25519.pub
<add id_ed25519.pub key data>

sudo nano ssh/known_hosts
<add known_hosts data>
```

## Build the image

```bash
export WORKERADMIN="$(git config user.name) <$(git config user.email)>"

sudo docker build --progress=plain --build-arg WORKERADMIN="$WORKERADMIN" -t buildbot-worker/llvm-project/ubuntu:gcc-ssh .
```
and check the image existence

```bash
$ sudo docker images

IMAGE                                          ID             DISK USAGE   CONTENT SIZE   EXTRA
buildbot-worker/llvm-project/ubuntu:gcc-ssh   fc56faf6d243       1.69GB             0B
```

## Create worker password file

For some reason, Docker does not allow to create the secrets within `/var` folder. We need to create the password filesomewhere else, at the `root` home directory as example.

```bash
echo "<worker-pwd>" | sudo tee /root/worker_password.txt
```

## Run containers with Docker composer

to run all workers with the docker composer run the following command
```bash
sudo docker compose -f docker-compose/compose-as-builder-11.prod.yaml up -d
```

to stop it
```
sudo docker compose -f docker-compose/compose-as-builder-11.prod.yaml down
```
