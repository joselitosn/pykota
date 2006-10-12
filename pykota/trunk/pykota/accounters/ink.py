# PyKota
# -*- coding: ISO-8859-15 -*-
#
# PyKota - Print Quotas for CUPS and LPRng
#
# (c) 2003, 2004, 2005, 2006 Jerome Alet <alet@librelogiciel.com>
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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# $Id$
#
#

import os
from pykota.accounter import AccounterBase, PyKotaAccounterError


class Accounter(AccounterBase) :
    cspaceExpanded = {
                        "CMYK" : { "C" : "cyan", "M" : "magenta", "Y" : "yellow", "K" : "black" } ,
                        "CMY" : { "C" : "cyan", "M" : "magenta", "Y" : "yellow" } ,
                        "RGB" : { "R" : "red", "G" : "green", "B" : "blue" } ,
                        "BW" : { "B" : "black", "W" : "white" } ,
                     }
    def computeJobSize(self) :    
        """Do ink accounting for a print job."""
        if (not self.isPreAccounter) and \
            (self.filter.accounter.arguments == self.filter.preaccounter.arguments) :
            # if precomputing has been done and both accounter and preaccounter are
            # configured the same, no need to launch a second pass since we already
            # know the result.
            self.filter.logdebug("Precomputing pass told us that job is %s pages long." % self.filter.softwareJobSize)
            return self.filter.softwareJobSize   # Optimize : already computed !
            
        (colorspace, resolution) = [p.strip() for p in self.arguments.split(',')]
        colorspace = colorspace.lower()
        if colorspace not in ("cmyk", "bw", "cmy", "rgb") :
            raise PyKotaAccounterError, "Invalid parameters for ink accounter : [%s]" % self.arguments
            
        try :    
            resolution = int(resolution)
        except ValueError :    
            raise PyKotaAccounterError, "Invalid parameters for ink accounter : [%s]" % self.arguments
            
        self.filter.logdebug("Using internal parser to compute job's size and ink usage.")
        
        jobsize = 0
        self.inkUsage = []
        if self.filter.JobSizeBytes :
            try :
                from pkpgpdls import analyzer, pdlparser
            except ImportError :    
                self.filter.printInfo("pkpgcounter is now distributed separately, please grab it from http://www.pykota.com/software/pkpgcounter", "error")
                self.filter.printInfo("Precomputed job size will be forced to 0 pages.", "error")
            else :     
                options = analyzer.AnalyzerOptions(colorspace=colorspace, resolution=resolution)
                infile = open(self.filter.DataFile, "rb")
                try :
                    try :
                        parser = analyzer.PDLAnalyzer(infile, options)
                        (cspace, pages) = parser.getInkCoverage()
                        cspacelabels = self.cspaceExpanded[cspace]
                        for page in pages :
                            colordict = {}
                            for color in page.keys() :
                                colordict[cspacelabels[color]] = page[color]
                            self.inkUsage.append(colordict)    
                        jobsize = len(pages)
                        self.filter.logdebug("Ink usage : %s ===> %s" % (cspace, repr(self.inkUsage)))
                    except pdlparser.PDLParserError, msg :    
                        # Here we just log the failure, but
                        # we finally ignore it and return 0 since this
                        # computation is just an indication of what the
                        # job's size MAY be.
                        self.filter.printInfo(_("Unable to precompute the job's size with the generic PDL analyzer : %s") % msg, "warn")
                    else :    
                        if self.filter.InputFile is not None :
                            # when a filename is passed as an argument, the backend 
                            # must generate the correct number of copies.
                            jobsize *= self.filter.Copies
                finally :            
                    infile.close()        
        return jobsize        
