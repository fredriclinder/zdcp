"""Module docstring.

Ajax Openstack Neutron/Contrail calls module

- left and right divs frames (div_os_left/right) needs to be created by ajax call

"""
__author__= "Zacharias El Banna"
__version__ = "17.6.15GA"
__status__= "Production"

from sdcp.devices.openstack import OpenstackRPC
from sdcp.site.ajax_openstack import dict2html

############################### Neutron ##############################
#
def list(aWeb):
 cookie = aWeb.get_cookie()
 token  = cookie.get('os_user_token')
 if not token:
  print "Not logged in"
  return
 controller = OpenstackRPC(cookie.get('os_controller'),token)
 pname = cookie.get("os_project_name")

 ret = controller.call("8082","virtual-networks?fields=name,display_name,virtual_network_properties,network_ipam_refs")
 if not ret['result'] == "OK":
  print "Error retrieving list"
  return
 
 print "<DIV CLASS=z-os-left ID=div_os_left>"
 print "<DIV CLASS=z-frame style='overflow:auto;'><DIV CLASS=z-table style='width:99%'>"
 print "<DIV CLASS=thead  style='height:20px'><DIV CLASS=th><CENTER>Contrail VNs</CENTER></DIV></DIV>"
 print "<DIV CLASS=tr  style='height:20px'><DIV CLASS=td COLSPAN=3>"
 print "<A TITLE='Reload List' CLASS='z-btn z-small-btn z-op' DIV=div_os_frame URL='ajax.cgi?call=neutron_list'><IMG SRC='images/btn-reboot.png'></A>"
 print "</DIV></DIV>"
 print "<DIV CLASS=thead><DIV CLASS=th>Network</DIV><DIV CLASS=th>Subnet</DIV><DIV CLASS=th></DIV></DIV>"
 print "<DIV CLASS=tbody>"
 for net in ret['data']['virtual-networks']:
  if not net.get('display_name'):
   continue
  print "<DIV CLASS=tr>"
  print "<!-- {} -->".format(net.get('href'))
  print "<DIV CLASS=td style='max-width:200px; overflow-x:hidden;'><A TITLE='Info {1}' CLASS='z-op' DIV=div_os_right URL=ajax.cgi?call=neutron_action&id={0}&op=info SPIN=true>{1}</A></DIV>".format(net['uuid'],net['display_name'])
  print "<DIV CLASS=td>"
  if net.get('network_ipam_refs'):
   for ipam in net['network_ipam_refs']:
    for sub in ipam['attr']['ipam_subnets']:
     print "{}/{}".format(sub['subnet']['ip_prefix'],sub['subnet']['ip_prefix_len'])
  print "</DIV>"
  print "<DIV CLASS=td>"
  tmpl = "<A TITLE='{}' CLASS='z-btn z-op z-small-btn' DIV=div_os_right URL=ajax.cgi?call=neutron_action&name=" + net['display_name'] + "&id=" + net['uuid'] + "&op={} {} SPIN=true>{}</A>&nbsp;"
  print tmpl.format('Remove','remove',"MSG='Really delete network?'", '<IMG SRC=images/btn-remove.png>')
  print "</DIV>"
  print "</DIV>"
 print "</DIV>"
 print "</DIV></DIV></DIV></DIV>"
 print "<DIV CLASS=z-os-right ID=div_os_right></DIV>"

