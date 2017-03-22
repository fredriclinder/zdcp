"""Moduledocstring.

Ajax calls module

"""
__author__= "Zacharias El Banna"                     
__version__= "2.1GA"
__status__= "Production"


######################################## Examine pane - logs ########################################
#
#
#

def examine_clear_logs(aWeb, aClear = True):
 domain  = aWeb.get_value('domain')
 try:
  from subprocess import check_output
  import sdcp.SettingsContainer as SC
  if aClear:
   open("/var/log/network/"+ domain +".log",'w').close()
   open(SC.sdcp_logformat,'w').close()
   aWeb.log_msg("Emptied logs")
  netlogs = check_output("tail -n 15 /var/log/network/{}.log | tac".format(domain), shell=True)
  print "<DIV CLASS='z-logs'><H1>Network Logs</H1><PRE>{}</PRE></DIV>".format(netlogs)
  print "<BR>"
  syslogs = check_output("tail -n 15 " + SC.sdcp_logformat + " | tac", shell=True)
  print "<DIV CLASS='z-logs'><H1>System Logs</H1><PRE>{}</PRE></DIV>".format(syslogs)
 except Exception as err:
  print "<DIV CLASS='z-error'>{}</DIV>".format(str(err))

########################################## Basic Rack Info ##########################################
#
#
#

def rack_info(aWeb):
 rack = aWeb.get_value('rack', 0)
 print "<DIV style='padding:20px;'>"
 print "<DIV style=' background-image: url(images/rack48u.png); background-position: center; background-repeat: no-repeat; height:1680px; width:770px;'></DIV>"
 print "</DIV>"

########################################## ESXi Operations ##########################################
#
#
#
def esxi_op(aWeb, aEsxi = None):
 excpt  = aWeb.get_value('except','-1')
 nstate = aWeb.get_value('nstate')
 vmid   = aWeb.get_value('vmid','-1')

 if not aEsxi:
  from sdcp.devices.ESXi import ESXi
  host   = aWeb.get_value('host')
  domain = aWeb.get_value('domain')
  aEsxi   = ESXi(host,domain)

 if nstate:
  from subprocess import check_call, check_output
  try:
   aWeb.log_msg("ESXi: {} got command {}".format(aEsxi._fqdn,nstate))
   if "vm-" in nstate:
    vmop = nstate.split('-')[1]
    with aEsxi:
     aEsxi.ssh_send("vim-cmd vmsvc/power." + vmop + " " + vmid)
   elif nstate == 'poweroff':
    with aEsxi:
     aEsxi.ssh_send("poweroff")
   elif nstate == 'vmsoff':
    excpt = "" if vmid == '-1' else vmid
    check_call("/usr/local/sbin/ups-operations shutdown " + aEsxi._hostname + " " + excpt + " &", shell=True)
  except Exception as err:
   aWeb.log_msg("ESXi: nstate error [{}]".format(str(err)))

 print "<TABLE>"
 template="<A CLASS='z-btn z-small-btn z-btnop' TITLE='{3}' OP=load DIV=div_esxi_op LNK='site.cgi?ajax=esxi_op&domain=" +  aEsxi._domain + "&host="+ aEsxi._hostname + "&nstate={0}&vmid={2}'><IMG SRC=images/btn-{1}.png></A>"
 statelist = aEsxi.get_vms()
 if not nstate:
  print "<TR><TH CLASS='z-header' COLSPAN=2>{}</TH></TR>".format(aEsxi._fqdn)
 else:
  print "<TR><TH CLASS='z-header' COLSPAN=2>{} - {}:{}</TH></TR>".format(aEsxi._fqdn,vmid, nstate.split('-')[1])
 print "<TR><TH>VM</TH><TH>Operations</TH></TR><TR>"
 if nstate and nstate == 'vmsoff':
  print "<TD><B>SHUTDOWN ALL VMs!</B></TD>"
 else:
  print "<TD>SHUTDOWN ALL VMs!</TD>"
 print "<TD><CENTER>" + template.format('vmsoff','shutdown',excpt, "Shutdown all VMs") + "</CENTER></TD></TR>"
 for vm in statelist:
  if vm[0] == vmid:
   print "<TR><TD><B>" + vm[1] + "</B></TD>"
  else:
   print "<TR><TD>" + vm[1] + "</TD>"
  print "<TD><CENTER>"
  if vm[2] == "1":
   print template.format('vm-shutdown','shutdown', vm[0], "Soft shutdown")
   print template.format('vm-reboot','reboot', vm[0], "Soft reboot")
   print template.format('vm-suspend','suspend', vm[0], "Suspend")
   print template.format('vm-off','off', vm[0], "Hard power off")
  elif vm[2] == "3":
   print template.format('vm-on','start', vm[0], "Start")
   print template.format('vm-off','off', vm[0], "Hard power off")
  else:
   print template.format('vm-on','start', vm[0], "Start")
  print "</CENTER></TD></TR>"
 print "</TABLE>"


