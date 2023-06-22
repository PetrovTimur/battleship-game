"""User config."""

import configparser
from os.path import exists
import battleship.resources as resources


class Config:
    """Class to describe user's config."""

    file = None

    @staticmethod
    def load():
        """Load config file or create one."""
        if not exists(resources.config):
            Config.default()
        Config.file = configparser.ConfigParser()
        Config.file.read(resources.config)

    @staticmethod
    def save(value, field='settings'):
        """Save to config file."""
        if Config.file is None:
            Config.load()
        Config.file[field] = value
        with open(resources.config, 'w') as configFile:
            Config.file.write(configFile)

    @staticmethod
    def get(field='settings'):
        """Get config keys and values."""
        if Config.file is None:
            Config.load()
        return Config.file[field]

    @staticmethod
    def default():
        """Create default config."""
        config = configparser.ConfigParser()

        config['settings'] = {'name': 'Player',
                              'resolution': '1280x720',
                              'fullscreen': 'no',
                              'language': 'English'}

        with open(resources.config, 'w') as configfile:
            config.write(configfile)
