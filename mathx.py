# Copyright: Peter Williams (2012) - All rights reserved
#
# This software is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License only.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import math

class Angle(float):
    """
    A wrapper around float type to represent angles incorporating the
    restrictions that their value will be between -pi and pi.
    """
    def __new__(cls, value):
        """
        >>> Angle(2)
        Angle(2.0)
        >>> Angle(4)
        Traceback (most recent call last):
        AssertionError
        """
        #Make sure the value is between -pi and pi
        assert value >= -math.pi and value <= math.pi
        return float.__new__(cls, value)
    def __repr__(self):
        '''
        >>> Angle(2).__repr__()
        'Angle(2.0)'
        '''
        return '{0}({1})'.format(self.__class__.__name__, float.__repr__(self))
    @classmethod
    def normalize(cls, angle):
        """
        >>> Angle.normalize(2)
        Angle(2.0)
        >>> Angle.normalize(4)
        Angle(-2.2831853071795862)
        >>> Angle.normalize(-4)
        Angle(2.2831853071795862)
        >>> Angle.normalize(Angle(2))
        Traceback (most recent call last):
        AssertionError
        """
        assert not isinstance(angle, Angle)
        if angle > math.pi:
            return cls(angle - 2 * math.pi)
        elif angle < -math.pi:
            return cls(angle + 2 * math.pi)
        return cls(angle)
    def __neg__(self):
        """
        Change sign while maintaining type
        >>> -Angle(2)
        Angle(-2.0)
        >>> -Angle(-2)
        Angle(2.0)
        """
        return type(self)(float.__neg__(self))
    def __abs__(self):
        """
        Get absolate value while maintaining type
        >>> abs(-Angle(2))
        Angle(2.0)
        >>> abs(Angle(-2))
        Angle(2.0)
        """
        return type(self)(float.__abs__(self))
    def __add__(self, other):
        """
        Do addition and normalize the result
        >>> Angle(2) + 2
        Angle(-2.2831853071795862)
        >>> Angle(2) + 1
        Angle(3.0)
        """
        return self.normalize(float.__add__(self, other))
    def __radd__(self, other):
        """
        Do addition and normalize the result
        >>> 2.0 + Angle(2)
        Angle(-2.2831853071795862)
        >>> 1.0 + Angle(2)
        Angle(3.0)
        >>> 1 + Angle(2)
        Angle(3.0)
        """
        return self.normalize(float.__radd__(self, other))
    def __sub__(self, other):
        """
        Do subtraction and normalize the result
        >>> Angle(2) - 1
        Angle(1.0)
        >>> Angle(2) - 6
        Angle(2.2831853071795862)
        """
        return self.normalize(float.__sub__(self, other))
    def __rsub__(self, other):
        """
        Do subtraction and normalize the result
        >>> 1 - Angle(2)
        Angle(-1.0)
        >>> 6 - Angle(2)
        Angle(-2.2831853071795862)
        """
        return self.normalize(float.__rsub__(self, other))
    def __mul__(self, other):
        """
        Do multiplication and normalize the result
        >>> Angle(1) * 4
        Angle(-2.2831853071795862)
        >>> Angle(1) * 2.5
        Angle(2.5)
        """
        return self.normalize(float.__mul__(self, other))
PI_0 = Angle(0.0)
PI_30 = Angle(math.pi / 6)
PI_60 = Angle(math.pi / 3)
PI_90 = Angle(math.pi / 2)
PI_120 = PI_60 * 2
PI_150 = PI_30 * 5
PI_180 = Angle(math.pi)

def gcd(*args):
    if len(args) == 0:
        return None
    elif len(args) == 1:
        return args[0]
    result = math.gcd(args[0], args[1])
    for arg in args[2:]:
        result = math.gcd(result, arg)
    return result
