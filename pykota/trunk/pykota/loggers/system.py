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
# Revision 1.5  2003/03/29 13:45:27  jalet
# GPL paragraphs were incorrectly (from memory) copied into the sources.
# Two README files were added.
# Upgrade script for PostgreSQL pre 1.01 schema was added.
#
# Revision 1.4  2003/02/27 23:48:41  jalet
# Correctly maps PyKota's log levels to syslog log levels
#
# Revision 1.3  2003/02/27 22:55:20  jalet
# WARN log priority doesn't exist.
#
# Revision 1.2  2003/02/05 23:47:54  jalet
# Forgotten default argument
#
# Revision 1.1  2003/02/05 23:09:20  jalet
# Name conflict
#
#
#

import sys
import syslog

class Logger :
    """A logger class which logs to syslog."""
    levels = { "error" : "ERR", "warn": "WARNING", "info": "INFO", "debug": "DEBUG" }
    def __init__(self) :
        """Opens the logging subsystem."""
        syslog.openlog("PyKota", 0, syslog.LOG_LPR)
        
    def __del__(self) :    
        """Ensures the logging subsystem is closed."""
        syslog.closelog()
        
    def log_message(self, message, level="info") :
        """Sends the message to syslog."""
        priority = getattr(syslog, "LOG_%s" % self.levels.get(level.lower(), "DEBUG").upper(), syslog.LOG_DEBUG)
        syslog.syslog(priority, message)