########################################## Device Operations ##########################################
#
#
#
def device_view_devicelist(aWeb):
 from sdcp.devices.DevHandler import Devices
 from sdcp.core.GenLib import sys_ip2int
 domain = aWeb.get_value('domain')
 target = aWeb.get_value('target')
 arg    = aWeb.get_value('arg')
 devs = Devices() 
 devs.load_json()
 if target and arg:
  keys = devs.get_keys(target,arg, aSortKey = sys_ip2int)
 else:
  keys = devs.get_keys(aSortKey = sys_ip2int)
 print "<DIV CLASS='z-framed' ID=div_device_devicelist><DIV CLASS='z-table'>"
 print "<CENTER><TABLE WIDTH=330>"
 print "<TR><TH>IP</TH><TH>FQDN</TH><TH>Model</TH></TR>"
 for key in keys:
  values = devs.get_entry(key)
  print "<TR><TD><A CLASS=z-btnop TITLE='Show device info for {0}' OP=load DIV=div_navcont LNK='site.cgi?ajax=device_view_devinfo&node={0}'>{0}</A></TD><TD>{1}</TD><TD>{2}</TD></TR>".format(key, values['fqdn'], values['model'])
 print "</TABLE></CENTER>"
 print "</DIV></DIV>"

#
# View graphs
#
def device_view_graphlist(aWeb):
 from sdcp.core.Grapher import Grapher
 node  = aWeb.get_value('node')
 state = aWeb.get_value('state')
 graph = Grapher()
 graph.load_conf()
 if node and state:
  nstate = "yes" if state == "no" else "no"
  graph.update_entry(node, nstate)
 print "<DIV CLASS='z-framed'><DIV CLASS='z-table'>"
 print "<CENTER><TABLE WIDTH=330><TR><TH>Node</TH><TH>Handler</TH><TH TITLE='Include in graphing?'>Include</TH></TR>"
 keys = graph.get_keys()
 for key in keys:
  entry = graph.get_entry(key)
  gdomain = key.partition(".")[2]
  print "<TR>"
  if entry['update'] == 'yes':
   print "<TD><A CLASS=z-btnop TITLE='Show graphs for {1}' OP=load DIV=div_navcont LNK='/munin-cgi/munin-cgi-html/{0}/{1}/index.html'>{1}</A></TD>".format(gdomain,key)
  else:
   print "<TD>{0}</TD>".format(key)
  print "<TD>"+ entry['handler'] +"</TD>"
  print "<TD TITLE='Include in graphing?'><CENTER><A CLASS='z-btn z-small-btn z-btnop' OP=load DIV=div_navleft LNK='site.cgi?ajax=device_view_graphlist&node=" + key + "&state=" + entry['update'] + "'><IMG SRC=images/btn-{}.png></A></CENTER></TD>".format("start" if entry['update'] == "no" else "shutdown")
  print "</TR>"
 print "</TABLE></CENTER></DIV></DIV>"

