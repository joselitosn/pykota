# -*- coding: UTF-8 -*-
#
# PyKota : Print Quotas for CUPS
#
# (c) 2003, 2004, 2005, 2006, 2007 Jerome Alet <alet@librelogiciel.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# $Id$
#
#

"""This module defines some helper functions to use in CGI scripts."""

import sys
import os

def getLanguagePreference() :
    """Returns the preferred language."""
    languages = os.environ.get("HTTP_ACCEPT_LANGUAGE", "")
    langs = [l.strip().split(';')[0] for l in languages.split(",")]
    #sys.stderr.write("Languages preferences : %s\n" % langs)
    return langs[0].replace("-", "_")
    
def getCharsetPreference() :
    """Returns the preferred charset."""
    charsets = os.environ.get("HTTP_ACCEPT_CHARSET", "UTF-8")
    charsets = [l.strip().split(';')[0] for l in charsets.split(",")]
    #sys.stderr.write("Charsets preferences : %s\n" % charsets)
    return charsets[0]
