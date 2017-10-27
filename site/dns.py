"""Module docstring.

Ajax DNS calls module

"""
__author__= "Zacharias El Banna"
__version__ = "17.10.4"
__status__= "Production"

import sdcp.PackageContainer as PC
from sdcp.core.dbase import DB
from sdcp.core.rest import call as rest_call

#
#
#
def load(aWeb):
 dns_domains  = rest_call(PC.dns['url'], "sdcp.rest.{}_domains".format(PC.dns['type']))
 print "<DIV CLASS=z-frame>"
 with DB() as db:
  db.do("SELECT id,name FROM domains")
  sdcp_domains = db.get_rows_dict('id')
  for dom in dns_domains:
   add = sdcp_domains.pop(dom['id'],None)
   if not add:
    print "Added: {}".format(dom)
   db.do("INSERT INTO domains(id,name) VALUES ({0},'{1}') ON DUPLICATE KEY UPDATE name='{1}'".format(dom['id'],dom['name']))
  print "<SPAN>Domains - Inserted:{}, Remaining old:{}</SPAN><BR>".format(len(dns_domains),len(sdcp_domains))
  for dom,entry in sdcp_domains.iteritems():
   print "Delete {} -> {}<BR>".format(dom,entry)
   db.do("DELETE FROM domains WHERE id = '{}'".format(dom))
  db.commit()
 print "</DIV>"

#
#
#
def discrepancy(aWeb):
 dns = rest_call(PC.dns['url'],"sdcp.rest.{}_get_records".format(PC.dns['type']),{'type':'A'})
 with DB() as db:
  db.do("SELECT devices.id, ip, INET_NTOA(ip) as ipasc, hostname, a_id, ptr_id, a_dom_id FROM devices ORDER BY ip")
  devs = db.get_rows_dict('ipasc')
 print "<DIV CLASS=z-frame><DIV CLASS=title>DNS Consistency</DIV><SPAN ID=span_dns STYLE='font-size:9px;'>&nbsp;</SPAN>"
 print "<DIV CLASS=z-table STYLE='width:auto;'><DIV CLASS=tbody>"
 for rec in dns['records']:
  dev = devs.pop(rec['content'],None)
  print "<DIV CLASS=tr>"
  print "<!-- {} --> ".format(rec)
  if not dev or dev['a_id'] != rec['id']:
   print "<DIV CLASS=td>{}</DIV>".format(rec['content'])
   print "<DIV CLASS=td>{}</DIV>".format(rec['name'])
   print "<DIV CLASS=td>{}</DIV>".format(rec['type'])
   if dev:
    print "<DIV CLASS=td>{} vs {}</DIV>".format(rec['id'],dev['a_id'])
    print "<DIV CLASS=td>{}</DIV>".format(dev['hostname'])
   else:
    print "<DIV CLASS=td>&nbsp</DIV>"
    print "<DIV CLASS=td>&nbsp</DIV>"
  print "</DIV>"
 if len(devs) > 0:
  print "<DIV CLASS=title>Extra only in SDCP</DIV>"
  import sdcp.core.extras as EXT
  EXT.dict2table(devs)
 print "</DIV>"

#
# DNS top
#
def top(aWeb):
 import sdcp.core.extras as EXT
 dnstop = rest_call(PC.dns['url'], "sdcp.rest.{}_top".format(PC.dns['type']), {'count':20})
 print "<DIV CLASS=z-frame STYLE='float:left; width:49%;'><DIV CLASS=title>Top looked up FQDN</DIV>"
 EXT.dict2table(dnstop['top'])
 print "</DIV>"
 print "<DIV CLASS=z-frame STYLE='float:left; width:49%;'><DIV CLASS=title>Top looked up FQDN per Client</DIV>"
 EXT.dict2table(dnstop['who'])
 print "</DIV>"

#
# Cleanup duplicate entries
#
def cleanup(aWeb):
 dnsclean = rest_call(PC.dns['url'], "sdcp.rest.{}_cleanup".format(PC.dns['type']))
 print "<DIV CLASS=z-frame><DIV CLASS=title>Cleanup</DIV>"
 xist = len(dnsclean['removed'])
 if xist > 0:
  import sdcp.core.extras as EXT
  EXT.dict2table(dnsclean['removed'])
 print "</DIV>"
