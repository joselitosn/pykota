# PyKota
# -*- coding: ISO-8859-15 -*-
#
# PyKota : Print Quotas for CUPS and LPRng
#
# (c) 2003 Jerome Alet <alet@librelogiciel.com>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# $Id$
#
# $Log$
# Revision 1.3  2003/11/25 23:46:40  jalet
# Don't try to verify if module name is valid, Python does this better than us.
#
# Revision 1.2  2003/10/07 09:07:28  jalet
# Character encoding added to please latest version of Python
#
# Revision 1.1  2003/06/30 12:46:15  jalet
# Extracted reporting code.
#
#
#

class PyKotaReporterError(Exception):
    """An exception for Reporter related stuff."""
    def __init__(self, message = ""):
        self.message = message
        Exception.__init__(self, message)
    def __repr__(self):
        return self.message
    __str__ = __repr__
    
class BaseReporter :    
    """Base class for all reports."""
    def __init__(self, tool, printers, ugnames, isgroup) :
        """Initialize local datas."""
        self.tool = tool
        self.printers = printers
        self.ugnames = ugnames
        self.isgroup = isgroup
        
def openReporter(tool, reporttype, printers, ugnames, isgroup) :
    """Returns a reporter instance of the proper reporter."""
    try :
        exec "from pykota.reporters import %s as reporterbackend" % reporttype.lower()
    except ImportError :
        raise PyKotaReporterError, _("Unsupported reporter backend %s") % reporttype
    else :    
        return getattr(reporterbackend, "Reporter")(tool, printers, ugnames, isgroup)
