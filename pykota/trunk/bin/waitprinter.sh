#! /bin/sh
#
# PyKota - Print Quotas for CUPS and LPRng
#
# (c) 2003 Jerome Alet <alet@librelogiciel.com>
# You're welcome to redistribute this software under the
# terms of the GNU General Public Licence version 2.0
# or, at your option, any higher version.
#
# You can read the complete GNU GPL in the file COPYING
# which should come along with this software, or visit
# the Free Software Foundation's WEB site http://www.fsf.org
#
# $Id$
#

until snmpget -v1 -c public -Ov $1 HOST-RESOURCES-MIB::hrPrinterStatus.1 | grep -vi printing >/dev/null ; do 
   sleep 1 ; 
done

