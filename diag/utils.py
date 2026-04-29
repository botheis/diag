from configparser import ConfigParser
import os, sys
import psutil
import subprocess

def get_config(path, local=".local"):
    config = None
    if os.path.exists(path):
        config = ConfigParser()
        with open(path, "r") as f:
            config.read_file(f)
    else:
        return None

    localfile = path+local

    if os.path.exists(localfile):
        # Override loaded config with local one
        with open(localfile, "r") as f:
            config.read_file(f)

    return config

def project_dir():
    return os.path.dirname(os.path.abspath(__file__))

def user_dir():
    return os.path.expanduser("~")

def is_admin():
    return os.geteuid() == 0

def service_running(name):
    if sys.platform == "linux":
        # Check if a service is running by looking for its PID file
        cmd = "systemctl is-active --quiet {}".format(name)
        result = subprocess.run(cmd, shell=True)
        if result.returncode == 0:
            return True
        return False

    elif sys.platform == "darwin":
        # Check if a service is running by looking for its launchd plist
        plistfile = f"/Library/LaunchDaemons/{name}.plist"
        return os.path.exists(plistfile)
    elif sys.platform == "win32":
        # Check if a service is running using psutil
        service = None
        try:
            service = psutil.win_service_get(name)
            service = service.as_dict()
        except:
            return False
        if service and service["status"] == "running":
            return True
        else:
            return False
    else:
        return False