#
# View PDUs
#
def device_view_pdulist(aWeb):
 from sdcp.devices.RackUtils import Avocent
 domain  = aWeb.get_value('domain')
 slot    = aWeb.get_value('slot')
 nstate  = aWeb.get_value('nstate')
 pdulist = aWeb.get_list('pdulist')
 pduop   = aWeb.get_value('pdu')
 if len(pdulist) == 0:
  pdulist.append(pduop)
 print "<DIV CLASS='z-framed'><DIV CLASS='z-table'><TABLE WIDTH=330>"
 print "<TR><TH>PDU</TH><TH>Entry</TH><TH>Device</TH><TH>State</TH></TR>"
 optemplate = "<A CLASS='z-btn z-small-btn z-btnop' OP=load SPIN=true DIV=div_navleft LNK='site.cgi?ajax=device_view_pdulist&pdu={0}&nstate={1}&slot={2}'><IMG SRC='images/btn-{3}'></A>"
 for pdu in pdulist:
  avocent = Avocent(pdu,domain)
  avocent.load_snmp()
  if pdu == pduop and slot and nstate:
   avocent.set_state(slot,nstate)
   # Avocent is not fast enough to execute something immediately after reboot op, halt output then :-)
   if nstate == 'reboot':
    from time import sleep
    sleep(10)
  for key in avocent.get_keys(aSortKey = lambda x: int(x.split('.')[0])*100+int(x.split('.')[1])):
   value = avocent.get_entry(key)
   print "<TR><TD>{0}</TD><TD>{1}</TD><TD>{2}</TD><TD>".format(pdu,value['pduslot'], value['name'])
   if value['state'] == "off":
    print optemplate.format(pdu, "on", key, "start")
   else:
    print optemplate.format(pdu, "off", key, "shutdown")
    print optemplate.format(pdu, "reboot", key, "reboot")
   print "</TD></TR>"
 print "</TABLE></DIV></DIV>"

#
# View Consoles
#
def device_view_consolelist(aWeb):
 from sdcp.devices.RackUtils import OpenGear
 domain = aWeb.get_value('domain')
 conlist = aWeb.get_list('conlist')
 config="https://{0}/?form=serialconfig&action=edit&ports={1}&start=&end="
 print "<DIV CLASS='z-framed'><DIV CLASS='z-table'><TABLE WIDTH=330>"
 print "<TR><TH>Server</TH><TH>Port</TH><TH>Device</TH></TR>"
 for con in conlist:
  console = OpenGear(con,domain)
  console.load_snmp()
  conip = console._ip
  for key in console.get_keys():
   port = str(6000 + key)
   value = console.get_entry(key)
   print "<TR><TD><A HREF='https://{0}/'>{1}</A></TD><TD><A TITLE='Edit port info' HREF={5}>{2}</A></TD><TD><A HREF='telnet://{0}:{3}'>{4}</A></TD>".format(conip, con,str(key),port, value, config.format(conip,key))
 print "</TABLE></DIV></DIV>"

