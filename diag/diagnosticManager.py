import logging
import os
import diag.utils as utils

logger = logging.getLogger()

class DiagnosticManager:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(DiagnosticManager, cls).__new__(cls)
        return cls.instance

    diagnostics = {}
    store = {}
    report_path=os.path.join(utils.user_dir(), "diag.log")

    def __init__(self):
        self.logger = logger

    def register(self, name, diagnostic):
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
        """
        self.reset_report()

        for _name, diag in self.diagnostics.items():
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

    def get_diagnostic(self, name):
        return self.diagnostics.get(name["diagnostic"], None)

    def has_diagnostic(self, name):
        return name in self.diagnostics

    def diagnostic_get_count(self, name):
        diag = self.diagnostics.get(name, None)

        if diag is not None:
            return diag["count"]
        return -1

    def diagnostic_set_count(self, name, count):
        diag = self.diagnostics.get(name, None)
        if diag is not None:
            diag["count"] = count
            return True
        return False
    
    def diagnostic_get_result(self, name):
        diag = self.diagnostics.get(name, None)
        if diag is not None:
            return diag["result"]
        return None

    def store(self, key="", value=None):
        if key == "":
            return self.store

        if value is None:
            return self.store.get(key, None)
        self.store[key] = value

    def unstore(self, key):
        if key in self.store:
            del self.store[key]

    def reset_report(self):
        with open(self.report_path, "w") as f:
            f.close()

    def report(self, name, diagnostic):
        # Save the diagnostic report into the report path
        with open(self.report_path, "a") as f:
            for item in diagnostic.report:
                f.write(f"{item['datetime']} - {name} - {item['level']} - {item['message']}\n")


class Diagnostic:

    manager = DiagnosticManager()
    def __init__(self):
        self.logger = logger
        self.report = []

    def register(self, name):
        Diagnostic.manager.register(name, self)

    def run(self):
        pass

    def add_report(self, _datetime, level, message):
        self.report.append({
            "datetime": _datetime,
            "level": level,
            "message": message
        })
