# PyKota
# -*- coding: ISO-8859-15 -*-
#
# PyKota : Print Quotas for CUPS and LPRng
#
# (c) 2003-2004 Jerome Alet <alet@librelogiciel.com>
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
#

from pykota.storage import PyKotaStorageError,BaseStorage,StorageObject,StorageUser,StorageGroup,StoragePrinter,StorageJob,StorageLastJob,StorageUserPQuota,StorageGroupPQuota
from pykota.storages.sql import SQLStorage

try :
    import pg
except ImportError :    
    import sys
    # TODO : to translate or not to translate ?
    raise PyKotaStorageError, "This python version (%s) doesn't seem to have the PygreSQL module installed correctly." % sys.version.split()[0]
else :    
    try :
        PGError = pg.Error
    except AttributeError :    
        PGError = pg.error

class Storage(BaseStorage, SQLStorage) :
    def __init__(self, pykotatool, host, dbname, user, passwd) :
        """Opens the PostgreSQL database connection."""
        BaseStorage.__init__(self, pykotatool)
        try :
            (host, port) = host.split(":")
            port = int(port)
        except ValueError :    
            port = -1         # Use PostgreSQL's default tcp/ip port (5432).
        
        try :
            self.database = pg.connect(host=host, port=port, dbname=dbname, user=user, passwd=passwd)
        except PGError, msg :
            raise PyKotaStorageError, str(msg)
        else :    
            self.closed = 0
            self.tool.logdebug("Database opened (host=%s, port=%s, dbname=%s, user=%s)" % (host, port, dbname, user))
            
    def close(self) :    
        """Closes the database connection."""
        if not self.closed :
            self.database.close()
            self.closed = 1
            self.tool.logdebug("Database closed.")
        
    def beginTransaction(self) :    
        """Starts a transaction."""
        self.database.query("BEGIN;")
        self.tool.logdebug("Transaction begins...")
        
    def commitTransaction(self) :    
        """Commits a transaction."""
        self.database.query("COMMIT;")
        self.tool.logdebug("Transaction committed.")
        
    def rollbackTransaction(self) :     
        """Rollbacks a transaction."""
        self.database.query("ROLLBACK;")
        self.tool.logdebug("Transaction aborted.")
        
    def doRawSearch(self, query) :
        """Does a raw search query."""
        query = query.strip()    
        if not query.endswith(';') :    
            query += ';'
        try :
            self.tool.logdebug("QUERY : %s" % query)
            result = self.database.query(query)
        except PGError, msg :    
            raise PyKotaStorageError, str(msg)
        else :    
            return result
            
    def doSearch(self, query) :        
        """Does a search query."""
        result = self.doRawSearch(query)
        if (result is not None) and (result.ntuples() > 0) : 
            return result.dictresult()
        
    def doModify(self, query) :
        """Does a (possibly multiple) modify query."""
        query = query.strip()    
        if not query.endswith(';') :    
            query += ';'
        try :
            self.tool.logdebug("QUERY : %s" % query)
            result = self.database.query(query)
        except PGError, msg :    
            raise PyKotaStorageError, str(msg)
        else :    
            return result
            
    def doQuote(self, field) :
        """Quotes a field for use as a string in SQL queries."""
        if type(field) == type(0.0) : 
            typ = "decimal"
        elif type(field) == type(0) :    
            typ = "int"
        elif type(field) == type(0L) :    
            typ = "int"
        else :    
            typ = "text"
        return pg._quote(field, typ)