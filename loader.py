from argparse import ArgumentParser
import os, sys

import importlib.util

import mmc_diag.utils as utils

from mmc_diag.diagnosticManager import DiagnosticManager, Diagnostic

def load_diagnostics(path=""):
    dm = DiagnosticManager()

    if path == "":
        print("first case : empty path")
        path = os.path.join(utils.project_dir(), "diagnostic")

    if os.path.exists(path) is False :
        dm.logger.error(f"Diagnstic path '{path}' does not exist.")
        return sys.exit(1)
    if os.path.isdir(path) is False:
        dm.logger.error(f"Diagnstic path '{path}' is not a directory.")
        return sys.exit(1)

    Diagnostic.manager = dm
    for root, dirs, files in os.walk(path):
        if root.endswith("__pycache__"):
            continue
        dirs = [d for d in dirs if d != "__pycache__"]
        files = [f for f in files if f != "__init__.py" and f.endswith(".py")]

        # Full path for module
        
        for file in files:
            module_name = os.path.splitext(file)[0]
            module_path = os.path.join(root, file)

            _module_spec = importlib.util.spec_from_file_location(module_name, module_path)
            _module = importlib.util.module_from_spec(_module_spec)
            _module_spec.loader.exec_module(_module)

            # Load the module


    # dm.register("config.mmc", ConfigMmcDiagnostic(dm))
    # dm.register("config.pulse2-package-server", ConfigPackageServerDiagnostic(dm))

def load_options():
    parser = ArgumentParser(prog="MMC Diagnostics", description="Help to diagnose issues in MMC")
    
    parser.add_argument("--list", action="store_true", help="List all available diagnostics")
    parser.add_argument("--run", type=str, nargs="?",help="Run a specific diagnostic by name. If the name is not found, it will run all diagnostics that start with that name.")
    parser.add_argument("--diag", type=str, help="Specify the diagnostic path to load. If not specified, it will load all diagnostics in the diagnostic folder.")
    parser.add_argument("--report", type=str, help="Specify the report path to save the report. If not specified, it will be saved in /var/log/mmc/diag.log.")
    return parser
