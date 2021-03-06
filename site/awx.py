"""Module docstring.

HTML5 Ajax AWX module

"""
__author__= "Zacharias El Banna"
__version__ = "1.0GA"
__status__ = "Production"

#
#
def manage(aWeb):
 args = aWeb.get_args2dict()
 data = aWeb.rest_call("awx_inventory_list",args)
 print "<NAV><UL>"
 print "<LI><A CLASS=z-op HREF=%s     target=_blank>UI</A></LI>"%(data['webpage'])
 print "<LI><A CLASS='z-op reload' DIV=main URL='zdcp.cgi?awx_manage&id=%s'></A></LI>"%(data['id'])
 print "<LI CLASS='right navinfo'><A>%s</A></LI>"%(data['hostname'])
 print "</UL></NAV>"
 print "<SECTION CLASS=content ID=div_content><SECTION CLASS=content-left ID=div_content_left><ARTICLE><P>Inventories</P>"
 print "<DIV CLASS=table><DIV CLASS=thead><DIV CLASS=th>ID</DIV><DIV CLASS=th>Name</DIV><DIV CLASS=th>&nbsp;</DIV></DIV><DIV CLASS=tbody>"
 for row in data['inventories']:
  print "<DIV CLASS=tr><DIV CLASS=td>%s</DIV><DIV CLASS='td maxed'>%s</DIV><DIV CLASS=td><DIV CLASS=controls>"%(row['id'],row['name'])
  print aWeb.button('items',DIV='div_content_right', URL='zdcp.cgi?awx_inventory&node=%s&id=%s'%(data['node'],row['id']), SPIN='true', TITLE='Hosts list')
  print aWeb.button('trash',DIV='div_content_right', URL='zdcp.cgi?awx_inventory_delete&node=%s&id=%s'%(data['node'],row['id']), SPIN='true', TITLE='Delete inventory', MSG='Really delete inventory?')
  print "</DIV></DIV></DIV>"
 print "</DIV></DIV>"
 print "</ARTICLE></SECTION><SECTION CLASS=content-right ID=div_content_right></SECTION>"
 print "</SECTION>"

#
#
def inventory(aWeb):
 args = aWeb.get_args2dict()
 if aWeb['op'] == 'delete_list':
  opres = aWeb.rest_call("awx_inventory_delete_hosts",args)
 else:
  opres = ""
 res = aWeb.rest_call("awx_inventory_info",args)
 print "<ARTICLE><P>Hosts</P><DIV CLASS=controls>"
 print aWeb.button('reload', DIV='div_content_right', URL='zdcp.cgi?awx_inventory&node=%s&id=%s'%(aWeb['node'],aWeb['id']), SPIN='true')
 print aWeb.button('add',    DIV='div_content_right', URL='zdcp.cgi?awx_inventory_device_search&node=%s&id=%s'%(aWeb['node'],aWeb['id']), TITLE='Sync with AWX')
 print aWeb.button('trash',  DIV='div_content_right', URL='zdcp.cgi?awx_inventory&node=%s&id=%s&op=delete_list'%(aWeb['node'],aWeb['id']), MSG='Delete hosts?', FRM='host_list', SPIN='true')
 print "</DIV><SPAN CLASS=results>%s</SPAN><FORM ID=host_list>"%(opres)
 print "</DIV><DIV CLASS=table><DIV CLASS=thead><DIV CLASS=th>ID</DIV><DIV CLASS=th>Name</DIV><DIV CLASS=th>Description</DIV><DIV CLASS=th>Groups</DIV><DIV CLASS=th>&nbsp;</DIV></DIV><DIV CLASS=tbody>"
 for row in res['hosts']:
  name = "<A CLASS=z-op DIV=div_content_right URL='zdcp.cgi?device_info&id=%s'>%s</A>"%(row['instance_id'],row['name']) if row['instance_id'] != "" else row['name']
  print "<DIV CLASS=tr><DIV CLASS=td>%s</DIV><DIV CLASS=td>%s</DIV><DIV CLASS=td>%s</DIV><DIV CLASS=td>%s</DIV><DIV CLASS=td><DIV CLASS=controls>"%(row['id'],name,row['description'],",".join([k['name'] for k in row['groups']]))
  print "<INPUT TYPE=CHECKBOX VALUE=%(id)s NAME='host_%(id)s'>"%row
  print "</DIV></DIV></DIV>"
 print "</DIV></DIV></DIV>"
 print "</FORM></ARTICLE>"

