import fnmatch
import os
import sys

from twisted.application import service
from twisted.logger import FilteringLogObserver
from twisted.logger import ILogObserver
from twisted.logger import LogLevelFilterPredicate
from twisted.logger import textFileLogObserver

from buildbot_worker.bot import Worker

# setup worker
basedir = os.environ.get("BUILDBOT_BASEDIR",
    os.path.abspath(os.path.dirname(__file__)))
    
rotateLength = 3000000
maxRotatedFiles = 3

workerdir = basedir

# check for RAMDISK within the worker folder.
if os.path.ismount(f"{basedir}/ramdisk"):
    import distutils.dir_util
    import distutils.dep_util

    basedir = f"{basedir}/ramdisk"
    from_dir = f"{workerdir}/info"
    to_dir = f"{basedir}/info"
    if distutils.dep_util.newer(from_dir, to_dir):
        distutils.dir_util.copy_tree(from_dir, to_dir)


application = service.Application('buildbot-worker')

# log to console
application.setComponent(
    ILogObserver,
    FilteringLogObserver(
        textFileLogObserver(sys.stdout), predicates=[LogLevelFilterPredicate()]
    ),
)

# and worker on the same process!
buildmaster_host = os.environ.get("BUILDMASTER", 'localhost')
port = int(os.environ.get("BUILDMASTER_PORT", 9989))
protocol = os.environ.get("BUILDMASTER_PROTOCOL", 'pb')
workername = os.environ.get("WORKERNAME", 'docker')
passwd_file = os.environ.get("WORKERPASS_FILE")
if passwd_file:
    with open(passwd_file, "r") as f:
        passwd = f.readline().rstrip()
else:
    passwd = os.environ.get("WORKERPASS")

# delete the password from the environ so that it is not leaked in the log
blacklist = os.environ.get("WORKER_ENVIRONMENT_BLACKLIST", "WORKERPASS WORKERPASS_FILE").split()
for name in list(os.environ.keys()):
    for toremove in blacklist:
        if fnmatch.fnmatch(name, toremove):
            del os.environ[name]

keepalive = 600
umask = None
maxdelay = 300
allow_shutdown = None
maxretries = 10
delete_leftover_dirs = False

print(f">>> BUILDMASTER: {buildmaster_host}")
print(f">>> BUILDMASTER_PORT: {port}")
print(f">>> BUILDMASTER_PROTOCOL: {protocol}")
print(f">>> WORKERNAME: {workername}")

s = Worker(buildmaster_host, port, workername, passwd, basedir,
           keepalive, umask=umask, maxdelay=maxdelay, protocol=protocol,
           allow_shutdown=allow_shutdown, maxRetries=maxretries,
           delete_leftover_dirs=delete_leftover_dirs)
s.setServiceParent(application)
