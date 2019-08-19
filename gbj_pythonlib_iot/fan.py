# -*- coding: utf-8 -*-
"""Module for supporting cooling fan."""
__version__ = '0.5.0'
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
# Classes
###############################################################################
class Fan(object):
    """IoT processing the cooling fan.

    Arguments
    ---------
    pin : str
        Microcomputer I/O pin name for controlling a cooling fan.
    """


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

    def __init__(self, pin='PA13'):
        """Create the class instance - constructor."""
        self._system = iot_system.System()
        self.pin = pin
        self.status = None
        self.reset()
        # Logging
        self._logger = logging.getLogger(' '.join([__name__, __version__]))
        self._logger.debug(
            'Instance of %s created: %s',
            self.__class__.__name__,
            str(self)
            )

    def __str__(self):
        """Represent instance object as a string."""
        msg = \
            f'CoolingFan(' \
            f'{self.pin})'
        return msg

    def __repr__(self):
        """Represent instance object officially."""
        msg = \
            f'{self.__class__.__name__}(' \
            f'pin={repr(self.pin)})'
        return msg

    @property
    def pin(self):
        """Microcomputer fan control pin name."""
        return self._pin

    @pin.setter
    def pin(self, pin):
        """Set microcomputer pin name to control a fan."""
        self._pin = pin

    @property
    def status(self):
        """Status code recently."""
        return self._status

    @status.setter
    def status(self, status=None):
        """Save recently detected status."""
        self._status = status

    @property
    def percentage_on(self):
        """Start temperature percentage recently saved."""
        return self._percentage_on

    @percentage_on.setter
    def percentage_on(self, percentage=None):
        """Save start temperature percentage.

        Arguments
        ---------
        percentage : float
            Temperature in percentage of maximal temperature at which the fan
            starts cooling.
            If None provided, the default value is used

        """
        percentage = \
            max(min(percentage or self._PERCON_DEF,
                    self._PERCON_MAX), self._PERCON_MIN)
        self._percentage_on = percentage
        self._temperature_on = self._system.perc2temp(self._percentage_on)

    @property
    def percentage_off(self):
        """Stop temperature percentage recently saved."""
        return self._percentage_off

    @percentage_off.setter
    def percentage_off(self, percentage=None):
        """Save stop temperature percentage.

        Arguments
        ---------
        percentage : float
            Temperature in percentage of maximal temperature at which the fan
            stops cooling.
            If None provided, the default value is used

        """
        percentage = \
            max(min(percentage or self._PERCOFF_DEF,
                    self._PERCOFF_MAX), self._PERCOFF_MIN)
        self._percentage_off = percentage
        self._temperature_off = self._system.perc2temp(self._percentage_off)

    @property
    def temperature_on(self):
        """Start temperature recently saved."""
        return self._temperature_on

    @temperature_on.setter
    def temperature_on(self, temperature=None):
        """Save start temperature.

        Arguments
        ---------
        temperature : float
            Temperature in centigrades at which the fan starts cooling.
            If None provided the value calculated from default percentage
            is used.

        """
        percentage = None
        if temperature is not None:
            percentage = self._system.temp2perc(temperature)
        self.percentage_on = percentage

    @property
    def temperature_off(self):
        """Stop temperature recently saved."""
        return self._temperature_off

    @temperature_off.setter
    def temperature_off(self, temperature=None):
        """Save stop temperature.

        Arguments
        ---------
        temperature : float
            Temperature in centigrades at which the fan stops cooling.
            If None provided the value calculated from default percentage
            is used.

        """
        percentage = None
        if temperature is not None:
            percentage = self._system.temp2perc(temperature)
        self.percentage_off = percentage

    @property
    def temperature_max(self):
        """Maximal SoC temperature in centigrades."""
        return self._system.temperature_maximal

    @property
    def temperature(self):
        """Current SoC temperature in centigrades."""
        return self._system.temperature

    @property
    def percentage(self):
        """Current SoC temperature percentage."""
        return self._system.temp2perc(self.temperature)

    def reset(self):
        """Set all the default parameters."""
        self.percentage_on = None
        self.percentage_off = None
