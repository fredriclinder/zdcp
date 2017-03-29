"""Moduledocstring.

Ajax Device calls module

"""
__author__= "Zacharias El Banna"                     
__version__= "1.0GA"
__status__= "Production"

from sdcp.devices.DevHandler import Devices, sys_int2ip

########################################## Device Operations ##########################################
#
#
#
def device_view_devicelist(aWeb):
 target = aWeb.get_value('target')
 arg    = aWeb.get_value('arg')
 devs = Devices()
 db   = devs.connect_db()
 if target and arg:
  db.do("SELECT * FROM devices WHERE {0}='{1}' ORDER BY ip".format(target,arg))
 else:
  db.do("SELECT * FROM devices ORDER BY ip")
 print "<DIV CLASS='z-framed' ID=div_device_devicelist><DIV CLASS='z-table'>"
 print "<CENTER><TABLE WIDTH=330>"
 print "<TR><TH>IP</TH><TH>FQDN</TH><TH>Model</TH></TR>"
 rows = db.get_all_rows()
 for row in rows:
  print "<TR><TD><A CLASS=z-btnop TITLE='Show device info for {0}' OP=load DIV=div_navcont LNK='ajax.cgi?call=device_view_devinfo&node={3}'>{0}</A></TD><TD>{1}</TD><TD>{2}</TD></TR>".format(sys_int2ip(row['ip']), row['hostname']+"."+row['domain'], row['model'],row['id'])
 print "</TABLE></CENTER>"
 print "</DIV></DIV>"

