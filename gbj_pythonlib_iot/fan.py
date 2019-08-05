# -*- coding: utf-8 -*-
"""Module for supporting cooling fan."""
__version__ = '0.3.0'
__status__ = 'Beta'
__author__ = 'Libor Gabaj'
__copyright__ = 'Copyright 2019, ' + __author__
__credits__ = []
__license__ = 'MIT'
__maintainer__ = __author__
__email__ = 'libor.gabaj@gmail.com'


import logging

from . import system as iot_system


###############################################################################
# Constants
###############################################################################
_PERCON_DEF = 90.0
_PERCON_MIN = 80.0
_PERCON_MAX = 95.0
"""float: Default, minimal, and maximal start temperature expressed
   in percentage of maximal one.
"""

_PERCOFF_DEF = 60.0
_PERCOFF_MIN = 50.0
_PERCOFF_MAX = 75.0
"""float: Default, minimal, and maximal stop temperature expressed
   in percentage of maximal one.
"""

_PIN = ''


###############################################################################
# Classes
###############################################################################
class Fan(object):
    """IoT processing the cooling fan.

    Arguments
    ---------
    pin : str
        Microcomputer I/O pin name for controlling a cooling fan.
    """

    def __init__(self, pin='PA13'):
        """Create the class instance - constructor."""
        self._system = iot_system.System()
        self.set_status()
        self.set_pin(pin)
        # Logging
        self._logger = logging.getLogger(' '.join([__name__, __version__]))
        self._logger.debug(
            'Instance of %s created: %s',
            self.__class__.__name__,
            str(self)
            )
        # Set default values
        self.reset()

    def __str__(self):
        """Represent instance object as a string."""
        msg = \
            f'CoolingFan(' \
            f'{self.get_pin()})'
        return msg

    def __repr__(self):
        """Represent instance object officially."""
        msg = \
            f'{self.__class__.__name__}(' \
            f'pin={repr(self.get_pin())})'
        return msg

    def reset(self):
        """Set all the default parameters."""
        self.set_percentage_on()
        self.set_percentage_off()

    # -------------------------------------------------------------------------
    # Setters
    # -------------------------------------------------------------------------
    def set_status(self, status=None):
        """Save recently detected status.

        Arguments
        ---------
        status : int
            Status code normalized.

        """
        self._status = status

    def set_pin(self, pin):
        """Save microcomputer pin name to control a fan."""
        self._pin = pin

    def set_percentage_on(self, percentage=None):
        """Save start temperature percentage.

        Arguments
        ---------
        percentage : float
            Temperature in percentage of maximal temperature at which the fan
            starts cooling.
            If not provided, the default value is used

        """
        percentage = \
            max(min(percentage or _PERCON_DEF, _PERCON_MAX), _PERCON_MIN)
        self._percentage_on = percentage
        self._temperature_on = \
            self._system.calculate_temperature_value(self._percentage_on)
        self._logger.debug(
            'Percentage ON set to %s%% (%s°C)',
            self._percentage_on,
            self._temperature_on
            )

    def set_percentage_off(self, percentage=None):
        """Save stop temperature percentage.

        Arguments
        ---------
        percentage : float
            Temperature in percentage of maximal temperature at which the fan
            stops cooling.
            If not provided, the default value is used

        """
        percentage = \
            max(min(percentage or _PERCOFF_DEF, _PERCOFF_MAX), _PERCOFF_MIN)
        self._percentage_off = percentage
        self._temperature_off = \
            self._system.calculate_temperature_value(self._percentage_off)
        self._logger.debug(
            'Percentage OFF set to %s%% (%s°C)',
            self._percentage_off,
            self._temperature_off
            )

    def set_temperature_on(self, temperature=None):
        """Save start temperature.

        Arguments
        ---------
        temperature : float
            Temperature in centigrades at which the fan starts cooling.
            If not provided the value calculated from default percentage
            is used.

        """
        percentage = None
        if temperature is not None:
            percentage = self._system.calculate_temperature_percentage(
                temperature
                )
        self.set_percentage_on(percentage)

    def set_temperature_off(self, temperature=None):
        """Save stop temperature.

        Arguments
        ---------
        temperature : float
            Temperature in centigrades at which the fan stops cooling.
            If not provided the value calculated from default percentage
            is used.

        """
        percentage = None
        if temperature is not None:
            percentage = self._system.calculate_temperature_percentage(
                temperature
                )
        self.set_percentage_off(percentage)

    # -------------------------------------------------------------------------
    # Getters
    # -------------------------------------------------------------------------
    def get_pin(self):
        """Return microcomputer fan control pin name."""
        return self._pin

    def get_status(self):
        """Return status code recently saved."""
        return self._status

    def get_percentage_on(self):
        """Return start temperature percentage recently saved."""
        return self._percentage_on

    def get_percentage_off(self):
        """Return stop temperature percentage recently saved."""
        return self._percentage_off

    def get_temperature_on(self):
        """Return start temperature recently saved."""
        return self._temperature_on

    def get_temperature_off(self):
        """Return stop temperature recently saved."""
        return self._temperature_off

    def get_temperature_max(self):
        """Return maximal SoC temperature in centigrades."""
        return self._system.get_temperature_maximal()

    def get_temperature(self):
        """Return current SoC temperature in centigrades."""
        return self._system.get_temperature()

    def get_percentage(self):
        """Return current SoC temperature percentage."""
        return self._system.calculate_temperature_percentage(
            self._system.get_temperature())
