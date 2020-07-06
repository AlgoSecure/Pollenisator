"""Implement a default to plugin. Using Plugin inheritied functions"""
from core.plugins.plugin import Plugin


class Default(Plugin):
    """Attributes:
        autoDefect: a boolean indication that this plugin should be used to autodetect file.
    """
    autoDetect = False  # Override default True value
