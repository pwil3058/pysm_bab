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

import collections

PathAndRelation = collections.namedtuple("PathAndRelation", ["path", "relation"])
StyleAndForeground = collections.namedtuple("StyleAndForeground", ["style", "foreground"])

class WH(collections.namedtuple("WH", ["width", "height"])):
    __slots__ = ()
    def __sub__(self, other):
        # don't assume other is WH just that it has width and height attributes
        return WH(width=self.width - other.width, height=self.height - other.height)
    def __rsub__(self, other):
        # don't assume other is WH just that it has width and height attributes
        return WH(width=other.width - self.width, height=other.height - self.height)
    def __eq__(self, other):
        # don't assume other is WH just that it has width and height attributes
        return other.width == self.width and other.height == self.height

class XY(collections.namedtuple("XY", ["x", "y"])):
    __slots__ = ()
    def __add__(self, other):
        # don't assume other is XY just that it has x and y attributes
        return XY(x=self.x + other.x, y=self.y + other.y)
    def __sub__(self, other):
        # don't assume other is XY just that it has x and y attributes
        return XY(x=self.x - other.x, y=self.y - other.y)
    def __rsub__(self, other):
        # don't assume other is XY just that it has x and y attributes
        return XY(x=other.x - self.x, y=other.y - self.y)
    def __mul__(self, other):
        # allow scaling
        return XY(x=self.x * other, y=self.y * other)
    def __eq__(self, other):
        # don't assume other is XY just that it has x and y attributes
        return other.x == self.x and other.y == self.y

class RECT(collections.namedtuple("XY", ["x", "y", "width", "height"])):
    __slots__ = ()
    @staticmethod
    def from_xy_wh(xy, wh):
        return RECT(x=xy.x, y=xy.y, width=wh.width, height=wh.height)
    @property
    def position(self):
        return XY(self.x, self.y)
    @property
    def size(self):
        return WH(self.width, self.height)
