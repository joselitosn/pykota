#! /usr/bin/env python
# -*- coding: ISO-8859-15 -*-
#
# PyKota
#
# PyKota : Print Quotas for CUPS and LPRng
#
# (c) 2003, 2004, 2005 Jerome Alet <alet@librelogiciel.com>
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
# Revision 1.5  2005/02/14 23:37:58  jalet
# Added a check for the presence of pythn-psyco
#
# Revision 1.4  2005/01/17 08:44:23  jalet
# Modified copyright years
#
# Revision 1.3  2004/11/15 21:11:01  jalet
# Modified some labels for Python modules
#
# Revision 1.2  2004/11/15 21:08:01  jalet
# Now checks for the presence of ReportLab and PIL
#
# Revision 1.1  2004/11/10 22:17:12  jalet
# Installation script is now non-interactive again, and doesn't install
# the sample configuration files into /etc/pykota anymore.
# Dependencies check is now done by running checkdeps.py
# The database creation scripts will now be included in RPM packages.
#
#
#

import sys
import os

def checkModule(module) :
    """Checks if a Python module is available or not."""
    try :
        exec "import %s" % module
    except ImportError :    
        return 0
    else :    
        return 1
        
def checkCommand(command) :
    """Checks if a command is available or not."""
    input = os.popen("type %s 2>/dev/null" % command)
    result = input.read().strip()
    input.close()
    return result
    
def checkWithPrompt(prompt, module=None, command=None, helper=None) :
    """Tells the user what will be checked, and asks him what to do if something is absent."""
    sys.stdout.write("Checking for %s availability : " % prompt)
    sys.stdout.flush()
    if command is not None :
        result = checkCommand(command)
    elif module is not None :    
        result = checkModule(module)
    if result :    
        sys.stdout.write("OK\n")
    else :    
        sys.stdout.write("NO.\n")
        sys.stderr.write("ERROR : %s not available !\n" % prompt)
        sys.stdout.write("%s\n" % helper)
    
if __name__ == "__main__" :    
    print "Checking PyKota dependencies..."
    
    # checks if Python version is correct, we need >= 2.1
    if not (sys.version > "2.1") :
        sys.stderr.write("PyKota needs at least Python v2.1 !\nYour version seems to be older than that, please update.\nAborted !\n")
        sys.exit(-1)
        
    # checks if some needed Python modules are there or not.
    modulestocheck = [ ("Python-PygreSQL", "pg", "PygreSQL is mandatory if you want to use PostgreSQL as the quota storage backend.\nSee http://www.pygresql.org"),
                       ("Python-egenix-mxDateTime", "mx.DateTime", "eGenix' mxDateTime is mandatory for PyKota to work.\nSee http://www.egenix.com"),
                       ("Python-LDAP", "ldap", "Python-LDAP is mandatory if you plan to use an LDAP\ndirectory as the quota storage backend.\nSee http://python-ldap.sf.net"),
                       ("Python-OSD", "pyosd", "Python-OSD is recommended if you plan to use the X Window On Screen Display\nprint quota reminder named pykosd."),
                       ("Python-SNMP", "pysnmp", "Python-SNMP is recommended if you plan to use hardware\naccounting with printers which support SNMP.\nSee http://pysnmp.sf.net"),
                       ("Python-JAXML", "jaxml", "Python-JAXML is recommended if you plan to dump datas in the XML format.\nSee http://www.librelogiciel.com/software/"),
                       ("Python-ReportLab", "reportlab.pdfgen.canvas", "Python-ReportLab is required if you plan to have PyKota generate banners.\nSee http://www.reportlab.org/"),
                       ("Python-Imaging", "PIL.Image", "Python-Imaging is required if you plan to have PyKota generate banners.\nSee http://www.pythonware.com/downloads/"),
                       ("Python-Psyco", "psyco", "Python-Psyco speedups parsing of print files, you should use it.\nSee http://psyco.sourceforge.net/"),
                     ]
    commandstocheck = [ ("SNMP Tools", "snmpget", "SNMP Tools are needed if you want to use SNMP enabled printers."), 
                        ("Netatalk", "pap", "Netatalk is needed if you want to use AppleTalk enabled printers.")
                      ]
    for (name, module, helper) in modulestocheck :
        checkWithPrompt(name, module=module, helper=helper)
            
    # checks if some software are there or not.
    for (name, command, helper) in commandstocheck :
        checkWithPrompt(name, command=command, helper=helper)
            