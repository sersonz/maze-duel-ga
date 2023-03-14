from types import SimpleNamespace

Common = SimpleNamespace()

Common.dirs = {"E": 1, "W": 2, "N": 4, "S": 8}
Common.inv_dirs = {"E": 2, "W": 1, "N": 8, "S": 4}
Common.dx = {"E": 1, "W": -1, "N": 0, "S": 0}
Common.dy = {"E": 0, "W": 0, "N": -1, "S": 1}