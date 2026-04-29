from argparse import ArgumentParser
import os, sys

import importlib.util

from diag.diagnosticManager import DiagnosticManager

def list_diagnostics():
    """List all available loaded diagnostics."""
    if len(DiagnosticManager().diagnostics) == 0:
        print("No diagnostics available.")
        return

    print("Available diagnostics:")
    for name in DiagnosticManager().diagnostics.keys():
        print(f" - {name}")


def load_diagnostics():
    """Load diagnostics from the diagnostic path. The diagnostic path is set by the --diag option. 
    If not set, it will load all diagnostics in the diagnostic folder."""

    dm = DiagnosticManager()

    # Path exists
    path = dm.get_path("diagnostic")

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

def load_options():
    """Load options for diagnostic stand alone mode."""

    # Parser here
    parser = ArgumentParser(prog="Diagnostic", description="Help to diagnose issues based on your tests.")
    
    parser.add_argument("--list", action="store_true", help="List all available diagnostics. It takes account on loaded and selected diagnostics.")
    parser.add_argument("--run", type=str, nargs="?",help="Select diagnostics by name and run it. If the name is not found, it will run all diagnostics that start with that name.")
    parser.add_argument("--diag", type=str, help="Specify the diagnostic path (directory) to load. If not specified, it will load all diagnostics in the diagnostic folder.")
    parser.add_argument("--report", type=str, help="Specify the report path (file) to save the report. If not specified, it will be saved in /var/log/diag.log.")

    # Parser actions

    # --diag opt handler
    DiagnosticManager().set_path("diagnostic", parser.parse_args().diag, "strict")
    load_diagnostics()

    # --report opt handler
    DiagnosticManager().set_path("report", parser.parse_args().report, "parent")
    DiagnosticManager().logger.info("Report will be saved into %s"%(DiagnosticManager().get_path("report")))

    # --list opt handler
    if parser.parse_args().list:
        list_diagnostics()
        return sys.exit(0)

    # --run opt handler
    # If no run selected, run all diagnostics found.
    name = parser.parse_args().run
    DiagnosticManager().run(name)
