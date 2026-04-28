from configparser import ConfigParser
import os

def get_config(path, local=".local"):
    config = None
    if os.path.exists(path):
        config = ConfigParser()
        config.read(path)
    else:
        return None

    localfile = path+local

    localconfig = None
    if os.path.exists(localfile):
        # Override loaded config with local one
        localconfig = ConfigParser()
        localconfig.read(localfile)

        for section in localconfig.sections():
            for option in localconfig.options(section):
                config.set(section, option, localconfig.get(section, option))
    
    return config

def project_dir():
    return os.path.dirname(os.path.abspath(__file__))

def user_dir():
    return os.path.expanduser("~")

def is_admin():
    return os.geteuid() == 0