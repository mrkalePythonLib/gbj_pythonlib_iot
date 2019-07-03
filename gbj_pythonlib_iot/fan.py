# -*- coding: utf-8 -*-
"""Module for supporting cooling fan."""
__version__ = '0.1.0'
__status__ = 'Beta'
__author__ = 'Libor Gabaj'
__copyright__ = 'Copyright 2019, ' + __author__
__credits__ = []
__license__ = 'MIT'
__maintainer__ = __author__
__email__ = 'libor.gabaj@gmail.com'


import logging

# from . import common as common


###############################################################################
# Constants
###############################################################################


###############################################################################
# Classes
###############################################################################
class Fan(object):
    """IoT processing the cooling fan."""

    def __init__(self):
        """Create the class instance - constructor."""
        self._logger = logging.getLogger(' '.join([__name__, __version__]))
        self._logger.debug('Instance of %s created', self.__class__.__name__)
        # Device parameters
        self.temperature_on = None  # Start value in centigrades
        self.temperature_off = None  # Stop value in centigrades
        self.status = None  # Recent status detected

    def __str__(self):
        """Represent instance object as a string."""
        return 'CoolingFan'

    # -------------------------------------------------------------------------
    # Setters
    # -------------------------------------------------------------------------
    def set_temperature_on(self, temperature):
        """Save start temperature.

        Arguments
        ---------
        temperature : float
            Temperature in centigrades at which the fan starts cooling.

        """
        self.temperature_on = temperature

    def set_temperature_off(self, temperature):
        """Save stop temperature.

        Arguments
        ---------
        temperature : float
            Temperature in centigrades at which the fan stops cooling.

        """
        self.temperature_off = temperature

    def set_status(self, status):
        """Save recently detected status.

        Arguments
        ---------
        status : int
            Status code normalized.

        """
        self.status = status

    # -------------------------------------------------------------------------
    # Getters
    # -------------------------------------------------------------------------
    def get_temperature_on(self):
        """Return start temperature recently saved."""
        return self.temperature_on

    def get_temperature_off(self):
        """Return stop temperature recently saved."""
        return self.temperature_off

    def get_status(self):
        """Return status code recently saved."""
        return self.status
