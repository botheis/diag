"""Diagnostic class. Inherit this class to implement a new Diagnostic."""

from diag.errors import *
class Diagnostic:
    manager = None
    log_levels = ["debug", "info", "warning", "error", "fatal"]

    @staticmethod
    def set_manager(manager):
        """Set the manager for the Diagnostic class."""
        if Diagnostic.manager is not None:
            return

        if manager is None:
            raise DiagnosticError(DIAGNOSTIC_INVALID_NONE_MANAGER)

        # Restrictions on circular imports;
        # we cannot import the manager at the top of the file, we can't do too much tests.
        Diagnostic.manager = manager

    def __init__(self):
        """Initialize the Diagnostic instance."""
        self.count = 0
        self.dependencies = []
        self.register_name = "Manager"

    def register(self, name):
        """Register the diagnostic instance into the manager under the given name.

        Args:
            name (str): The name to register the diagnostic.
        """
        self.register_name = name
        self.manager.register(name, self)

    def run(self):
        """Virtual method: override this method to implement the diagnostic logic."""
        pass

    def log(self, level="info", message=""):
        """Log a message to the report file with a specific format.

        Args:
            level (str): The severity level of the log message (e.g., "info", "warning", "error").
            message (str): The content of the log message.
        """
        if self.manager is None:
            raise DiagnosticError(DIAGNOSTIC_MANAGER_NOT_SET)

        # Get the logging.getLogger.level method based on the level string
        if hasattr(self.manager.logger, level):
            logger = getattr(self.manager.logger, level)

        if logger is None:
            raise DiagnosticError(MANAGER_LOGGER_NOT_SET)
        logger(f"{self.register_name} - {message}")
