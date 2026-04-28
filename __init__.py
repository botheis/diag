import logging

logging.basicConfig(level=logging.INFO)

# Diagnostic name can be anything, but unique. There is a convention on how to name them.
# Diagnostic name convention:
# <name>
# <section>.<name>
# <section>.<subsection>.<name>
# <section>.<subsection>.<subsubsection>.<name> ...

# Thanks to this convention, we can easily call `mmc_diag --run <name> ` and it will run the diagnostic with that name, or if it doesn't exist, it will run all diagnostics that start with that name. For example, `mmc_diag --run section.sub.subsub....name` will run the found diagnostics starting with this this name.
