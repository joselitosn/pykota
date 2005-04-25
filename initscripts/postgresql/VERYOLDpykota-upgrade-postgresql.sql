--
-- PyKota - Print Quotas for CUPS and LPRng
--
-- (c) 2003-2004 Jerome Alet <alet@librelogiciel.com>
-- This program is free software; you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation; either version 2 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
-- 
-- You should have received a copy of the GNU General Public License
-- along with this program; if not, write to the Free Software
-- Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
--
-- $Id$
--
--
--
-- This script has to be used if you already
-- have a pre-1.01 version of PyKota to upgrade
-- your database schema. Don't use it if
-- you've just installed PyKota, just use
-- the normal script instead.
--
                        
--                         
-- WARNING : YOU NEED A RECENT VERSION OF POSTGRESQL FOR THE DROP COLUMN STATEMENT TO WORK !
--

--                         
-- Modify the old database schema
--
ALTER TABLE grouppquota DROP COLUMN lifepagecounter;
ALTER TABLE grouppquota DROP COLUMN pagecounter;

--                         
-- Create the groups/members relationship
--
CREATE TABLE groupsmembers(groupid INT4 REFERENCES groups(id),
                           userid INT4 REFERENCES users(id),
                           PRIMARY KEY (groupid, userid));
                           
--                        
-- Set some ACLs                        
--
REVOKE ALL ON groupsmembers FROM public;                        
GRANT SELECT, INSERT, UPDATE, DELETE, REFERENCES ON groupsmembers TO pykotaadmin;