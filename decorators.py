### -*- coding: utf-8 -*-
###
###  Copyright (C) 2016 Peter Williams <pwil3058@gmail.com>
###
### This program is free software; you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation; version 2 of the License only.
###
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
###
### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

# Method 4 from <http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python>
def singleton(class_):
    class class_w(class_):
        _instance = None
        def __new__(class_, *args, **kwargs):
            if class_w._instance is None:
                class_w._instance = super(class_w, class_).__new__(class_, *args, **kwargs)
                class_w._instance._sealed = False
            return class_w._instance
        def __init__(self, *args, **kwargs):
            if self._sealed:
                return
            super(class_w, self).__init__(*args, **kwargs)
            self._sealed = True
    class_w.__name__ = class_.__name__
    return class_w

def prop(func):
    """ The builtin @property decorator lets internal AttributeErrors escape.
       While that can support properties that appear to exist conditionally,
       in practice this is almost never what I want, and it masks deeper errors.
       Hence this wrapper for @property that transmutes internal AttributeErrors
       into RuntimeErrors.
    """
    # FROM Cameron Simpson <cs@zip.com.au> post to "python-list"
    def wrapper(*a, **kw):
        try:
            return func(*a, **kw)
        except AttributeError as e:
            raise RuntimeError("inner function %s raised %s" % (func, e))
    return property(wrapper)

class classproperty:
    """Turn class methods into read only properties
    """
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, _owner_self, owner_cls):
        return self.fget(owner_cls)

    def __set__(self, _owner_self, _value):
        raise AttributeError("unsettable attribute")
