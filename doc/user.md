User Doc
===

This documentation explain how to use the diag as a user who want to run tests.

# Command
The global command line will be :
```python
python3 -m diag [options]
```

# Options

The available options are:
- `--help` : show the help message and exit.
- `--list` : list all diagnostics and exit.
- `--run [name]` : run the diagnostic with the given name. Launch all the diagnostics with the name starting with the given name. If no name specified, run all registered diagnostics.
- `--diag DIR_PATH` : specify the path to the diagnostics. By default, it will look for diagnostics in the `diag/diagnostics` folder.
- `--report FILE_PATH` : specify the path to the report file. By default, it will create a report in the user directory :`~/diag.log`. The parent directory must exist, but the file will be created if it doesn't exist.

## --list

The result is a basic list of diagnostics names given during the registration.

## --run [name]
For example, there are some registered diagnostics with the following names:

    - `service.running`
    - `config.my`
    - `config.pulse2-package-server`
    - `network.test_connectivity`  

These commands will have the same result, because there is only one diagnostic with the name starting with `service`:
```python
# Launch service.running
python3 -m diag --run service
python3 -m diag --run service.running
```

But this command will launch all the config diagnostics:
```python
# Launch all config diagnostics
python3 -m diag --run config
```

And this one will launch only the config.my diagnostic:
```python
# Launch only config.my diagnostic
python3 -m diag --run config.my
```

## --diag DIR_PATH
This option allows you to specify the path to the diagnostics. By default, it will look for diagnostics in the `diag/diagnostics` folder.

Because usually it's not a good idea to work on global context, you can specify another path if you want.

## --report FILE_PATH
This option allows you to specify the path to the report file. By default, it will create a report in the user directory :`~/diag.log`. The parent directory must exist, but the file will be created if it doesn't exist.