#
#
#
def device_view_devinfo(aWeb):
 node   = aWeb.get_value('node')
 devs   = Devices()
 db     = devs.connect_db()
 db.do("SELECT * FROM devices WHERE id ='{}'".format(node))
 values = db.get_row()
 height = 230
 
 print "<DIV CLASS='z-framed z-table' style='resize: horizontal; margin-left:0px; width:420px; z-index:101; height:{}px;'>".format(str(height))
 print "<FORM ID=info_form>"
 print "<TABLE style='width:100%;'><TR>"
 
 # First table
 print "<TD><TABLE style='width:200px;'><TR><TH COLSPAN=2>Reachability Info</TH></TR>"
 print "<TR><TD>Name:</TD><TD><INPUT NAME=hostname CLASS='z-input' TYPE=TEXT PLACEHOLDER='{}'></TD></TR>".format(values['hostname'])
 print "<TR><TD>Domain:</TD><TD>{}</TD></TR>".format(values['domain'])
 print "<TR><TD>SNMP:</TD><TD>{}</TD></TR>".format(values['snmp'])
 print "<TR><TD>IP:</TD><TD>{}</TD></TR>".format(sys_int2ip(values['ip']))
 print "<TR><TD>Type:</TD><TD TITLE='Device type'><SELECT NAME=type CLASS='z-select'>"
 for tp in Devices.get_types():
  extra = " selected disabled" if values['type'] == tp else ""      
  print "<OPTION VALUE={0} {1}>{0}</OPTION>".format(str(tp),extra)
 print "</SELECT></TD></TR>"
 print "<TR><TD>Model:</TD><TD style='max-width:140px;'>{}</TD></TR>".format(values['model'])
 print "<TR><TD>DNS ID: {}</TD><TD>IPAM ID: {}</TD></TR>".format(values['dns_id'], values['ipam_id'])
 if values['graphed'] == "yes":
  print "<TR><TD><A CLASS='z-btnop' TITLE='View graphs for {1}' OP=load DIV=div_navcont LNK='/munin-cgi/munin-cgi-html/{0}/{1}/index.html#content'>Graphs</A>:</TD><TD>yes</TD></TR>".format(values['domain'],values['hostname']+"."+values['domain'])
 else:
  if not values['hostname'] == 'unknown':
   print "<TR><TD>Graphs:</TD><TD><A CLASS='z-btnop' OP=load DIV=div_navcont LNK='ajax.cgi?call=graph_add&node={}&name={}&domain={}' TITLE='Add Graphs for node?'>no</A></TD></TR>".format(node, values['hostname'], values['domain'])
  else:
   print "<TR><TD>Graphs:</TD><TD>no</TD></TR>"
 print "</TABLE></TD>"

 # Second table
 print "<TD><TABLE><TR><TH COLSPAN=2>Rack Info</TH></TR>"
 print "<TR><TD>Rack:</TD><TD><SELECT NAME=rack_id CLASS='z-select'>"
 db.do("SELECT * FROM racks")
 racks = db.get_all_rows()
 racks.append({ 'id':0, 'name':'Not used', 'size':'48', 'fk_pdu_1':'0', 'fk_pdu_2':'0','fk_console':'0'})
 for rack in racks:
  extra = " selected" if values['rack_id'] == rack['id'] else ""
  print "<OPTION VALUE={0} {1}>{2}</OPTION>".format(rack['id'],extra,rack['name'])
 print "</SELECT></TD></TR>"

 if not values['rack_id'] == 0:
  db.do("SELECT * FROM consoles")
  consoles = db.get_all_rows()
  consoles.append({ 'id':0, 'name':'Not used', 'ip':'127.0.0.1' })
  db.do("SELECT * FROM pdus")
  pdus = db.get_all_rows()
  pdus.append({ 'id':0, 'name':'Not used', 'ip':'127.0.0.1' })
  print "<TR><TD>Rack Unit:</TD><TD TITLE='Lower rack unit of device placement'><INPUT NAME=rack_unit CLASS='z-input' TYPE=TEXT PLACEHOLDER='{}'></TD></TR>".format(values['rack_unit'])
  print "<TR><TD>TS:</TD><TD><SELECT NAME=console_id CLASS='z-select'>"
  for console in consoles:
   extra = " selected" if values['console_id'] == console['id'] else ""
   print "<OPTION VALUE={0} {1}>{2}</OPTION>".format(console['id'],extra,console['name'])
  print "<TR><TD>TS Port:</TD><TD TITLE='Console port in rack TS'><INPUT NAME=consoleport CLASS='z-input' TYPE=TEXT PLACEHOLDER='{}'></TD></TR>".format(values['consoleport'])
  print "<TR><TD>PEM Left:</TD><TD><SELECT NAME=pwr_left_pdu_id CLASS='z-select'>"
  for pdu in pdus:
   extra = " selected" if values['pwr_left_pdu_id'] == pdu['id'] else ""
   print "<OPTION VALUE={0} {1}>{2}</OPTION>".format(pdu['id'],extra,pdu['name'])
  print "</SELECT></TD></TR>"
  print "<TR><TD>PEM Left Unit:</TD><TD><INPUT NAME=pwr_left_pdu_slot CLASS='z-input' TYPE=TEXT PLACEHOLDER='{}'></TD></TR>".format(values['pwr_left_pdu_slot'])
  print "<TR><TD>PEM Right:</TD><TD><SELECT NAME=pwr_right_pdu_id CLASS='z-select'>"
  for pdu in pdus:
   extra = " selected" if values['pwr_right_pdu_id'] == pdu['id'] else ""
   print "<OPTION VALUE={0} {1}>{2}</OPTION>".format(pdu['id'],extra,pdu['name'])
  print "</SELECT></TD></TR>"
  print "<TR><TD>PEM Right Unit:</TD><TD><INPUT NAME=pwr_right_pdu_slot CLASS='z-input' TYPE=TEXT PLACEHOLDER='{}'></TD></TR>".format(values['pwr_right_pdu_slot'])
 else:
  for index in range(0,7):
   print "<TR><TD COLSPAN=2 style='width:200px'>&nbsp;</TD></TR>"
 print "</TABLE></TD>"

 # Close large table
 print "</TR></TABLE>"
 print "<A CLASS='z-btn z-btnop z-small-btn' DIV=div_navcont LNK=ajax.cgi?call=device_view_devinfo&node={} OP=load><IMG SRC='images/btn-reboot.png'></A>".format(node)
 print "<A CLASS='z-btn z-btnop z-small-btn' DIV=update_results LNK=ajax.cgi?call=device_update_devinfo&node={} FRM=info_form OP=post TITLE='Update Entry'><IMG SRC='images/btn-save.png'></A>".format(node)
 print "<A CLASS='z-btn z-btnop z-small-btn' DIV=update_results LNK=ajax.cgi?call=device_update_dns&node={}  FRM=info_form OP=post TITLE='Update DNS'>D</A>".format(node)
 print "<A CLASS='z-btn z-btnop z-small-btn' DIV=update_results LNK=ajax.cgi?call=device_update_ipam&node={} FRM=info_form OP=post TITLE='Update IPAM'>I</A>".format(node)
 print "<SPAN style='float:right' ID=update_results></SPAN>&nbsp;"
 print "</FORM>"
 print "</DIV>"

 devs.close_db()

 print "<DIV CLASS='z-framed' style='margin-left:420px; overflow-x:hidden; z-index:100'><CENTER><IMG TITLE='Info image of {0}' ALT='Missing file images/info_{1}.jpg - 600px x 160px max' SRC='images/info_{1}.jpg'></CENTER></DIV>".format(values['hostname'],values['model'])

 print "<DIV CLASS='z-navbar' style='top:{}px;'>".format(str(height + 40))
 functions = Devices.get_widgets(values['type'])
 if functions:
  if functions[0] == 'operated':
   if values['type'] == 'esxi':
    print "<A TARGET='main_cont' HREF='pane.cgi?view=esxi&domain={}&host={}'>Manage</A></B></DIV>".format(values['domain'], values['hostname'])
  else:
   for fun in functions:
    name = " ".join(fun.split('_')[1:])
    print "<A CLASS='z-btnop' OP=load DIV=div_navdata SPIN=true LNK='ajax.cgi?call=device_view_devdata&ip={0}&type={1}&op={2}'>{3}</A>".format(sys_int2ip(values['ip']), values['type'], fun, name.title())
 else:
  print "&nbsp;"
 print "</DIV>"
 print "<DIV CLASS='z-navcontent' ID=div_navdata style='top:{}px; overflow-x:hidden; overflow-y:auto; z-index:100'></DIV>".format(str(height + 40))




