#! /usr/bin/env python
# -*- encoding:utf-8 -*-
# FileName: setup.py

"This file is part of ____"
 
__author__   = "yetist"
__copyright__= "Copyright (C) 2007 yetist <yetist@gmail.com>"
__license__  = """
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330,
Boston, MA 02111-1307, USA.
"""
from distutils.core import setup

setup(
    name = "keyfile",
    version = "0.1",
    author ="yetist",
    author_email ="yetist@gmail.com",
    url = "http://code.google.com/p/keyfile/",
    description = "An ini configure process module, similar the keyfile on glib.",
    license ="GPL",
    packages = ["KeyFile"]
    )
