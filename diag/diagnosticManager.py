import logging
import os, sys
import diag.utils as utils
from datetime import datetime

logger = logging.getLogger()

class DiagnosticManager:
    instance = None
    connectors = {}
    diagnostics = {}
    _store = {}
    running = True

    reports = []
    paths = {
        "report": os.path.join(utils.user_dir(), "diag.log"),
        "diagnostic": os.path.join(utils.project_dir(), "diagnostic"),
        "connector": os.path.join(utils.project_dir(), "connector")
    }

    def __new__(cls):
        """Singleton pattern implementation

        Args:
            cls (DiagnosticManager): The class itself

        Returns:
            DiagnosticManager: The singleton instance of the class"""

        if cls.instance is None:
            cls.instance = super(DiagnosticManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        """Initialize the DiagnosticManager instance.

        Args:
            self (DiagnosticManager): The instance itself"""
        self.logger = logger

    def register(self, name, diagnostic):
        """Register a diagnostic with the manager.

        Args:
            name (str): The name of the diagnostic
            diagnostic (Diagnostic): The diagnostic instance to register"""

        if name is None or name == "" or diagnostic is None:
            return
        self.diagnostics[name] = {
            "diagnostic": diagnostic,
            "count": 0,
            "result": None
        }

    def run(self, name=""):
        """Run diagnostics. If the name is empty, run all the diagnostics. Else run the diagnostics that start with the specific name.

        Args:
            name (str, optional): Diagnostic name. Defaults to "".

        Note:
            It implies there is no order on diagnostics execution. Probably you want to run diagnostics in specific order.
            - In that case, you can create "basic" diagnostic and launch it manually.
            - An another option is to play with the diagnostic names when registering them by calling a specific diagnostic name i.e.: dependency.my.
            Later, when you need to call dependency diagnostic, you can call DiagnosticManager.run("dependency.my")
        """
        self.reset_report()

        for _name, diag in self.diagnostics.items():
            if self.running is False:
                break
            if name is not None:
                if _name.startswith(name):
                    if diag["count"] == 0:
                        diag["result"] = diag["diagnostic"].run()
                        diag["count"] += 1
                        self.report(_name, diag["diagnostic"])
                    else:
                        continue
            else:
                if diag["count"] == 0:
                    diag["result"] = diag["diagnostic"].run()
                    diag["count"] += 1
                    self.report(_name, diag["diagnostic"])
                else:
                    continue


    def stop(self, level="info", content="Stop ordered by user"):
        """Stop the diagnostic manager and push a report of the reason

        Args:
            level (str, optional): The level of the report. Defaults to "info".
            content (str, optional): The content of the report. Defaults to "Stop ordered by user".
        """
        timing = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.push_report(timing, "Manager", level, content)
        sys.exit(1)

    def get_path(self, name):
        """Get the path of a specific name.

        Args:
            name (str): The name of the path to retrieve.

        Returns:
            str: The path associated with the given name, or an empty string if not found.
        """
        return self.paths.get(name, "")

    def check_path(self, name, mode="strict"):
        """Check if the path associated with the given name exists.

        Args:
            name (str): The name of the path to check.
            mode (str, optional): The mode of checking. Defaults to "strict".
                - "strict": Check if the exact path exists.
                - "parent": Check if the parent directory of the path exists.
        Returns:
            bool: True if the path (or its parent, depending on the mode) exists, False otherwise.
        """
        path = self.get_path(name)
        if path == "":
            return False

        # Strict mode check the exact path
        # Parent mode check the parent path

        if mode == "strict":
            return os.path.exists(path)
        elif mode == "parent":
            return os.path.exists(os.path.dirname(path))
        else:
            return False

    def set_path(self, name, _path, mode="strict"):
        """Set the path for a specific name.

        Args:
            name (str): The name of the path to set.
            _path (str): The path to set.
            mode (str, optional): The mode of checking. Defaults to "strict".
                - "strict": Check if the exact path exists.
                - "parent": Check if the parent directory of the path exists.
        """
        # Path can't be empty or None
        if _path is None or _path == "":
            return

        if self.check_path(name, mode=mode) is False:
            return
        self.paths[name] = _path

    def get_connector(self, name):
        """Get a connector by name.

        Args:
            name (str): The name of the connector to retrieve.

        Returns:
            Connector: The connector associated with the given name, or None if not found.
        """
        return self.connectors.get(name, None)

    def set_connector(self, name, connector):
        """Set a connector by name.

        Args:
            name (str): The name of the connector to set.
            connector (Connector): The connector instance to associate with the given name.
        """
        if name is None or name == "" or connector is None:
            return
        self.connectors[name] = connector


    def get_diagnostic(self, name):
        """Get a diagnostic by name.

        Args:
            name (str): The name of the diagnostic to retrieve.

        Returns:
            Diagnostic: The diagnostic associated with the given name, or None if not found.
        """
        return self.diagnostics.get(name, None)

    def has_diagnostic(self, name):
        """Check if a diagnostic with the given name exists.

        Args:
            name (str): The name of the diagnostic to check.

        Returns:
            bool: True if the diagnostic exists, False otherwise.
        """
        return name in self.diagnostics

    def diagnostic_get_count(self, name):
        """Get the count of a diagnostic by name.

        Args:
            name (str): The name of the diagnostic.

        Returns:
            int: The count of the diagnostic, or -1 if not found.
        """
        diag = self.diagnostics.get(name, None)

        if diag is not None:
            return diag["count"]
        return -1

    def diagnostic_set_count(self, name, count):
        """Set the count of a diagnostic by name.

        Args:
            name (str): The name of the diagnostic.
            count (int): The count to set.

        Returns:
            bool: True if the count was set successfully, False otherwise.
        """
        diag = self.diagnostics.get(name, None)
        if diag is not None:
            diag["count"] = count
            return True
        return False

    def diagnostic_get_result(self, name):
        """Get the result of a diagnostic by name.

        Args:
            name (str): The name of the diagnostic.

        Returns:
            any: The result of the diagnostic, or None if not found.
        """
        diag = self.diagnostics.get(name, None)
        if diag is not None:
            return diag["result"]
        return None

    def store(self, key="", value=None):
        """Store or retrieve a value in the internal store.

        Args:
            key (str, optional): The key to store or retrieve. Defaults to "".
            value (any, optional): The value to store. If None, the method will retrieve the value associated with the key.

        Returns:
            any: The value associated with the key if retrieving, or the entire store if no key is provided.
        """
        if key == "":
            return self._store

        if value is None:
            return self._store.get(key, None)
        self._store[key] = value

    def unstore(self, key):
        """Remove a key-value pair from the internal store.

        Args:
            key (str): The key to remove from the store.
        """
        if key in self._store:
            del self._store[key]

    def reset_report(self):
        """Reset the report file by clearing its contents. The file is opened and closed in this method."""
        with open(self.get_path("report"), "w") as f:
            f.close()

    def push_report(self, timing, name, level, content):
        """Push a line into the report file.
        Args:
            timing (str): The datetime of the event
            name (str): The (registered) name of the diagnostic
            level (str): The level of the report (e.g., "info", "warning", "error")
            content (str): The content of the report
        Note:
            The file is opened and closed each time this method is called.
            So use it on specific circumstances.
        """
        with open(self.get_path("report"), "a") as f:
            f.write(f"{timing} - {name} - {level} - {content}\n")
            f.close()

    def report(self, name, diagnostic):
        """Save the diagnostic report into the report path.
        Args:
            name (str): The name of the diagnostic
            diagnostic (Diagnostic): The diagnostic instance to report

        Note:
            The file is opened once then all the datas are added into it.
        """
        # Save the diagnostic report into the report path
        with open(self.get_path("report"), "a") as f:
            for item in self.reports:
                f.write(f"{item['datetime']} - {name} - {item['level']} - {item['message']}\n")
            f.close()

    def __del__(self):
        """Destructor for the DiagnosticManager instance."""
        for element in self.connectors.values():
            try:
                element.close()
            except:
                continue


class Diagnostic:

    manager = DiagnosticManager()
    def __init__(self):
        """Initialize the Diagnostic instance."""
        self.logger = logger
        self.report = []
        self.count = 0
        self.dependencies = []

    def register(self, name):
        """Register the diagnostic instance into the manager under the given name.

        Args:
            name (str): The name to register the diagnostic.
        """
        Diagnostic.manager.register(name, self)

    @staticmethod
    def run_dependencies(fnc):
        """Decorator to run the dependencies of a diagnostic before executing the decorated function.

        Args:
            fnc (function): The function to decorate.

        Returns:
            function: The decorated function that runs the dependencies before executing the original function.
        """
        def wrapper(self, *args, **kwargs):
            # self.push_report("info", f"Running dependencies for {self.__class__.__name__}")
            for name in self.dependencies:
                self.manager.run(name)
            return fnc(self, *args, **kwargs)
        return wrapper

    @run_dependencies
    def run(self):
        """Virtual method: override this method to implement the diagnostic logic."""
        pass

    def push_report(self, level, message):
        """Push a report entry into the diagnostic's report list.

        Args:
            level (str): The level of the report entry (e.g., "info", "warning", "error").
            message (str): The message of the report entry.

        Note:
            The reports are stored in the diagnostic, but not written directly by him.
            The manager is responsible for writing the report into the file.
        """
        _datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.manager.reports.append({
            "datetime": _datetime,
            "level": level,
            "message": message
        })
