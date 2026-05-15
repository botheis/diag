Dev Doc
===

This document gives specifications for developers who want to add a new diagnostic to diag.

# Organization

The project is composed of several files and folders:
- `diag.errors` : defines all the error class handler and messages.
- `diag.diagonal.Diagonal` : Defines the app wrapper. Basically loads some args and interprets them. You can derivate this class and add your own command line arguments on the parser, and associate them to an executor.

- `diag.__init__` : declare the diag folder as python module
- `diag.__main__` : declare what to do when the module is called in standalone mode.
- `diag.manager` : defines the class `DiagnosticManager`.
- `diag.diagnostic` : defines the class `Diagnostic`.
- `utils` : common functions and defines. Can be used everywhere.
- `diagnostics/` : default diagnostics folder. You can create new files here to add new diagnostics. But in general it's a bad idea to put personnal code into the lib.
- `tests/` : unit tests.
- `doc/` : the module documentation.


# Several way to use diag
Depending on how you want to use it, you have to define/redefine more or less elements.

## Standalone mode
In my opinion the most common way to use diag is by running it in standalone mode.

In standalone mode, you just have to declare new diagnostics and specify its location with `--diag` option. In this case, you can skip the DiagnosticManager declaration.

## Project mode

In this case your app will play the role of the Diagonal object, which is the app wrapper. It defines args options, and associates them to Diagonal method.

This part can be ommited, if you handle by yourself what to do with the manager.

The real thing starts with the instanciation of your own DiagnosticManager.

**The report is generated all along the execution. It is handled by a classical logger. This logger is setup by the Diagonal object. If you don't use Diagonal, you will have to setup your own logger handlers.**

# DiagnosticManager

## Declaration
If you use diag on your own project, you have to setup a diagnostic manager, and link it to all Diagnostics.
```python
from diag.manager import DiagnosticManager

# Instanciate your manager
dm = DiagnosticManager()

# manager is stored in a static location : visible from all Diagnostics.
Diagnostic.set_manager(dm)
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
from diag.diagnosticManager import DiagnosticManager
dm = DiagnosticManager()
# Get the whole storage
dm.store()

# Get the my_key value or None
dm.store("my_key")

# Associate the "my_value" value to the "my_key" key
dm.store("my_key", "my_value")
```

# Diagnostic

## Create basic Diagnostic

The Diagnostic class is a generic class to get access to some functionnalities or to normalize the way to create a diagnostic.

Here is the minimal code to create a diagnostic:

```python
import configparser
import os

from diag.utils import *
from diag.diagnostic import Diagnostic

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
from diag.diagnostic import Diagnostic

class MyDiagnostic(Diagnostic):
    def __init__(self):
        super().__init__()
        # Declare here the resources needed by this diagnostic.

        # register this diagnostic as 'category.sub.sub.my_diagnostic'
        self.register("category.sub.sub.my_diagnostic")

    def run(self):
        """Put here what you want to do with your diagnostic.
        """
        pass

# Instanciate your object right after the definition.
# We need it to call once MyDiagnostic.__init__()
MyDiagnostic()
```

Here are two differences:
    - The `register` method is called during initialization.
    - An instance is created right after the definition. This allows to instanciate the object and launch the register method.

## What's the purpose of Basic Diagnostics ?

The purpose of 'basic' (not registered) diagnostic is to be usable by any other diagnostic as a private dependency.

But it also means the load, call and usage will be completely handled by the developer.

## Why to use the Diagnostic class on basic diagnostics ?

Technically you can create any class without inheriting from Diagnostic.

But by using the Diagnostic inheritance, you can use the Diagnostic context, manager ...
