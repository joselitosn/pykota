# PyKota
#
# PyKota : Print Quotas for CUPS
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
# Revision 1.20  2003/03/29 13:45:27  jalet
# GPL paragraphs were incorrectly (from memory) copied into the sources.
# Two README files were added.
# Upgrade script for PostgreSQL pre 1.01 schema was added.
#
# Revision 1.19  2003/02/27 08:41:49  jalet
# DATETIME is not supported anymore in PostgreSQL 7.3 it seems, but
# TIMESTAMP is.
#
# Revision 1.18  2003/02/10 12:07:31  jalet
# Now repykota should output the recorded total page number for each printer too.
#
# Revision 1.17  2003/02/10 08:41:36  jalet
# edpykota's --reset command line option resets the limit date too.
#
# Revision 1.16  2003/02/08 22:39:46  jalet
# --reset command line option added
#
# Revision 1.15  2003/02/08 22:12:09  jalet
# Life time counter for users and groups added.
#
# Revision 1.14  2003/02/07 22:13:13  jalet
# Perhaps edpykota is now able to add printers !!! Oh, stupid me !
#
# Revision 1.13  2003/02/07 00:08:52  jalet
# Typos
#
# Revision 1.12  2003/02/06 23:20:03  jalet
# warnpykota doesn't need any user/group name argument, mimicing the
# warnquota disk quota tool.
#
# Revision 1.11  2003/02/06 15:05:13  jalet
# self was forgotten
#
# Revision 1.10  2003/02/06 15:03:11  jalet
# added a method to set the limit date
#
# Revision 1.9  2003/02/06 14:52:35  jalet
# Forgotten import
#
# Revision 1.8  2003/02/06 14:49:04  jalet
# edpykota should be ok now
#
# Revision 1.7  2003/02/06 14:28:59  jalet
# edpykota should be ok, minus some typos
#
# Revision 1.6  2003/02/06 09:19:02  jalet
# More robust behavior (hopefully) when the user or printer is not managed
# correctly by the Quota System : e.g. cupsFilter added in ppd file, but
# printer and/or user not 'yet?' in storage.
#
# Revision 1.5  2003/02/05 23:26:22  jalet
# Incorrect handling of grace delay
#
# Revision 1.4  2003/02/05 23:02:10  jalet
# Typo
#
# Revision 1.3  2003/02/05 23:00:12  jalet
# Forgotten import
# Bad datetime conversion
#
# Revision 1.2  2003/02/05 22:28:38  jalet
# More robust storage
#
# Revision 1.1  2003/02/05 21:28:17  jalet
# Initial import into CVS
#
#
#

import fnmatch

