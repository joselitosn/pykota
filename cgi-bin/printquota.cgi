#! /usr/bin/python
# -*- coding: ISO-8859-15 -*-

# PyKota Print Quota Reports generator
#
# PyKota - Print Quotas for CUPS and LPRng
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
# Revision 1.44  2005/01/19 08:49:41  jalet
# Now dumpykota.cgi behaves like printquota.cgi wrt the REMOTE_USER environment
# variables if the script is username+password protected.
# Small fix in printquota.cgi wrt ldap auth with Apache : the workaround was
# not used everywhere.
#
# Revision 1.43  2005/01/17 08:44:24  jalet
# Modified copyright years
#
# Revision 1.42  2005/01/08 17:19:02  jalet
# Fixed incorrect import statement
#
# Revision 1.41  2005/01/08 17:13:08  jalet
# Move some functions outside of the CGI to allow their use in other CGI scripts
#
# Revision 1.40  2004/10/23 19:28:18  jalet
# Small fix to the cgi script to please Freshmeat's fmII URL validator/1.1
#
# Revision 1.39  2004/10/13 09:38:25  jalet
# Added a translatable message from the CGI script
#
# Revision 1.38  2004/10/02 13:47:46  jalet
# The CGI script doesn't depend anymore on what is in the submit button
# to display the print quota report.
#
# Revision 1.37  2004/10/02 05:48:56  jalet
# Should now correctly deal with charsets both when storing into databases and when
# retrieving datas. Works with both PostgreSQL and LDAP.
#
# Revision 1.36  2004/09/02 10:34:09  jalet
# Fixed problem with mod_auth_ldap Apache module
#
# Revision 1.35  2004/07/24 20:10:10  jalet
# Incorrect number of parameters in error method
#
# Revision 1.34  2004/07/24 20:07:13  jalet
# Added special Python comment to remove warning at runtime
#
# Revision 1.33  2004/07/21 19:24:48  jalet
# Inversion
#
# Revision 1.32  2004/07/21 19:20:05  jalet
# Missing translation in CGI script
#
# Revision 1.31  2004/07/21 13:32:02  jalet
# All messages should be translatable now.
#
# Revision 1.30  2004/07/01 17:45:48  jalet
# Added code to handle the description field for printers
#
# Revision 1.29  2004/06/06 21:07:55  jalet
# Improved CGI script to allow history on printers and hostnames.
# Better (?) colors in stylesheet.
#
# Revision 1.28  2004/06/05 22:42:41  jalet
# Improved web history reports
#
# Revision 1.27  2004/05/26 14:49:40  jalet
# First try at saving the job-originating-hostname in the database
#
# Revision 1.26  2004/03/24 19:37:04  jalet
# Doesn't retrieve users or printers objects to display the history,
# this is not needed, and saves a lot of time (and database queries
# if storagecahing is disabled)
#
# Revision 1.25  2004/01/12 15:28:45  jalet
# Now can output the user's history on several printers at the same time.
#
# Revision 1.24  2004/01/12 14:52:03  jalet
# Cuts the date string
#
# Revision 1.23  2004/01/12 14:35:01  jalet
# Printing history added to CGI script.
#
# Revision 1.22  2004/01/09 07:58:53  jalet
# Changed URL to PyKota's logo
#
# Revision 1.21  2004/01/08 14:10:32  jalet
# Copyright year changed.
#
# Revision 1.20  2004/01/07 16:07:17  jalet
# The stylesheet is again expected to be local, it was a bad idea to use
# the one on my server.
#
# Revision 1.19  2004/01/06 16:05:45  jalet
# Will now search the stylesheet on my own website.
#
# Revision 1.18  2003/12/27 16:49:25  uid67467
# Should be ok now.
#
# Revision 1.16  2003/12/02 14:40:20  jalet
# Some code refactoring.
# New HTML reporter added, which is now used in the CGI script for web based
# print quota reports. It will need some de-uglyfication though...
#
# Revision 1.15  2003/10/24 22:06:42  jalet
# Initial support for browser's language preference added.
#
# Revision 1.14  2003/10/10 19:48:07  jalet
# Now displays version number
#
# Revision 1.13  2003/08/25 11:23:05  jalet
# More powerful CGI script for quota reports
#
# Revision 1.12  2003/07/29 20:55:17  jalet
# 1.14 is out !
#
# Revision 1.11  2003/07/01 12:37:31  jalet
# Nicer UI
#
# Revision 1.10  2003/07/01 07:30:32  jalet
# Message changed.
#
# Revision 1.9  2003/06/30 13:47:26  jalet
# Allows multiple user / group names masks in the input field
#
# Revision 1.8  2003/06/30 13:32:01  jalet
# Much more powerful CGI script for quota reports
#
# Revision 1.7  2003/06/30 12:46:15  jalet
# Extracted reporting code.
#
# Revision 1.6  2003/04/23 22:13:56  jalet
# Preliminary support for LPRng added BUT STILL UNTESTED.
#
# Revision 1.5  2003/04/17 21:30:09  jalet
# Now includes the logo
#
# Revision 1.4  2003/04/08 21:20:25  jalet
# CGI Script now displays a link to PyKota's website.
#
# Revision 1.3  2003/03/29 13:45:27  jalet
# GPL paragraphs were incorrectly (from memory) copied into the sources.
# Two README files were added.
# Upgrade script for PostgreSQL pre 1.01 schema was added.
#
# Revision 1.2  2003/02/12 11:31:51  jalet
# doesn't use the jaxml module anymore
#
# Revision 1.1  2003/02/10 13:41:38  jalet
# repykota cgi script added.
# cleaner doc.
#