#
# Device Info
#
def device_view_devinfo(aWeb):
 from sdcp.devices.DevHandler import Devices
 node   = aWeb.get_value('node')
 height = 190
 devs   = Devices()
 devs.load_json()
 values = devs.get_entry(node)
 
 print "<DIV CLASS='z-framed z-table' style='resize: horizontal; margin-left:0px; width:440px; z-index:101; height:{}px;'>".format(str(height))
 print "<FORM ID=info_form><INPUT NAME=ajax VALUE=device_update_devinfo TYPE=HIDDEN><INPUT NAME=node TYPE=HIDDEN VALUE={}>".format(node)
 print "<TABLE><TR><TD><TABLE>"
 
 print "<TR><TH COLSPAN=2 WIDTH=230>Reachability Info</TH></TR>"
 print "<TR><TD>DNS_Name:</TD><TD><INPUT NAME=dns CLASS='z-input' TYPE=TEXT PLACEHOLDER='{}'></TD></TR>".format(values['dns'])
 print "<TR><TD>Domain:</TD><TD>{}</TD></TR>".format(values['domain'])
 print "<TR><TD>FQDN:</TD><TD>{}</TD></TR>".format(values['fqdn'])
 print "<TR><TD>SNMP_Name:</TD><TD>{}</TD></TR>".format(values['snmp'])
 print "<TR><TD>IP:</TD><TD>{}</TD></TR>".format(node)
 if values['graphed'] == "yes":
  print "<TR><TD><A CLASS='z-btnop' TITLE='View graphs for {1}' OP=load DIV=div_navcont LNK='/munin-cgi/munin-cgi-html/{0}/{1}/index.html#content'>Graphs</A>:</TD><TD>yes</TD></TR>".format(values['domain'],values['fqdn'])
 else:
  if not values['dns'] == 'unknown':
   print "<TR><TD>Graphs:</TD><TD><A CLASS='z-btnop' OP=load DIV=div_navcont LNK='site.cgi?ajax=device_op_addgraph&node={}&name={}&domain={}' TITLE='Add Graphs for node?'>no</A></TD></TR>".format(node, values['dns'], values['domain'])
  else:
   print "<TR><TD>Graphs:</TD><TD>no</TD></TR>"
 print "</TABLE></TD><TD><TABLE>"
 print "<TR><TH COLSPAN=2 WIDTH=200>Device Info</TH></TR>"  
 print "<TR><TD>Type:</TD><TD><SELECT NAME=type CLASS='z-select'>"
 for tp in Devices.get_types():
  extra = " selected disabled" if values['type'] == tp else ""      
  print "<OPTION VALUE={0} {1}>{0}</OPTION>".format(str(tp),extra)
 
 print "</SELECT></TD></TR>"
 print "<TR><TD>Model:</TD><TD>{}</TD></TR>".format(values['model'])
 print "<TR><TD>Rack_ID:</TD><TD TITLE='Rack ID - numeric value of rack'><INPUT NAME=rack CLASS='z-input' TYPE=TEXT PLACEHOLDER='{}'></TD></TR>".format(values['rack'])
 print "<TR><TD>Unit:</TD><TD><SELECT NAME=unit CLASS='z-select'>"
 units = map(lambda x: str(x),range(1,49))
 units.append('unknown')
 for unit in units:
  extra = " selected disabled" if values['unit'] == unit else ""
  print "<OPTION VALUE={0} {1}>{0}</OPTION>".format(str(unit),extra)
 print "</SELECT></TD></TR>"
 print "<TR><TD>TS_Port:</TD><TD><INPUT NAME=consoleport CLASS='z-input' TYPE=TEXT PLACEHOLDER='{}'></TD></TR>".format(values['consoleport'])
 print "<TR><TD>Power:</TD><TD><INPUT CLASS='z-input' style='width:45%;' NAME=power_left TYPE=number PLACEHOLDER='{}'> : <INPUT CLASS='z-input' style='width:45%;' NAME=power_right TYPE=number PLACEHOLDER='{}'></TD></TR>".format(values['power_left'], values['power_right']) 

 print "</TABLE></TD></TR></TABLE>"
 print "<A CLASS='z-btn z-btnop z-small-btn' DIV=div_navcont LNK=site.cgi?ajax=device_view_devinfo&node={} OP=load><IMG SRC='images/btn-reboot.png'></A>".format(node)
 print "<A CLASS='z-btn z-btnop z-small-btn' DIV=update_results LNK=site.cgi FRM=info_form OP=post><IMG SRC='images/btn-save.png'></A><SPAN ID=update_results></SPAN>"
 print "</FORM>"
 print "</DIV>"

 print "<DIV CLASS='z-framed' style='margin-left:440px; overflow-x:hidden; z-index:100'><CENTER><IMG TITLE='Info image of {0}' ALT='Missing file images/info_{1}.jpg - 600px x 160px max' SRC='images/info_{1}.jpg'></CENTER></DIV>".format(values['fqdn'],values['model'])

 print "<DIV CLASS='z-navbar' style='top:{}px;'>".format(str(height + 40))
 functions = Devices.get_widgets(values['type'])
 if functions:
  if functions[0] == 'operated':
   if values['type'] == 'esxi':
    print "<A TARGET='main_cont' HREF='site.cgi?pane=esxi&domain={}&host={}'>Manage</A></B></DIV>".format(values['domain'], values['fqdn'].split('.')[0])
  else:
   for fun in functions:
    name = " ".join(fun.split('_')[1:])
    print "<A CLASS='z-btnop' OP=load DIV=div_navdata SPIN=true LNK='site.cgi?ajax=device_view_devdata&node={0}&type={1}&op={2}'>{3}</A>".format(node, values['type'], fun, name.title())
 else:
  print "&nbsp;"
 print "</DIV>"
 print "<DIV CLASS='z-navcontent' ID=div_navdata style='top:{}px; overflow-x:hidden; overflow-y:auto; z-index:100'></DIV>".format(str(height + 40))

