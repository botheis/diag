import logging
import os, sys
from datetime import datetime

from diag.errors import *
import diag.utils as utils
from diag.diagnostic import Diagnostic



class DiagnosticManager:
    def __init__(self):
        """Initialize the DiagnosticManager instance."""
        self.diagnostics = {}
        self.logger = None
        self.storage = {}

    # Related to diagnostics
    def register(self, name, diagnostic):
        """Register a new diagnostic with the given name.

        Args:
            name (str): The name of the diagnostic to register.
            diagnostic (Diagnostic): The diagnostic instance to register.

        Raises:
            DiagnosticManagerError: If the name is empty, already used, or if the diagnostic is invalid.
        """
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
        """Get the list of registered diagnostics.

        Returns:
            list: A list of registered diagnostic names.
        """
        return self.diagnostics.keys()

    def get(self, name):
        """Get the diagnostic instance by name.

        Args:
            name (str): The name of the diagnostic to retrieve.

        Returns:
            Diagnostic: The diagnostic instance associated with the given name.

        Raises:
            DiagnosticManagerError: If the diagnostic with the given name does not exist.
        """

        if name not in self.diagnostics:
            raise DiagnosticManagerError(MANAGER_INVALID_UNKNOWN_NAME)
        return self.diagnostics[name]

    def has(self, name):
        """Check if a diagnostic with the given name exists.

        Args:
            name (str): The name of the diagnostic to check.

        Returns:
            bool: True if the diagnostic exists, False otherwise.
        """
        return name in self.diagnostics
    
    def set(self, name, diagnostic):
        """Set the diagnostic instance for the given name.

        Args:
            name (str): The name of the diagnostic to set.
            diagnostic (Diagnostic): The diagnostic instance to set.

        Raises:
            DiagnosticManagerError: If the diagnostic with the given name does not exist.
        """
        if name not in self.diagnostics:
            raise DiagnosticManagerError(MANAGER_INVALID_UNKNOWN_NAME)
        self.diagnostics[name] = diagnostic

    def run(self, name):
        """Run the diagnostic with the given name.

        Args:
            name (str): The name of the diagnostic to run.

        Raises:
            DiagnosticManagerError: If the diagnostic with the given name does not exist.
        """
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
                # prevent from infinite loop if a diagnostic depends on itself
                if diagnostic.register_name == dep:
                    continue
                self.run(dep)

            diagnostic.run()
            diagnostic.count += 1

    # Related to storage
    def store(self, key, value=None):
        """Store a value in the manager's storage with the given key. If value is None, it will return the stored value for the key.
        Args:
            key (str): The key to store the value under.
            value (any, optional): The value to store. If None, it will return the stored value for the key. Default is None.
        Returns:
            any: The stored value for the key if value is None, otherwise None."""
        if value is None:
            return self.storage.get(key, None)
        self.storage[key] = value

    def unstore(self, key):
        """Remove a value from the manager's storage with the given key.
        Args:
            key (str): The key to remove from storage."""
        if key in self.storage:
            del self.storage[key]
    
    def hasstore(self, key):
        """Check if a value exists in the manager's storage with the given key.
        Args:
            key (str): The key to check in storage.
        Returns:
            bool: True if the key exists in storage, False otherwise."""
        return key in self.storage