#
#
def inventory_delete(aWeb):
 args = aWeb.get_args2dict()
 res = aWeb.rest_call("awx_inventory_delete",args)
 print "<ARTICLE>Delete result: %s</ARTICLE>"%res

#
#
def inventory_device_search(aWeb):
 print "<ARTICLE STYLE='display:inline-block'>"
 print "<FORM ID=awx_choose>"
 print "<INPUT TYPE=HIDDEN NAME=id VALUE=%s>"%(aWeb['id'])
 print "<INPUT TYPE=HIDDEN NAME=node VALUE=%s>"%(aWeb['node'])
 print "<SPAN>Sync devices matching field:</SPAN><SELECT CLASS='background' ID='field' NAME='field'><OPTION VALUE='hostname'>Hostname</OPTION><OPTION VALUE='type'>Type</OPTION><OPTION VALUE='ip'>IP</OPTION><OPTION VALUE='mac'>MAC</OPTION><OPTION VALUE='id'>ID</OPTION></SELECT>"
 print "<INPUT CLASS='background' TYPE=TEXT ID='search' NAME='search' STYLE='width:200px' REQUIRED>"
 print "</FORM><DIV CLASS=controls>"
 print aWeb.button('back',DIV='div_content_right',URL='zdcp.cgi?awx_inventory&id=%s&node=%s'%(aWeb['id'],aWeb['node']))
 print aWeb.button('forward',DIV='div_content_right',URL='zdcp.cgi?awx_inventory_device_choose',FRM='awx_choose', SPIN='true')
 print "</DIV></ARTICLE>"

#
#
def inventory_device_choose(aWeb):
 args = aWeb.get_args2dict()
 res = aWeb.rest_call("device_list",args)
 print "<ARTICLE STYLE='display:inline-block'>"
 print "<FORM ID=awx_choose>"
 print "<INPUT TYPE=HIDDEN NAME=id VALUE=%s>"%(aWeb['id'])
 print "<INPUT TYPE=HIDDEN NAME=node VALUE=%s>"%(aWeb['node'])
 print "</DIV><DIV CLASS=table><DIV CLASS=thead><DIV CLASS=th>Id</DIV><DIV CLASS=th>FQDN</DIV><DIV CLASS=th>&nbsp;</DIV></DIV><DIV CLASS=tbody>"
 for row in res['data']:
  print "<DIV CLASS=tr><DIV CLASS=td>%(id)s</DIV><DIV CLASS=td>%(hostname)s.%(domain)s</DIV><DIV CLASS=td><DIV CLASS=controls><INPUT TYPE=CHECKBOX VALUE=%(id)s NAME=device_%(id)s></DIV></DIV></DIV>"%row
 print "</DIV></DIV></FORM><DIV CLASS=controls>"
 print aWeb.button('back',DIV='div_content_right',URL='zdcp.cgi?awx_inventory_device_search&id=%s&node=%s'%(aWeb['id'],aWeb['node']))
 print aWeb.button('forward',DIV='div_content_right',URL='zdcp.cgi?awx_inventory_device_sync',FRM='awx_choose', SPIN='true')
 print "</DIV></ARTICLE>"

#
#
def inventory_device_sync(aWeb):
 args = aWeb.get_args2dict()
 res = aWeb.rest_call("awx_inventory_sync",args)
 print "<ARTICLE><P>Synced Devices</P><DIV CLASS=controls>"
 print aWeb.button('forward', DIV='div_content_right', URL='zdcp.cgi?awx_inventory&node=%s&id=%s'%(aWeb['node'],aWeb['id']))
 print "</DIV><DIV CLASS=table><DIV CLASS=tbody>"
 for row in res['devices']:
  print "<DIV CLASS=tr><DIV CLASS=td>%s</DIV><DIV CLASS=td>%s.%s</DIV><DIV CLASS=td>%s</DIV><DIV CLASS=td>%s</DIV></DIV>"%(row['id'],row['hostname'],row['domain'],row['ip'],row['awx'])
 print "</DIV></DIV>"
 print "</ARTICLE>"
