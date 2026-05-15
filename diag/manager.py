import logging
import os, sys
from datetime import datetime

from diag.errors import *
import diag.utils as utils
from diag.diagnostic import Diagnostic



class DiagnosticManager:
    def __init__(self):
        self.diagnostics = {}
        self.logger = None
        self.storage = {}

    # Related to diagnostics
    def register(self, name, diagnostic):
        if name == None or name == "":
            raise DiagnosticManagerError(MANAGER_INVALID_EMPTY_NAME)
        
        if name in self.diagnostics:
            raise DiagnosticManagerError(MANAGER_INVALID_USED_NAME)

        if diagnostic == None:
            raise DiagnosticManagerError(MANAGER_INVALID_EMPTY_INSTANCE)

        if not isinstance(diagnostic, Diagnostic):
            raise DiagnosticManagerError(MANAGER_INVALID_TYPE_INSTANCE)

        self.diagnostics[name] = diagnostic

    @property
    def list(self):
        return self.diagnostics.keys()

    def get(self, name):
        if name not in self.diagnostics:
            raise DiagnosticManagerError(MANAGER_INVALID_UNKNOWN_NAME)
        return self.diagnostics[name]

    def has(self, name):
        return name in self.diagnostics
    
    def set(self, name, diagnostic):
        if name not in self.diagnostics:
            raise DiagnosticManagerError(MANAGER_INVALID_UNKNOWN_NAME)
        self.diagnostics[name] = diagnostic

    def run(self, name):
        if name not in self.diagnostics:
            raise DiagnosticManagerError(MANAGER_INVALID_UNKNOWN_NAME)

        diagnostic = self.get(name)
        if diagnostic is None:
            raise DiagnosticManagerError(MANAGER_INVALID_EMPTY_INSTANCE)

        if diagnostic.count > 0:
            self.logger.info(f"diagnostic {diagnostic.register_name} already launched : skip ...")
            return
            
        if diagnostic is not None:
            # Find and launch deps before launch the main diagnostic
            for dep in diagnostic.dependencies:
                self.run(dep)

            diagnostic.run()
            diagnostic.count += 1

    # Related to storage
    def store(self, key, value=None):
        if value is None:
            return self.storage.get(key, None)
        self.storage[key] = value

    def unstore(self, key):
        if key in self.storage:
            del self.storage[key]
    
    def hasstore(self, key):
        return key in self.storage
