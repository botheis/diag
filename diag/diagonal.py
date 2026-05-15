from argparse import ArgumentParser
import os, sys
import logging
from diag.manager import DiagnosticManager
from diag.errors import *
from diag import utils
import importlib.util

logging.basicConfig(level=logging.INFO)


class Diagonal:
    # args priority order: handle the parameters in this order
    args_resolution_order = ["help", "report", "diag", "list", "run"]
    logger_configured = False

    def __init__(self, argv, manager):
        """Instanciate the Diagonal class.
        Args:
            argv (list): The list of arguments to parse. It corresponds to the command line arguments.
            manager (DiagnosticManager): The diagnostic manager instance to use.
        """

        if argv is None:
            raise DiagonalError(DIAGONAL_INVALID_NONE_ARGS)

        if isinstance(argv, list) is False:
            raise DiagonalError(DIAGONAL_INVALID_TYPE_ARGS)

        if manager is None:
            raise DiagonalError(DIAGONAL_INVALID_NONE_MANAGER)
        
        if isinstance(manager, DiagnosticManager) is False:
            raise DiagonalError(DIAGONAL_INVALID_TYPE_MANAGER)

        self.logger = logging.getLogger()

        self.manager = manager
        self.manager.logger = self.logger

        self.argv = argv
        self.parser = ArgumentParser(prog="Diagnostic", description="Help to diagnose issues based on your tests.")
        
        self.__paths = {
            "project": utils.project_dir(),
            "report": os.path.join(utils.user_dir(), "diag.log"),
            "diagnostics": os.path.join(utils.project_dir(), "diagnostics"),
        }

    def configure_logger(self, log_path):
        """Configure the logger to write to the specified log file path.
        Args:
            log_path (str): The file path where the log should be saved.
        """

        if Diagonal.logger_configured:
            return

        if log_path == None:
            raise DiagonalError(DIAGONAL_INVALID_NONE_PATH)

        if isinstance(log_path, str) is False:
            raise DiagonalError(DIAGONAL_INVALID_TYPE_PATH)

        if log_path == "":
            raise DiagonalError(DIAGONAL_INVALID_NONE_PATH)

        logging.shutdown()
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        Diagonal.logger_configured = True
        self.logger = logger
        self.manager.logger = logger

    def paths(self):
        """Get the paths dictionary containing the project, report and diagnostics paths.
        
        Returns:
            dict: A dictionary with keys "project", "report" and "diagnostics" and their corresponding paths as values.
        """
        return self.__paths

    def path(self, name, value=None):
        """ Get or set a specific path by name.
        Args:
            name (str): The name of the path to get or set. It should be one of "project", "report" or "diagnostics".
            value (str, optional): The new value for the path. If None, the method will return the current value of the path. If not None, it will set the path to the new value.
        Returns:
            str: (get mode) The current value of the path or None if no value
            None (set mode).
        """
        if name is None:
            raise DiagonalError(DIAGONAL_INVALID_PATH)

        if value is None:
            return self.__paths.get(name, None)
        else:
            self.__paths[name] = value

    def has_path(self, name):
        """Check if a specific path exists by name.
        Args:
            name (str): The name of the path to check. It should be one of "project", "report" or "diagnostics".
        Returns:
            bool: True if the path exists, False otherwise.
        """
        if name is None:
            raise DiagonalError(DIAGONAL_INVALID_PATH)
        return name in self.__paths

    def unpath(self, name):
        """Remove a specific path by name.
        Args:
            name (str): The name of the path to remove. It should be one of "project", "report" or "diagnostics".
        """
        if name is None:
            raise DiagonalError(DIAGONAL_INVALID_PATH)

        if name in self.__paths:
            del self.__paths[name]

    def add_argument(self, name, **kwargs):
        """Push a new argument to the argument parser.
        Args:
            name (str): The name of the argument to add. It should be a valid argument name for argparse (e.g., "--list", "--run", etc.).
            **kwargs: Additional keyword arguments to pass to the add_argument method of the ArgumentParser instance (see argparse.ArgumentParser.add_argument).
        """
        self.parser.add_argument(name, **kwargs)

    @property
    def _exec(self):
        """Execute the diagonal by parsing the arguments and executing the corresponding actions based on the defined resolution order.

        Returns:
            int: The exit code of the execution (0 for success, non-zero for errors).
        """

        self.parser.parse_args(self.argv)

        for action in Diagonal.args_resolution_order:
            if hasattr(self.parser.parse_args(), action):
                value = getattr(self.parser.parse_args(), action)
                if hasattr(self, action):
                    method = getattr(self, action)
                    try:
                        method(value)
                    except Exception as e:
                        self.logger.error(f"Error executing {action} with value {value}: {str(e)}")
                        return 1
            continue

        return 0

    #
    # args executor
    #

    @staticmethod
    def executor(fnc):
        """Decorator launched before to execute an argument action. It logs the execution of the action and its value.

        Args:
            fnc (function): The function to decorate. It should be a method of the Diagonal class that corresponds to an argument action (e.g., list, run, diag, report).
        Returns:
            function: The decorated function that will log the execution of the action and its value before executing the original function.
        """

        def wrapper(self, *args, **kwargs):
            # Add Some logs before execution of the method
            self.logger.debug(f"==== {fnc.__name__} ====")
            self.logger.debug(f"Executing {fnc.__name__} with value: {args[0] if args else None}")
            return fnc(self, *args, **kwargs)
        return wrapper

    @executor
    def list(self, value=None):
        """List all available diagnostics. It takes account on loaded and selected diagnostics.
        Args:
            value (bool, optional): If True, it will list the diagnostics. If False, it will skip the listing. Default is None (which is treated as False).
        """

        if value is False:
            self.logger.debug("skip ...")
            return
        self.logger.info(f"List of diagnostics : ")
        if len(self.manager.list) == 0:
            self.logger.info("\tNo diagnostics available.")
        else:
            for element in self.manager.list:
                self.logger.info("\t- " + element)

        # Do nothing more.
        return 0

    @executor
    def run(self, value=None):
        """Select diagnostics by name and run it. If the name is not found, it will run all diagnostics that start with that name.
        Args:
            value (str, optional): The name of the diagnostic to run. If None or empty, it will run all diagnostics. If it starts with "^", it will run the specific diagnostic with the exact name (without the "^"). If it does not start with "^", it will run all diagnostics that start with the given name. Default is None."""

        # First case : no value : run all diagnostics
        if value is None or value == "":
            diagnostics = self.manager.list
            if len(diagnostics) == 0:
                self.logger.info("No diagnostics to run.")
            else:
                for name in diagnostics:
                    return self.manager.run(name)

        # Second case : normal use: run diagnostics that start with the value
        else:
            if value.startswith("^") is False:
                diagnostics = [x for x in self.manager.list if x.startswith(value)]
                if len(diagnostics) == 0:
                    self.logger.info("No diagnostics to run.")
                else:
                    for name in diagnostics:
                        if name.startswith(value):
                            return self.manager.run(name)
            # Third case: run specific diagnostic
            else:
                value = value[1:]
                if self.manager.has(value):
                    return self.manager.run(value)
                else:
                    self.logger.info("No diagnostics to run.")
            return 0

    @executor
    def diag(self, value=None):
        """Specify the diagnostic path (directory) to load. If not specified, it will load all diagnostics in the diagnostic folder.
        Args:
            value (str, optional): The path to the diagnostics directory. If None, it will use the default diagnostics path defined in the paths dictionary. Default is None.
        """

        if value is None:
            value = self.path("diagnostics")

        if os.path.exists(value) and os.path.isdir(value):
            self.path("diagnostics", value)
        
        for root, dirs, files in os.walk(self.path("diagnostics")):
            if root.endswith("__pycache__"):
                continue
            dirs = [d for d in dirs if d != "__pycache__"]
            files = [f for f in files if f != "__init__.py" and f.endswith(".py")]

            # Full path for module
            
            for file in files:
                self.logger.info(f"Loading diagnostics modules from {os.path.join(root, file)}")

                module_name = os.path.splitext(file)[0]
                module_path = os.path.join(root, file)

                _module_spec = importlib.util.spec_from_file_location(module_name, module_path)
                _module = importlib.util.module_from_spec(_module_spec)
                _module_spec.loader.exec_module(_module)

    @executor
    def report(self, value=None):
        """
        Specify the report path (file) to save the report. If not specified, it will be saved in /var/log/diag.log.
        Args:
            value (str, optional): The path to the report file. If None, it will use the default report path defined in the paths dictionary. Default is None.
        """
        # Default log file
        if value is None or value == "":
            self.configure_logger(self.path("report"))
            self.reset_report()
            self.logger.info(f"Report will be saved into {self.path('report')}")
            return
        else:
            # Save the report to the specified file path
            existing = os.path.exists(value)
            # Case 1 path exists
            if existing:
                if os.path.isfile(value):
                    self.path("report", value)

                if os.path.isdir(value):
                    self.path("report", os.path.join(value, "diag.log"))
            # Case 2 path does not exist, the parent directory exists: set the new path
            else:
                if os.path.isdir(os.path.dirname(value)):
                    self.path("report", value)

            self.configure_logger(self.path("report"))
            self.logger.info(f"Report will be saved into {self.path('report')}")
            self.reset_report()

    def reset_report(self):
        """Reset the report file by clearing its content. It will create the file if it does not exist.
        """
        report_path = self.path("report")
        with open(report_path, 'w') as fb:
            fb.close()