#
# Save data for device info
#
def device_update_devinfo(aWeb):
 from sdcp.devices.DevHandler import Devices
 node   = aWeb.get_value('node')
 devs   = Devices()
 devs.load_json()
 entry  = devs.get_entry(node)
 values = aWeb.get_keys()
 values.remove('ajax')
 values.remove('node')
 for data in values:
  entry[data] = aWeb.get_value(data)
  if data == 'dns':
   # Update FQDN as well
   entry['fqdn'] = entry['dns'] + "." + entry['domain']
 devs.save_json()
 print "Updated: {}".format(" ".join(values))
  
 # loop through values and update accordingly
 #
 #

#
# View operation data
#
def device_view_devdata(aWeb):
 node = aWeb.get_value('node')
 type = aWeb.get_value('type')
 op   = aWeb.get_value('op')
 try:
  from sdcp.devices.DevHandler import Devices
  dev = Devices.get_node(node,type)
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
  from sdcp.devices.DevHandler import Devices
  devs = Devices() 
  devs.discover(discstart,discstop, domain, clear)
  print "<B>Done Discovering Devices: {} -> {} for {}!</B>".format(discstart,discstop,domain)
  aWeb.log_msg("devices.cgi: Discovered devices [{}] {} -> {} for {}".format(str(clear), discstart,discstop,domain))

#
# Find graphs
#
def device_op_findgraphs(aWeb):
 from sdcp.core.Grapher import Grapher
 try:
  graph = Grapher() 
  graph.discover()
  print "<B>Done discovering graphs</B>"
  aWeb.log_msg("devices.cgi: Discovered graphs")
 except Exception as err:
  print "<B>Error: {}</B>".format(str(err))

#
# Sync graphs and devices
#
def device_op_syncgraphs(aWeb):
 from sdcp.devices.DevHandler import Devices
 from sdcp.core.Grapher import Grapher
 try:
  devs  = Devices()
  devs.load_json()
  graph = Grapher()
  graphdevices = graph.get_keys()
  for dev in devs.get_keys():
   entry = devs.get_entry(dev)
   entry['graphed'] = 'yes' if entry['fqdn'] in graphdevices else 'no'
  devs.save_json()
  print "<B>Done syncing devices' graphing</B>"
  aWeb.log_msg("devices.cgi: Done syncing devices' graphing")
 except Exception as err:
  print "<B>Error: {}</B>".format(str(err))

#
# Add graphs
#
def device_op_addgraph(aWeb):
 node   = aWeb.get_value('node',None)
 name   = aWeb.get_value('name',None)
 domain = aWeb.get_value('domain',None)
 if name and domain:
  fqdn   = name + "." + domain
  from sdcp.core.Grapher import Grapher
  graph = Grapher()
  entry = graph.get_entry(fqdn)
  if entry:
   print "<B>Entry existed</B>"
  else:
   graph.add_entry(fqdn,'no')
   print "<B>Added graphing for node {0} ({1})</B>".format(node, fqdn)
