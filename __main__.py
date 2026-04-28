import os, sys

import mmc_diag.utils as utils
from mmc_diag.diagnosticManager import DiagnosticManager

from mmc_diag.loader import load_options
from mmc_diag.loader import load_diagnostics

def list_diagnostics():
    print("Available diagnostics:")
    for name in DiagnosticManager().diagnostics.keys():
        print(f" - {name}")

# Launcher
if __name__ == "__main__":
    # Load args
    parser = load_options()

    diagnostic_path = parser.parse_args().diag
    diagnostic_path = diagnostic_path if diagnostic_path is not None else ""
    # Load diagnostics
    load_diagnostics(diagnostic_path)

    report_path = "/var/log/mmc/diag.log"
    if parser.parse_args().report != None:
        report_path = DiagnosticManager().report_path
    
    DiagnosticManager().logger.info(f"Report will be saved into {DiagnosticManager().report_path}")


    if parser.parse_args().list:
        list_diagnostics()
    else:
        name = parser.parse_args().run
        DiagnosticManager().run(name)
