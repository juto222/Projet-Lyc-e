"""Supprime les fichiers temporaires de l'utilisateur.

Ce script efface le contenu du répertoire temporaire courant du système
(typiquement %TEMP% sous Windows ou /tmp sous Linux/Mac) en supprimant
les fichiers et dossiers qui s'y trouvent.
"""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path


def clean_temp_directory(dry_run: bool = False, verbose: bool = False) -> int:
    """Supprime le contenu du répertoire temporaire.

    Args:
        dry_run: Si vrai, n'effectue aucune suppression, affiche seulement ce qui serait supprimé.
        verbose: Si vrai, affiche chaque fichier/répertoire supprimé.

    Returns:
        Le nombre d'éléments supprimés.
    """

    temp_dir = Path(tempfile.gettempdir())
    if not temp_dir.exists():
        raise FileNotFoundError(f"Répertoire temporaire introuvable: {temp_dir}")

    removed = 0

    for entry in temp_dir.iterdir():
        try:
            if entry.is_dir():
                if verbose or dry_run:
                    print(f"[DIR ] {'(dry)' if dry_run else ''} Suppression: {entry}")
                if not dry_run:
                    shutil.rmtree(entry, ignore_errors=True)
            else:
                if verbose or dry_run:
                    print(f"[FILE] {'(dry)' if dry_run else ''} Suppression: {entry}")
                if not dry_run:
                    entry.unlink(missing_ok=True)

            removed += 1
        except Exception as exc:  # pragma: no cover
            print(f"Erreur lors de la suppression de {entry}: {exc}")

    return removed


def main() -> None:
    """Entrée principale du script."""

    # Exemple d'utilisation: suppression réelle
    removed = clean_temp_directory(dry_run=False, verbose=True)
    print(f"Terminé. {removed} éléments supprimés du répertoire temporaire.")


if __name__ == "__main__":
    main()
