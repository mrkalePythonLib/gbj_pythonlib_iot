# -*- coding: utf-8 -*-
"""Module for common constants, function, and classes for the IoT."""
__version__ = '0.1.0'
__status__ = 'Beta'
__author__ = 'Libor Gabaj'
__copyright__ = 'Copyright 2019, ' + __author__
__credits__ = []
__license__ = 'MIT'
__maintainer__ = __author__
__email__ = 'libor.gabaj@gmail.com'


###############################################################################
# Enumeration and parameter classes
###############################################################################
class Status:
    """Enumeration of possible status tokens for MQTT topics."""

    (
        ONLINE, OFFLINE, ACTIVE, IDLE,
    ) = range(4)


class Command:
    """Enumeration of possible commands tokens for MQTT topics."""

    (
        STATUS, RESET, ON, OFF, TOGGLE,
    ) = range(5)


# Mapping status and command codes to tokens
status_map = []
command_map = []
# Status codes
status_map.insert(Status.ONLINE, 'Online')  # Connected for LWT topic
status_map.insert(Status.OFFLINE, 'Offline')  # Disconnected for LWT topic
status_map.insert(Status.ACTIVE, 'Active')
status_map.insert(Status.IDLE, 'Idle')
# Commands
command_map.insert(Command.STATUS, 'STATUS')  # Requesting status data
command_map.insert(Command.RESET, 'RESET')  # Requesting reset of parameters
command_map.insert(Command.ON, 'ON')
command_map.insert(Command.OFF, 'OFF')
command_map.insert(Command.TOGGLE, 'TOGGLE')


# -------------------------------------------------------------------------
# Getters
# -------------------------------------------------------------------------
def get_status(index):
    """Return token value for token index."""
    try:
        token = status_map[index]
    except Exception:
        token = None
    return token


def get_status_index(token):
    """Return token index for token value."""
    index = None
    for i, t in enumerate(status_map):
        if t == token:
            index = i
            break
    return index


def get_command(index):
    """Return token value for token index."""
    try:
        token = command_map[index]
    except Exception:
        token = None
    return token


def get_command_index(token):
    """Return token index for token value."""
    index = None
    for i, t in enumerate(command_map):
        if t == token:
            index = i
            break
    return index
