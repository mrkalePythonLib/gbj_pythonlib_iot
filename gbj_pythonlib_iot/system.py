# -*- coding: utf-8 -*-
"""Module for supporting host microcomputer system."""
__version__ = '0.1.0'
__status__ = 'Beta'
__author__ = 'Libor Gabaj'
__copyright__ = 'Copyright 2019, ' + __author__
__credits__ = []
__license__ = 'MIT'
__maintainer__ = __author__
__email__ = 'libor.gabaj@gmail.com'


import logging


###############################################################################
# Classes
###############################################################################
class System(object):
    """IoT processing the microcomputer system."""

    def __init__(self):
        """Create the class instance - constructor."""
        self._logger = logging.getLogger(' '.join([__name__, __version__]))
        self._logger.debug('Instance of %s created', self.__class__.__name__)
        # Device parameters
        self.temperature_cur = None  # Current value in centigrades
        self.temperature_max = None  # Maximal value in centigrades

    def __str__(self):
        """Represent instance object as a string."""
        return 'Microcomputer'

    # -------------------------------------------------------------------------
    # Setters
    # -------------------------------------------------------------------------
    def set_temperature_current(self, temperature):
        """Save current temperature.

        Arguments
        ---------
        temperature : float
            Current temperature expressed in centigrades.

        """
        self.temperature_cur = temperature

    def set_temperature_maximal(self, temperature):
        """Save maximal temperature.

        Arguments
        ---------
        temperature : float
            Maximal value.

        """
        self.temperature_max = temperature

    # -------------------------------------------------------------------------
    # Getters
    # -------------------------------------------------------------------------
    def get_temperature_current(self):
        """Return current temperature recently saved."""
        return self.temperature_cur

    def get_temperature_maximal(self):
        """Return maximal temperature recently saved."""
        return self.temperature_max

    # -------------------------------------------------------------------------
    # Calculations
    # -------------------------------------------------------------------------
    def calculate_temperature_percentage(self, temperature):
        """Calculate temperature percentage.

        Arguments
        ---------
        temperature : float
            Value in centigrades to be converted to percentage of maximal
            value if it is saved.

        Returns
        -------
        percentage : float
            Input value expressed in percentage of saved maximal value
            or nothing.

        """
        percentage = None
        if self.temperature_max:
            percentage = temperature / self.temperature_max * 100.0
        return percentage

    def calculate_temperature_value(self, percentage):
        """Calculate temperature value in centigrades.

        Arguments
        ---------
        percentage : float
            Value in percentage of maximal value to be converted
            to centigrades.

        Returns
        -------
        temperature : float
            Input value expressed in centigrades if maximal value is saved
            or nothing.

        """
        temperature = None
        if self.temperature_max:
            temperature = percentage / 100.0 * self.temperature_max
        return temperature
