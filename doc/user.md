User Doc
===

This documentation explain how to use the mmc_diag as a user who want to run tests.

# Command
The global command line will be :
```python
python3 -m mmc_diag [options]
```

# Options

For now there are only two options:
- `--list` : list all diagnostics.
- `--run [name]` : run the diagnostic with the given name. Launch all the diagnostics with the name starting with the given name. If no name specified, run all registered diagnostics.

## --list

The result is a basic list of diagnostics names given during the registration.

## --run [name]
For example, there are some registered diagnostics with the following names:

    - `service.running`
    - `config.mmc`
    - `config.pulse2-package-server`
    - `network.test_connectivity`  

These commands will have the same result, because there is only one diagnostic with the name starting with `service`:
```python
# Launch service.running
python3 -m mmc_diag --run service
python3 -m mmc_diag --run service.running
```

But this command will launch all the config diagnostics:
```python
# Launch all config diagnostics
python3 -m mmc_diag --run config
```

And this one will launch only the config.mmc diagnostic:
```python
# Launch only config.mmc diagnostic
python3 -m mmc_diag --run config.mmc
```