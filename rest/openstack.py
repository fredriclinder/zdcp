"""Module docstring.

Openstack Portal REST module
- Hardcoded for the moment

"""
__author__ = "Zacharias El Banna"
__version__ = "17.11.01GA"
__status__ = "Production"

def application(aDict):
 from .. import PackageContainer as PC
 from ..core.dbase import DB
 from ..devices.openstack import OpenstackRPC
 from ..core.logger import log
 ret = {'result':'OK'}
 ret['title']   = "%s 2 Cloud"%(aDict.get('name','iaas'))
 ret['portal'] = "openstack_portal"
 ret['message']= "Welcome to the '%s' Cloud Portal"%(aDict.get('name','iaas'))
 cookies = {'name':aDict.get('name','iaas'),'controller':aDict.get('controller','127.0.0.1'),'appformix':aDict.get('appformix','127.0.0.1'),'main_token':aDict.get('main_token',None)}
 if cookies['main_token'] is None:
  controller = OpenstackRPC(cookies['controller'],None)
  res = controller.auth({'project':PC.openstack['project'], 'username':PC.openstack['username'],'password':PC.openstack['password']})
  cookies['main_token'] = controller.get_token()
  log("openstack_controller - login result: {}".format(str(res['result'])))
 else:
  log("openstack_controller - reusing token: {}".format(cookies['main_token']))
  controller = OpenstackRPC(cookies['controller'],cookies['main_token'])
 auth = controller.call("5000","v3/projects")
 if auth['code'] == 200:
  projects = []
  for project in auth['data']['projects']:
   projects.append({'name':project['name'], 'id':"%s_%s"%(project['id'],project['name'])})
  ret['choices'] = [{'display':'Customer', 'id':'project', 'data':projects}]
 else:
  ret['result'] = 'NOT_OK'
 ret['parameters'] = [{'display':'Username', 'id':'username', 'data':'text'},{'display':'Password', 'id':'password', 'data':'password'}]
 ret['cookie'] = ",".join(["%s=%s"%(k,v) for k,v in cookies.iteritems()])
 return ret