################################################### UPDATE ###################################################
#
# Save data for device info
#
def device_update_devinfo(aWeb):
 node   = aWeb.get_value('node')
 values = aWeb.get_keys()
 values.remove('call')
 values.remove('node')
 if values:
  devs = Devices()
  db   = devs.connect_db()
  for key in values:
   db.do("UPDATE devices SET {0}='{1}' where id = '{2}'".format(key,aWeb.get_value(key),node))
  db.commit()
  devs.close_db()
  print "Updated: {}".format(" ".join(values))
 else:
  print "Nothing to update"

def device_update_detect(aWeb):
 print "not implemented yet"

def device_update_dns(aWeb):
 import sdcp.SettingsContainer as SC
 print "not implemented yet",SC.dnsdb_proxy

def device_update_ipam(aWeb):
 import sdcp.SettingsContainer as SC
 print "not implemented yet",SC.ipamdb_proxy

################################################## WIDGETs ################################################## 
#
# View operation data / widgets
#
def device_view_devdata(aWeb):
 ip   = aWeb.get_value('ip')
 type = aWeb.get_value('type')
 op   = aWeb.get_value('op')
 try:
  dev = Devices.get_node(ip,type)
  fun = getattr(dev,op,None)
  fun()
 except Exception as err:
  print "<B>Error in devdata: {}</B>".format(str(err))

#
# find devices operations
#
def device_op_finddevices(aWeb):
 domain    = aWeb.get_value('domain')
 discstart = aWeb.get_value('discstart')
 discstop  = aWeb.get_value('discstop')
 clear     = aWeb.get_value('clear',False)
 if discstart and discstop and domain:
  devs = Devices() 
  devs.discover(discstart,discstop, domain, clear)
  print "<B>Done Discovering Devices: {} -> {} for {}!</B>".format(discstart,discstop,domain)
  aWeb.log_msg("devices.cgi: Discovered devices [{}] {} -> {} for {}".format(str(clear), discstart,discstop,domain))
 else:
  print "<B>Not all parameters supplied</B>"