import sys
import os
import cgi
import urllib

from pykota import version
from pykota.tool import PyKotaTool, PyKotaToolError
from pykota.reporter import PyKotaReporterError, openReporter
from pykota.cgifuncs import getLanguagePreference, getCharsetPreference

header = """Content-type: text/html

<?xml version="1.0" encoding="%s"?>
<html>
  <head>
    <title>%s</title>
    <link rel="stylesheet" type="text/css" href="/pykota.css" />
  </head>
  <body>
    <form action="printquota.cgi" method="POST">
      <table>
        <tr>
          <td>
            <p>
              <a href="http://www.librelogiciel.com/software/"><img src="http://www.librelogiciel.com/software/PyKota/pykota.png" alt="PyKota's Logo" /></a>
              <br />
              <a href="http://www.librelogiciel.com/software/">PyKota v%s</a>
            </p>
          </td>
          <td colspan="2">
            <h1>%s</h1>
          </td>
        </tr>
        <tr>
          <td colspan="3" align="center">
            <input type="submit" name="report" value="%s" />
          </td>
        </tr>
      </table>"""
    
footer = """
      <table>
        <tr>
          <td colspan="3" align="center">
            <input type="submit" name="report" value="%s" />
          </td>
        </tr>
      </table>  
    </form>
  </body>
</html>"""  

