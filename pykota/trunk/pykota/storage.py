# PyKota
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
# Revision 1.13  2003/06/10 16:37:54  jalet
# Deletion of the second user which is not needed anymore.
# Added a debug configuration field in /etc/pykota.conf
# All queries can now be sent to the logger in debug mode, this will
# greatly help improve performance when time for this will come.
#
# Revision 1.12  2003/04/23 22:13:57  jalet
# Preliminary support for LPRng added BUT STILL UNTESTED.
#
# Revision 1.11  2003/04/10 21:47:20  jalet
# Job history added. Upgrade script neutralized for now !
#
# Revision 1.10  2003/03/29 13:45:27  jalet
# GPL paragraphs were incorrectly (from memory) copied into the sources.
# Two README files were added.
# Upgrade script for PostgreSQL pre 1.01 schema was added.
#
# Revision 1.9  2003/02/17 22:55:01  jalet
# More options can now be set per printer or globally :
#
#       admin
#       adminmail
#       gracedelay
#       requester
#
# the printer option has priority when both are defined.
#
# Revision 1.8  2003/02/17 22:05:50  jalet
# Storage backend now supports admin and user passwords (untested)
#
# Revision 1.7  2003/02/10 12:07:31  jalet
# Now repykota should output the recorded total page number for each printer too.
#
# Revision 1.6  2003/02/09 13:05:43  jalet
# Internationalization continues...
#
# Revision 1.5  2003/02/08 22:39:46  jalet
# --reset command line option added
#
# Revision 1.4  2003/02/08 09:59:59  jalet
# Added preliminary base class for all storages
#
# Revision 1.3  2003/02/05 22:10:29  jalet
# Typos
#
# Revision 1.2  2003/02/05 22:02:22  jalet
# __import__ statement didn't work as expected
#
# Revision 1.1  2003/02/05 21:28:17  jalet
# Initial import into CVS
#
#
#

class PyKotaStorageError(Exception):
    """An exception for Quota Storage related stuff."""
    def __init__(self, message = ""):
        self.message = message
        Exception.__init__(self, message)
    def __repr__(self):
        return self.message
    __str__ = __repr__
        
def openConnection(pykotatool) :
    """Returns a connection handle to the appropriate Quota Storage Database."""
    backendinfo = pykotatool.config.getStorageBackend()
    backend = backendinfo["storagebackend"]
    try :
        if not backend.isalpha() :
            # don't trust user input
            raise ImportError
        #    
        # TODO : descending compatibility
        # 
        if backend == "postgresql" :
            backend = "pgstorage"       # TODO : delete, this is for descending compatibility only
        exec "from pykota.storages import %s as storagebackend" % backend.lower()    
    except ImportError :
        raise PyKotaStorageError, _("Unsupported quota storage backend %s") % backend
    else :    
        host = backendinfo["storageserver"]
        database = backendinfo["storagename"]
        admin = backendinfo["storageadmin"]
        adminpw = backendinfo["storageadminpw"]
        return getattr(storagebackend, "Storage")(pykotatool, host, database, admin, adminpw)

