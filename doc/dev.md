Dev Doc
===

This document gives specifications for developers who want to add a new diagnostic to mmc_diag.

# Organization

The project is composed of several important files:
- `loader.py` : used to load diagnostics into diagnostic manager. Also used to load the options. Use this if you want to add a new load function to call into `__main__.py`.
- `diagnosticManager.py` : defines the classes `DiagnosticManager` and `Diagnostic`.
- `utils.py` : common functions and defines. Can be used everywhere.
- `diagnostic/` : this folder contains all diagnostics. You can create new files here to add new diagnostics. You can also create subfolders to organize your diagnostics.

# Diagnostic


## Create basic Diagnostic

The Diagnostic class is a generic class to get access to some functionnalities or to normalize the way to create a diagnostic.

Here is the minimal code to create a diagnostic:

```python
import configparser
import os

from mmc_diag.utils import *
from mmc_diag.diagnosticManager import Diagnostic

class ServiceRunningDiagnostic(Diagnostic):
    def __init__(self):
        super().__init__()
        # Declare here the resources needed by this diagnostic.

    def run(self):
        """Put here what you want to do with your diagnostic.
        """
        pass
```

This is the minimal code to create  diagnostic... But this diagnostic won't be registered.

## Create registered Diagnostic

To create a registered diagnostic, you need to register it with the `DiagnosticManager`. This allows the diagnostic to be managed and executed by the manager.

Here is an example of a registered diagnostic:

```python
class MyDiagnostic(Diagnostic):
    def __init__(self):
        super().__init__()
        # Declare here the resources needed by this diagnostic.

        # register
        self.register("category.sub.sub.my_diagnostic")


    def run(self):
        """Put here what you want to do with your diagnostic.
        """
        pass

# Instanciate your object right after the definition.
MyDiagnostic()
```

Here are two differences:
    - The `register` method is called during initialization.
    - An instance is created right after the definition. This allows to instanciate the object and launch the register method.

## What's the purpose of Basic Diagnostics ?

The purpose of basic (not registered) diagnostic is to be usable by any other diagnostic as a dependency.
The use has to handle by himself the import, instanciation, calls and that's it.

## Why to use the Diagnostic class on basic diagnostics ?

Technically you can create any class without inheriting from Diagnostic.

# DiagnosticManager

# Singleton
The DiagnosticManager is a singleton class that manages all registered diagnostics.
It means you can call several times DiagnosticManager() and you will always get the same instance.

```python
from mmc_diag.diagnosticManager import DiagnosticManager
dm = DiagnosticManager()
dm2 = DiagnosticManager()

print(dm is dm2) # True
```

All diagnostics have access to the diagnostic manager.

# Store

The diagnostic manager gives the user to store / unstore keys-values pairs. The values can be any type of data.
This can be useful to share data between diagnostics.

To get / set value in the manager storage, use the method `store(key="", value=None)`.

- key is empty: return the whole storage.
- key is not empty and value is None: return the value of the key if it exists.
- key is not empty and value is not None: set the value of the key.

```python
from mmc_diag.diagnosticManager import DiagnosticManager
dm = DiagnosticManager()
# Get the whole storage
dm.store()

# Get the my_key value or None
dm.store("my_key")

# Associate the "my_value" value to the "my_key" key
dm.store("my_key", "my_value")
```

