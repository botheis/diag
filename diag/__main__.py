import os, sys

import diag.utils as utils
from diag.diagonal import Diagonal
# from diag.diagnosticManager import DiagnosticManager
from diag.manager import DiagnosticManager
from diag.diagnostic import Diagnostic

# Launcher
if __name__ == "__main__":

    # Diagonal
    #   - arguments: args api: add, parse, run the 
    #   - manager : diagnostic api: load, run, stop diagnostics
    manager = DiagnosticManager()
    # Link all the diagnostics to the manager
    Diagnostic.set_manager(manager)
    # Link the manager to the diagonal
    diagonal = Diagonal(sys.argv[1:], manager)

    diagonal.add_argument("--list", action="store_true", help="List all available diagnostics. It takes account on loaded and selected diagnostics.")
    diagonal.add_argument("--run", type=str, nargs="?",help="Select diagnostics by name and run it. If the name is not found, it will run all diagnostics that start with that name.")
    diagonal.add_argument("--diag", type=str, help="Specify the diagnostic path (directory) to load. If not specified, it will load all diagnostics in the diagnostic folder.")
    diagonal.add_argument("--report", type=str, help="Specify the report path (file) to save the report. If not specified, it will be saved in /var/log/diag.log.")

    sys.exit(diagonal._exec)
