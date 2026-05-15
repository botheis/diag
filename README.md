Diag
===

Because to do support is annoying me a lot, I created this tool to help me to automate diagnostics and functional tests.

# Basically what is diag?

Diag is a standalone python package. After downloading it, you can use it as an external python module:
```python
# You must be on the /path/to/diag
python3 -m diag [args]
```
Diag is also a python package. You can use it inside your own project.

```python
from diag.errors import *
from diag.diagonal import Diagonal
from diag.manager import DiagnosticManager
from diag.diagnostic import Diagnostic

# Things to do with each element of the module.
```

# How to get diag ?

For now diag is available only on github through this repository:

```bash
# Clone the repo
git clone git@github.com:botheis/diag.git

# Copy the python module into your python env.
# cp -r diag /path/to/your/python-env/site-packages/
```

# How it works ?
We define some tests, then we execute this tool. The tool will load the tests, execute them and generate a report.

You can refer to the [user doc](./doc/user.md) for more details on how to use the tool.

You can refer to the [dev doc](./doc/dev.md) for more details on how to develop tests and how the tool works internally.

# My tests are ... special, can I use diag?

Probably yes ! If it can help you, here is my original user case:

```text
- A customer has installed the solution we develop.
- The solution includes
    - A main server,
    - 0 to n secondary relay servers
    - n agents-clients connected to the secondary relay servers.
- The access to the customer environment is quite hectic:
    - In best case, we have a ssh access
    - In middle case, a colleague has a unique access to the environment
    - In worst case, we have no access at all to the environment.
- Most of the time, the problem is not a code issue but a configuration issue... And I suck in sysadmin/network. So if normalized tests can be run to eliminate trivial tests. Or at best fix inconsistencies on config. It could be a great help for me.

On top of all that, the customer doesn't always know how to express the issue. So it ends up with this "thing" did this, this "stuff" did that...
```

So what can we do in this case ?
- Pray (almost not exegerating)
- Send a mail to the customer asking him to run commands, return the results and so on.

From this, we try to understand and reproduce the issue in our dev environment.

... I hate that ...

# How to improve this ?

When we have a problem, we execute some "checklists" driven by our experience to find the root cause of the problem.

Some of these checklists (diagnostics) are quite common, such as:
- Is this service running ?
- Is this port open ?
- Is this config file exists ?
- Is this config file correct ?
- ... (make your own checklist)

On the other hand, a diagnostic can be more complexe:
- Get the list of servers from sql database.
    - On each server, check if the config file exists and is correct.
    - On each server, try to connect with ssh (or other)
    - On each server, check if the port is open, if the service is running ...

Because I'm lazy, I want to make sure all my "checklists" are executed in a consistent way. It can reduce the time I spend on finding the right information.

# Conclusion

Don't let the support sessions suck up your soul.