class SQLStorage :    
    def getMatchingPrinters(self, printerpattern) :
        """Returns the list of all printers tuples (name, pagecounter) which match a certain pattern for the printer name."""
        printerslist = []
        # We 'could' do a SELECT printername FROM printers WHERE printername LIKE ...
        # but we don't because other storages semantics may be different, so every
        # storage should use fnmatch to match patterns and be storage agnostic
        result = self.doQuery("SELECT printername, pagecounter FROM printers;")
        result = self.doParseResult(result)
        if result is not None :
            for printer in result :
                if fnmatch.fnmatchcase(printer["printername"], printerpattern) :
                    printerslist.append((printer["printername"], printer["pagecounter"]))
        return printerslist        
            
    def addPrinter(self, printername) :        
        """Adds a printer to the quota storage."""
        self.doQuery("INSERT INTO printers (printername) VALUES (%s);" % self.doQuote(printername))
        
    def getPrinterUsers(self, printername) :        
        """Returns the list of usernames which uses a given printer."""
        result = self.doQuery("SELECT DISTINCT username FROM users WHERE id IN (SELECT userid FROM userpquota WHERE printerid IN (SELECT printerid FROM printers WHERE printername=%s)) ORDER BY username;" % self.doQuote(printername))
        result = self.doParseResult(result)
        if result is None :
            return []
        else :    
            return [record["username"] for record in result]
        
    def getPrinterGroups(self, printername) :        
        """Returns the list of groups which uses a given printer."""
        result = self.doQuery("SELECT DISTINCT groupname FROM groups WHERE id IN (SELECT groupid FROM grouppquota WHERE printerid IN (SELECT printerid FROM printers WHERE printername=%s));" % self.doQuote(printername))
        result = self.doParseResult(result)
        if result is None :
            return []
        else :    
            return [record["groupname"] for record in result]
        
    def getUserId(self, username) :
        """Returns a userid given a username."""
        result = self.doQuery("SELECT id FROM users WHERE username=%s;" % self.doQuote(username))
        try :
            return self.doParseResult(result)[0]["id"]
        except TypeError :      # Not found
            return
            
    def getPrinterId(self, printername) :        
        """Returns a printerid given a printername."""
        result = self.doQuery("SELECT id FROM printers WHERE printername=%s;" % self.doQuote(printername))
        try :
            return self.doParseResult(result)[0]["id"]
        except TypeError :      # Not found    
            return
            
    def getPrinterPageCounter(self, printername) :
        """Returns the last page counter value for a printer given its name."""
        result = self.doQuery("SELECT pagecounter, lastusername FROM printers WHERE printername=%s;" % self.doQuote(printername))
        try :
            return self.doParseResult(result)[0]
        except TypeError :      # Not found
            return
        
    def updatePrinterPageCounter(self, printername, username, pagecount) :
        """Updates the last page counter information for a printer given its name, last username and pagecount."""
        return self.doQuery("UPDATE printers SET pagecounter=%s, lastusername=%s WHERE printername=%s;" % (self.doQuote(pagecount), self.doQuote(username), self.doQuote(printername)))
        
    def addUserPQuota(self, username, printername) :
        """Initializes a user print quota on a printer, adds the printer and the user to the quota storage if needed."""
        (userid, printerid) = self.getUPIds(username, printername)
        if printerid is None :    
            self.addPrinter(printername)        # should we still add it ?
        if userid is None :    
            self.doQuery("INSERT INTO users (username) VALUES (%s);" % self.doQuote(username))
        (userid, printerid) = self.getUPIds(username, printername)
        if (userid is not None) and (printerid is not None) :
            return self.doQuery("INSERT INTO userpquota (userid, printerid) VALUES (%s, %s);" % (self.doQuote(userid), self.doQuote(printerid)))
        
    def getUPIds(self, username, printername) :    
        """Returns a tuple (userid, printerid) given a username and a printername."""
        return (self.getUserId(username), self.getPrinterId(printername))
        
    def getUserPQuota(self, username, printername) :
        """Returns the Print Quota information for a given (username, printername)."""
        (userid, printerid) = self.getUPIds(username, printername)
        if (userid is not None) and (printerid is not None) :
            result = self.doQuery("SELECT lifepagecounter, pagecounter, softlimit, hardlimit, datelimit FROM userpquota WHERE userid=%s AND printerid=%s;" % (self.doQuote(userid), self.doQuote(printerid)))
            try :
                return self.doParseResult(result)[0]
            except TypeError :      # Not found    
                pass
        
    def setUserPQuota(self, username, printername, softlimit, hardlimit) :
        """Sets soft and hard limits for a user quota on a specific printer given (username, printername)."""
        (userid, printerid) = self.getUPIds(username, printername)
        if (userid is not None) and (printerid is not None) :
            self.doQuery("UPDATE userpquota SET softlimit=%s, hardlimit=%s, datelimit=NULL WHERE userid=%s AND printerid=%s;" % (self.doQuote(softlimit), self.doQuote(hardlimit), self.doQuote(userid), self.doQuote(printerid)))
        
    def resetUserPQuota(self, username, printername) :    
        """Resets the page counter to zero. Life time page counter is kept unchanged."""
        (userid, printerid) = self.getUPIds(username, printername)
        if (userid is not None) and (printerid is not None) :
            self.doQuery("UPDATE userpquota SET pagecounter=0, datelimit=NULL WHERE userid=%s AND printerid=%s;" % (self.doQuote(userid), self.doQuote(printerid)))
        
    def setDateLimit(self, username, printername, datelimit) :
        """Sets the limit date for a soft limit to become an hard one given (username, printername)."""
        (userid, printerid) = self.getUPIds(username, printername)
        if (userid is not None) and (printerid is not None) :
            self.doQuery("UPDATE userpquota SET datelimit=%s::TIMESTAMP WHERE userid=%s AND printerid=%s;" % (self.doQuote("%04i-%02i-%02i %02i:%02i:%02i" % (datelimit.year, datelimit.month, datelimit.day, datelimit.hour, datelimit.minute, datelimit.second)), self.doQuote(userid), self.doQuote(printerid)))
        
    def updateUserPQuota(self, username, printername, pagecount) :
        """Updates the used user Quota information given (username, printername) and a job size in pages."""
        (userid, printerid) = self.getUPIds(username, printername)
        if (userid is not None) and (printerid is not None) :
            self.doQuery("UPDATE userpquota SET lifepagecounter=lifepagecounter+(%s), pagecounter=pagecounter+(%s) WHERE userid=%s AND printerid=%s;" % (self.doQuote(pagecount), self.doQuote(pagecount), self.doQuote(userid), self.doQuote(printerid)))
        
