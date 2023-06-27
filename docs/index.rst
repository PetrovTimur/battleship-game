.. battleship documentation master file, created by
   sphinx-quickstart on Fri Jun 23 02:22:25 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**Battleship**
======================================

Battleship is a simple-to-use Python package that seeks to recreate the classic game experience.

**About**
---------------

This application invites users to play famous strategy board game battleship.
You can play single-player mode with (not so good) AI or try to sink other player online.

**Installation**
-----------------

.. note::

    The following instructions are temporary. They will be updated
    when the package will be published.

Start the installation by cloning GitHub repo ::

    git clone https://github.com/PetrovTimur/battleship-game

Set up venv and install required packages with ::

   pipenv install --dev

Build a wheel ::

   doit wheel

The wheel will be in **dist** folder.
Install this wheel into some other virtual environment ::

   pip install YOUR_PATH/dist/*.whl

You can launch the game with this command ::

   play-battleship

**Indices and tables**
-------------------------

* :ref:`genindex`
* :ref:`modindex`