class PyKotaReportGUI(PyKotaTool) :
    """PyKota Administrative GUI"""
    def guiDisplay(self) :
        """Displays the administrative interface."""
        global header, footer
        print header % (self.getCharset(), _("PyKota Reports"), version.__version__, _("PyKota Reports"), _("Report"))
        print self.body
        print footer % _("Report")
        
    def error(self, message) :
        """Adds an error message to the GUI's body."""
        if message :
            self.body = '<p><font color="red">%s</font></p>\n%s' % (message, self.body)
        
    def htmlListPrinters(self, selected=[], mask="*") :    
        """Displays the printers multiple selection list."""
        printers = self.storage.getMatchingPrinters(mask)
        selectednames = [p.Name for p in selected]
        message = '<table><tr><td valign="top">%s :</td><td valign="top"><select name="printers" multiple="multiple">' % _("Printer")
        for printer in printers :
            if printer.Name in selectednames :
                message += '<option value="%s" selected="selected">%s (%s)</option>' % (printer.Name, printer.Name, printer.Description)
            else :
                message += '<option value="%s">%s (%s)</option>' % (printer.Name, printer.Name, printer.Description)
        message += '</select></td></tr></table>'
        return message
        
    def htmlUGNamesInput(self, value="*") :    
        """Input field for user/group names wildcard."""
        return _("User / Group names mask") + (' : <input type="text" name="ugmask" size="20" value="%s" /> <em>e.g. <strong>jo*</strong></em>' % (value or "*"))
        
    def htmlGroupsCheckbox(self, isgroup=0) :
        """Groups checkbox."""
        if isgroup :
            return _("Groups report") + ' : <input type="checkbox" checked="checked" name="isgroup" />'
        else :    
            return _("Groups report") + ' : <input type="checkbox" name="isgroup" />'
            
    def guiAction(self) :
        """Main function"""
        printers = ugmask = isgroup = None
        remuser = os.environ.get("REMOTE_USER", "root")    
        # special hack to accomodate mod_auth_ldap Apache module
        try :
            remuser = remuser.split("=")[1].split(",")[0]
        except IndexError :    
            pass
        self.body = "<p>%s</p>\n" % _("Please click on the above button")
        if self.form.has_key("report") :
            if self.form.has_key("printers") :
                printersfield = self.form["printers"]
                if type(printersfield) != type([]) :
                    printersfield = [ printersfield ]
                printers = [self.storage.getPrinter(p.value) for p in printersfield]
            else :    
                printers = self.storage.getMatchingPrinters("*")
            if remuser == "root" :
                if self.form.has_key("ugmask") :     
                    ugmask = self.form["ugmask"].value
                else :     
                    ugmask = "*"
            else :        
                if self.form.has_key("isgroup") :    
                    user = self.storage.getUser(remuser)
                    if user.Exists :
                        ugmask = " ".join([ g.Name for g in self.storage.getUserGroups(user) ])
                    else :    
                        ugmask = remuser # result will probably be empty, we don't care
                else :    
                    ugmask = remuser
            if self.form.has_key("isgroup") :    
                isgroup = 1
            else :    
                isgroup = 0
        self.body += self.htmlListPrinters(printers or [])            
        self.body += "<br />"
        self.body += self.htmlUGNamesInput(ugmask)
        self.body += "<br />"
        self.body += self.htmlGroupsCheckbox(isgroup)
        if not self.form.has_key("history") :
            if printers and ugmask :
                self.reportingtool = openReporter(admin, "html", printers, ugmask.split(), isgroup)
                self.body += "%s" % self.reportingtool.generateReport()
        else :        
            if remuser != "root" :
                username = remuser
            elif self.form.has_key("username") :    
                username = self.form["username"].value
            else :    
                username = None
            if username is not None :    
                user = self.storage.getUser(username)
            else :    
                user =None
            if self.form.has_key("printername") :
                printer = self.storage.getPrinter(self.form["printername"].value)
            else :    
                printer = None
            if self.form.has_key("datelimit") :    
                datelimit = self.form["datelimit"].value
            else :    
                datelimit = None
            if self.form.has_key("hostname") :    
                hostname = self.form["hostname"].value
            else :    
                hostname = None
            self.report = ["<h2>%s</h2>" % _("History")]    
            history = self.storage.retrieveHistory(user, printer, datelimit, hostname)
            if not history :
                self.report.append("<h3>%s</h3>" % _("Empty"))
            else :
                self.report.append('<table class="pykotatable" border="1">')
                headers = [_("Date"), _("Action"), _("User"), _("Printer"), _("Hostname"), _("JobId"), _("JobSize"), _("JobPrice"), _("Copies"), _("JobBytes"), _("PageCounter"), _("Title"), _("Filename"), _("Options")]
                self.report.append('<tr class="pykotacolsheader">%s</tr>' % "".join(["<th>%s</th>" % h for h in headers]))
                oddeven = 0
                for job in history :
                    oddeven += 1
                    if oddeven % 2 :
                        oddevenclass = "odd"
                    else :    
                        oddevenclass = "even"
                    if job.JobAction == "DENY" :
                        oddevenclass = "deny"
                    elif job.JobAction == "WARN" :    
                        oddevenclass = "warn"
                    username_url = '<a href="%s?%s">%s</a>' % (os.environ.get("SCRIPT_NAME", ""), urllib.urlencode({"history" : 1, "username" : job.UserName}), job.UserName)
                    printername_url = '<a href="%s?%s">%s</a>' % (os.environ.get("SCRIPT_NAME", ""), urllib.urlencode({"history" : 1, "printername" : job.PrinterName}), job.PrinterName)
                    if job.JobHostName :
                        hostname_url = '<a href="%s?%s">%s</a>' % (os.environ.get("SCRIPT_NAME", ""), urllib.urlencode({"history" : 1, "hostname" : job.JobHostName}), job.JobHostName)
                    else :    
                        hostname_url = None
                    self.report.append('<tr class="%s">%s</tr>' % (oddevenclass, "".join(["<td>%s</td>" % (h or "&nbsp;") for h in (job.JobDate[:19], job.JobAction, username_url, printername_url, hostname_url, job.JobId, job.JobSize, job.JobPrice, job.JobCopies, job.JobSizeBytes, job.PrinterPageCounter, job.JobTitle, job.JobFileName, job.JobOptions)])))
                self.report.append('</table>')
                dico = { "history" : 1,
                         "datelimit" : job.JobDate,
                       }
                if user and user.Exists :
                    dico.update({ "username" : user.Name })
                if printer and printer.Exists :
                    dico.update({ "printername" : printer.Name })
                if hostname :    
                    dico.update({ "hostname" : hostname })
                prevurl = "%s?%s" % (os.environ.get("SCRIPT_NAME", ""), urllib.urlencode(dico))
                self.report.append('<a href="%s">%s</a>' % (prevurl, _("Previous page")))
            self.body = "\n".join(self.report)    
            
if __name__ == "__main__" :
    os.environ["LC_ALL"] = getLanguagePreference()
    admin = PyKotaReportGUI(lang=os.environ["LC_ALL"], charset=getCharsetPreference())
    admin.form = cgi.FieldStorage()
    admin.guiAction()
    admin.guiDisplay()
    try :
        admin.storage.close()
    except (TypeError, NameError, AttributeError) :    
        pass
        
    sys.exit(0)
