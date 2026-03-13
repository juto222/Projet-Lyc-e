"""Ouvre le Gestionnaire des tâches Windows."""
import subprocess
import sys


def open_task_manager() -> None:
    """Lance le Gestionnaire des tâches.

    Sur Windows, il existe un exécutable `taskmgr` qui ouvre le gestionnaire.
    """

    if sys.platform != "win32":
        raise RuntimeError("Ce script fonctionne uniquement sur Windows.")

    # `taskmgr` est fourni par Windows et doit être dans le PATH.
    subprocess.Popen(["taskmgr"], shell=False)


if __name__ == "__main__":
    open_task_manager()