def action(aWeb):
 cookie = aWeb.get_cookie()
 token  = cookie.get('os_user_token')
 if not token:
  print "Not logged in"
  return
 controller = OpenstackRPC(cookie.get('os_controller'),token)

 id   = aWeb.get_value('id')
 op   = aWeb.get_value('op')

 print "<!-- action - op:{} - id:{} -->".format(op,id)
 if   op == 'info':
  vn = controller.call("8082","virtual-network/{}".format(id))['data']['virtual-network']
  name = vn['display_name']
  tmpl = "<A TITLE='{}' CLASS='z-btn z-op' DIV=div_os_info URL=ajax.cgi?call=neutron_action&name=" + name + "&id=" + id+ "&op={} SPIN=true>{}</A>"
  print "<DIV>"
  print "<A TITLE='Network details' CLASS='z-btn z-op' DIV=div_os_info URL=ajax.cgi?call=neutron_action&id={}&op=details    SPIN=true>Network Details</A>".format(id)
  if vn.get('instance_ip_back_refs'):
   print "<A TITLE='Network details' CLASS='z-btn z-op' DIV=div_os_info URL=ajax.cgi?call=neutron_action&id={}&op=interfaces SPIN=true>Interfaces</A>".format(id)
  if vn.get('floating_ip_pools'):
   # create a list of floating-ips
   fipool = ",".join(map(lambda x: x.get('uuid'), vn.get('floating_ip_pools')))
   print "<A TITLE='Network details' CLASS='z-btn z-op' DIV=div_os_info URL=ajax.cgi?call=neutron_action&op=floating-ip&fipool={} SPIN=true>Floating IPs</A>".format(fipool)

  print "</DIV>"
  print "<DIV CLASS=z-frame style='overflow:auto;' ID=div_os_info>"
  dict2html(vn,"{} ({})".format(name,id))
  print "</DIV>"

 elif op == 'details':
  vn = controller.call("8082","virtual-network/{}".format(id))['data']['virtual-network']
  name = vn['display_name']
  dict2html(vn,"{} ({})".format(name,id))

 elif op == 'interfaces':
  vn = controller.call("8082","virtual-network/{}".format(id))['data']['virtual-network']
  print "<DIV CLASS=z-table><DIV CLASS=thead><DIV CLASS=th>IP</DIV><DIV CLASS=th>MAC</DIV><DIV CLASS=th>Interface</DIV></DIV>"
  print "<DIV CLASS=tbody>"
  for ip in vn['instance_ip_back_refs']:
   iip = controller.href(ip['href'])['data']['instance-ip']
   vmi = controller.href(iip['virtual_machine_interface_refs'][0]['href'])['data']['virtual-machine-interface']
   print "<DIV CLASS=tr>"
   print "<! -- {} -->".format(ip['href'])
   print "<! -- {} -->".format(iip['virtual_machine_interface_refs'][0]['href'])
   if vmi.get('virtual_machine_refs'):
    print "<DIV CLASS=td><A CLASS='z-op' DIV=div_os_right SPIN=true URL=ajax.cgi?call=nova_action&id={0}>{1}</A></DIV>".format(vmi['virtual_machine_refs'][0]['uuid'],iip['instance_ip_address'])
   else:
    print "<DIV CLASS=td>{}</DIV>".format(iip['instance_ip_address'])
   print "<DIV CLASS=td>{}</DIV>".format(vmi['virtual_machine_interface_mac_addresses']['mac_address'][0])
   if   vmi.get('virtual_machine_interface_bindings'):
    host = vmi['virtual_machine_interface_bindings']['key_value_pair']
    for kvp in host:
     if kvp['key'] == 'host_id':
      print "<DIV CLASS=td>{}</DIV>".format(kvp['value'])
   elif vmi.get('logical_interface_back_refs'):
    li = vmi['logical_interface_back_refs'][0]
    interface = li['to'][1] + "-" + li['to'][3]
    print "<DIV CLASS=td><A CLASS='z-op' DIV=div_os_info SPIN=true URL=ajax.cgi?call=neutron_action&op=print&id={}>{}</A></DIV>".format(li['href'],interface)
   else:
    print "<!-- {} -->".format(vmi['href'])
    print "<DIV CLASS=td>{}</DIV>".format(vmi['virtual_machine_interface_device_owner'])
   print "</DIV>"
  print "</DIV></DIV>"

 ############################################# Floating IP ##############################################
 #
 #
 elif op == 'floating-ip':
  fipools = aWeb.get_value('fipool').split(',')
  print "<DIV CLASS=z-table><DIV CLASS=thead><DIV CLASS=th>Pool</DIV><DIV CLASS=th>Floating IP</DIV><DIV CLASS=th>Fixed IP</DIV><DIV CLASS=th>Fixed Network</DIV><DIV CLASS=th>Operations</DIV></DIV>"
  print "<DIV CLASS=tbody>"
  for fipool in fipools:
   pool  = controller.call("8082","floating-ip-pool/{}".format(fipool))['data']['floating-ip-pool']
   for fips in pool['floating_ips']:
    fip = controller.href(fips['href'])['data']['floating-ip']
    fixed =  fip.get('floating_ip_fixed_ip_address')
    print "<DIV CLASS=tr><DIV CLASS=td>{}</DIV><DIV CLASS=td>{}</DIV>".format(pool['display_name'],fip['floating_ip_address'])
    if fixed:
     # Do we select one or many VMI:s?
     print "<!-- {} -->".format(fip)
     vmi = controller.href(fip['virtual_machine_interface_refs'][0]['href'])['data']['virtual-machine-interface']
     print "<DIV CLASS=td><A TITLE='VM info' CLASS='z-op' DIV=div_os_right  URL=ajax.cgi?call=nova_action&op=info&id={0} SPIN=true>{1}</A></DIV>".format(vmi['virtual_machine_refs'][0]['to'][0],fixed)
     print "<DIV CLASS=td><A TITLE='Network info' CLASS='z-op' DIV=div_os_right  URL=ajax.cgi?call=neutron_action&op=info&id={0} SPIN=true>{1}</A></DIV>".format(vmi['virtual_network_refs'][0]['uuid'],vmi['virtual_network_refs'][0]['to'][2])
     print "<DIV CLASS=td>"
     print "<A TITLE='Info' CLASS='z-btn z-small-btn z-op' DIV=div_os_info  URL=ajax.cgi?call=neutron_action&op=print&id={} SPIN=true><IMG SRC=images/btn-info.png></A>".format(fip['href'])
     print "<A TITLE='Disassociate floating IP' CLASS='z-btn z-small-btn z-op' DIV=div_os_info  URL=ajax.cgi?call=neutron_action&op=fi_disassociate&id={} MSG='Are you sure?' SPIN=true><IMG SRC=images/btn-remove.png></A>".format(fip['uuid'])
     print "&nbsp;</DIV>"
    else:
     print "<DIV CLASS=td></DIV>"
     print "<DIV CLASS=td></DIV>"
     print "<DIV CLASS=td>"
     print "<A TITLE='Info' CLASS='z-btn z-small-btn z-op' DIV=div_os_info  URL=ajax.cgi?call=neutron_action&op=print&id={} SPIN=true><IMG SRC=images/btn-info.png></A>".format(fip['href'])
     print "<A TITLE='Associate floating IP' CLASS='z-btn z-small-btn z-op' DIV=div_os_info  URL=ajax.cgi?call=neutron_action&op=fi_associate_choose_vm&id={} OP=load><IMG SRC=images/btn-add.png></A>".format(fip['uuid'])
     print "</DIV>"
    print "</DIV>"
  print "</DIV></DIV>" 

 elif op == 'print':
  from json import dumps
  print "<PRE>{}</PRE>".format(dumps(controller.href(id)['data'],indent=4))

 elif op == 'remove':
  ret = controller.call("8082","virtual-network/{}".format(id), method='DELETE')
  print "<DIV CLASS=z-framee>{}</DIV>".format(ret)

 elif op == 'fi_disassociate':
  fip = {'floating-ip':{'virtual_machine_interface_refs':None,'floating_ip_fixed_ip_address':None }}
  res = controller.call("8082","floating-ip/{}".format(id),args=fip,method='PUT')
  print "Floating IP association removed" if res['code'] == 200 else "Error - [{}]".format(res)

 elif op == 'fi_associate_choose_vm':
  vms = controller.call(cookie.get('os_nova_port'),cookie.get('os_nova_url') + "/servers")['data']['servers']
  print "<FORM ID=frm_fi_assoc_vm><INPUT TYPE=HIDDEN NAME=id VALUE={}>".format(id)
  print "VM: <SELECT style='width:auto; height:22px;' NAME=vm>"
  for vm in vms:
   print "<OPTION VALUE={0}#{1}>{0}</OPTION>".format(vm['name'],vm['id'])
  print "</SELECT></FORM>"
  print "<A TITLE='Choose interface' CLASS='z-btn z-small-btn z-op'  DIV=div_os_info FRM=frm_fi_assoc_vm URL=ajax.cgi?call=neutron_action&op=fi_associate_choose_interface><IMG SRC=images/btn-start.png></A>"

 elif op == 'fi_associate_choose_interface':
  vm_name,_,vm_id = aWeb.get_value('vm').partition('#')
  vmis = controller.call("8082","virtual-machine/{}".format(vm_id))['data']['virtual-machine']['virtual_machine_interface_back_refs']
  print "<FORM ID=frm_fi_assoc_vmi>"
  print "<INPUT TYPE=HIDDEN NAME=id VALUE={}>".format(id)
  print "<INPUT TYPE=HIDDEN NAME=vm VALUE={}>".format(vm_id)
  print "VM: <INPUT style='width:auto;' TYPE=TEXT VALUE={} disabled> Interface:<SELECT style='width:auto; height:22px;' NAME=vmi>".format(vm_name)
  for vmi in vmis:
   uuid = vmi['uuid']
   vmi = controller.href(vmi['href'])['data']['virtual-machine-interface']
   iip = controller.href(vmi['instance_ip_back_refs'][0]['href'])['data']['instance-ip']
   print "<OPTION VALUE={0}#{1}>{2} ({1})</OPTION>".format(uuid,iip['instance_ip_address'],iip['virtual_network_refs'][0]['to'][2])
  print "</SELECT></FORM>"
  print "<A TITLE='Change VM' CLASS='z-btn z-small-btn z-op' DIV=div_os_info URL=ajax.cgi?call=neutron_action&op=fi_associate_choose_vm&id={}><IMG SRC=images/btn-back.png></A>".format(id)
  print "<A TITLE='Commit'    CLASS='z-btn z-small-btn z-op' DIV=div_os_info URL=ajax.cgi?call=neutron_action&op=fi_associate FRM=frm_fi_assoc_vmi><IMG SRC=images/btn-start.png></A>"

 elif op == 'fi_associate':
  from json import dumps
  vmid  = aWeb.get_value('vm')
  vmiid,_,ip = aWeb.get_value('vmi').partition('#')
  vmi = controller.call("8082","virtual-machine-interface/{}".format(vmiid))['data']['virtual-machine-interface']
  fip = { 'floating-ip':{ 'floating_ip_fixed_ip_address':ip, 'virtual_machine_interface_refs':[ {'href':vmi['href'],'attr':None,'uuid':vmi['uuid'],'to':vmi['fq_name'] } ] } }
  res = controller.call("8082","floating-ip/{}".format(id),args=fip,method='PUT')
  if res['code'] == 200:
   print "Floating IP association created"
  else:
   print "Error - [{}]".format(res)
