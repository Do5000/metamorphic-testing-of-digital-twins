pytest_plugins = [
    "pytest_dt_mt.plugin",
    "pytest_dt_mt.fixtures"
]

def pytest_load_initial_conftests(early_config, parser, args):
    """
    If --monitor is active, completely disable pytest's built-in capture (-s).
    We will manually capture stdout in plugin.py so that live output flows 
    naturally to the terminal without double-printing or buffering issues.
    """
    if "--monitor" in args:
        to_remove = [a for a in args if a.startswith("--capture=") or a == "-s"]
        for a in to_remove:
            args.remove(a)
        args.append("-s")

