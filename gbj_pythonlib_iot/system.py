# -*- coding: utf-8 -*-
"""Module for supporting host microcomputer system.

- The module utilizes statistical smoothing by exponential filtering.
  It enables calculating temperature rate from recently provided temperature
  value, so that they are consistent.

"""
__version__ = '0.5.0'
__status__ = 'Beta'
__author__ = 'Libor Gabaj'
__copyright__ = 'Copyright 2019, ' + __author__
__credits__ = []
__license__ = 'MIT'
__maintainer__ = __author__
__email__ = 'libor.gabaj@gmail.com'


import logging
import random

# Third party modules
import gbj_pythonlib_sw.utils as modUtils
import gbj_pythonlib_sw.statfilter as modFilter


###############################################################################
# Classes
###############################################################################
class System(object):
    """IoT processing the microcomputer system.

    Arguments
    ---------
    smoothing_factor : float
        Positive smoothing factor for exponential filtering.
        It is converted to absolute value provided.

        - Acceptable value range is ``0.0 ~ 1.0`` and input value is limited
          to it.
        - Value ``0.5`` means ``runnig average``.
        - Value ``1.0`` means ``no smoothing``.

    """

    def __init__(self, smoothing_factor=0.2):
        """Create the class instance - constructor."""
        # Statistical smoothing
        self._temperature_max = None
        self._filter = modFilter.ValueFilter(self.temperature_maximal)
        self._smoothing = modFilter.Exponential(smoothing_factor)
        self._smoothing.filter = self._filter
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
            f'Microcomputer(' \
            f'{float(self._temperature_max)}°C)'
        return msg

    def __repr__(self):
        """Represent instance object officially."""
        msg = \
            f'{self.__class__.__name__}(' \
            f'smoothing_factor={repr(self._smoothing.factor)})'
        return msg

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

    @property
    def temperature_maximal(self):
        """System maximal temperature."""
        if self._temperature_max is None:
            temperature = self._read_temperature(
                '/sys/class/thermal/thermal_zone0/trip_point_0_temp'
            )
            if temperature is None and modUtils.windows():
                temperature = 75.0
            self._temperature_max = temperature
        return self._temperature_max

    @property
    def temperature(self):
        """Read system current temperature."""
        temperature = self._read_temperature(
            '/sys/class/thermal/thermal_zone0/temp'
        )
        if temperature is None and modUtils.windows():
            temperature = float(random.randint(40, 70))
        return self._smoothing.result(temperature)

    @property
    def percentage(self):
        """Read system current temperature and express it in percentage."""
        return self.temp2perc(self._smoothing.result())

    # -------------------------------------------------------------------------
    # Calculations
    # -------------------------------------------------------------------------
    def temp2perc(self, temperature):
        """Calculate percentage from temperature.

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
        self.temperature_maximal
        if self._temperature_max:
            percentage = temperature / self._temperature_max * 100.0
        return percentage

    def perc2temp(self, percentage):
        """Calculate temperature value in centigrades from percentage.

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
        self.temperature_maximal
        if self._temperature_max:
            temperature = percentage / 100.0 * self._temperature_max
        return temperature
