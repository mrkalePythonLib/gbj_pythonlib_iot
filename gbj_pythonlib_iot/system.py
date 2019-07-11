# -*- coding: utf-8 -*-
"""Module for supporting host microcomputer system."""
__version__ = '0.2.0'
__status__ = 'Beta'
__author__ = 'Libor Gabaj'
__copyright__ = 'Copyright 2019, ' + __author__
__credits__ = []
__license__ = 'MIT'
__maintainer__ = __author__
__email__ = 'libor.gabaj@gmail.com'


import logging
import platform
import random


###############################################################################
# Classes
###############################################################################
class System(object):
    """IoT processing the microcomputer system."""

    def __init__(self):
        """Create the class instance - constructor."""
        # Cached system maximal temperature
        self._temperature_max = self.get_temperature_maximal()
        # Logging
        self._logger = logging.getLogger(' '.join([__name__, __version__]))
        self._logger.debug(
            'Instance of %s created: %s',
            self.__class__.__name__,
            str(self)
            )

    def __str__(self):
        """Represent instance object as a string."""
        return 'Microcomputer ({}°C)'.format(self._temperature_max)

    def _read_temperature(self, system_path):
        """Read system file and interpret the content as the temperature.

        Arguments
        ---------
        system_path : str
            Full path to a file with system temperature.

        Returns
        -------
        temperature : float
            System temperature in centigrades Celsius.
            If some problem occurs with reading system file, the None is
            provided.

        """
        try:
            system_file = open(system_path)
            content = system_file.read()
            temperature = float(content)
            # Raspbian with temp in centigrades, other Pis in millicentigrades
            if temperature > 85.0:
                temperature /= 1000.0
            system_file.close()
        except Exception:
            temperature = None
        return temperature

    # -------------------------------------------------------------------------
    # Getters
    # -------------------------------------------------------------------------
    def get_temperature(self):
        """Read system current temperature."""
        temperature = self._read_temperature(
            '/sys/class/thermal/thermal_zone0/temp'
            )
        if temperature is None and platform.system() == 'Windows':
            temperature = float(random.randint(40, 70))
        return temperature

    def get_temperature_maximal(self):
        """Read system maximal temperature."""
        # Get temperature from the cache
        if hasattr(self, '_temperature_max') \
                and self._temperature_max is not None:
            return self._temperature_max
        # Read temperature from the system
        temperature = self._read_temperature(
            '/sys/class/thermal/thermal_zone0/trip_point_0_temp'
            )
        if temperature is None and platform.system() == 'Windows':
            temperature = 75.0
        self._temperature_max = temperature  # Cache temperature
        return temperature

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
        self.get_temperature_maximal()
        if self._temperature_max:
            percentage = temperature / self._temperature_max * 100.0
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
        self.get_temperature_maximal()
        if self._temperature_max:
            temperature = percentage / 100.0 * self._temperature_max
        return temperature
