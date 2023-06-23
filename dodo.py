#!/usr/bin/env python3

import glob
from doit.tools import create_folder
from doit import create_after

DOIT_CONFIG = {'default_tasks': ['app']}


def task_test():
    """Perform tests."""
    return {
        'actions': ['python3 -m unittest discover tests']
    }


def task_pot():
    """Re-create .pot ."""
    return {
            'actions': ['pybabel extract -o messages.pot battleship'],
            'file_dep': glob.glob('battleship/*.py') + glob.glob('battleship/*/*.py'),
            'targets': ['messages.pot'],
           }


def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update -D messages -d battleship/translation -i messages.pot'],
            'file_dep': ['messages.pot'],
            'targets': ['battleship/translation/ru/LC_MESSAGES/messages.po'],
           }


def task_mo():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, ['battleship/translation/ru/LC_MESSAGES']),
                'pybabel compile -D messages -l ru -i battleship/translation/ru/LC_MESSAGES/messages.po -d battleship/translation'
                       ],
            'file_dep': ['battleship/translation/ru/LC_MESSAGES/messages.po'],
            'targets': ['battleship/translation/ru/LC_MESSAGES/messages.mo'],
           }


def task_app():
    """Run application."""
    from battleship import main
    return {
            'actions': [main],
            'task_dep': ['mo'],
           }


def task_style():
    """Check style against flake8."""
    return {
            'actions': ['flake8 battleship']
           }


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {
            'actions': ['pydocstyle battleship']
           }


def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
            'actions': ['git clean -Xdf'],
           }


def task_wheel():
    """Create binary wheel distribution."""
    return {
            'actions': ['python -m build -n -w'],
            'task_dep': ['mo'],
           }


def task_sdist():
    """Create source distribution."""
    return {
            'actions': ['python -m build -s -n'],
            'task_dep': ['gitclean'],
           }


def task_html():
    """Make HTML documentation."""
    return {
            'actions': ['sphinx-build -M html docs build'],
           }
