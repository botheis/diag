import os, sys

import diag.utils as utils
from diag.diagnosticManager import DiagnosticManager

from diag.loader import load_options

# Launcher
if __name__ == "__main__":
    # Load args
    parser = load_options()
