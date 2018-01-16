"""Module docstring.

Tools REST module

"""
__author__ = "Zacharias El Banna"
__version__ = "17.11.01GA"
__status__ = "Production"

#
def installation(aDict):
 from .. import PackageContainer as PC
 from ..tools.installation import install
 settings = {}
 for s in dir(PC):
  if not s[0:2] == '__':
   settings[s]= getattr(PC,s,None) 
 res = install(settings)
 ret = {'result':'OK', 'info':res}
 return ret

#
def sync_devicetypes(aDict):
 from os import listdir, path as ospath
 from importlib import import_module
 from ..core.dbase import DB
 path  = ospath.abspath(ospath.join(ospath.dirname(__file__), '../devices'))
 types = []
 new   = 0
 for file in listdir(path):
  pyfile = file[:-3]
  if file[-3:] == ".py" and pyfile[:2] != "__":
   try:
    mod = import_module("sdcp.devices.{}".format(pyfile))
    type = getattr(mod,'__type__',None)
    if type:
     types.append({'name':pyfile, 'base':type })
   except:
    pass
 with DB() as db:
  sql ="INSERT INTO devicetypes(name,base) VALUES ('{}','{}') ON DUPLICATE KEY UPDATE id = id"
  for type in types:
   try:
    type['db'] = db.do(sql.format(type['name'],type['base']))
    new += type['db']
   except Exception,e :
    print "DB:{}".format(str(e))

 ret = {'result':'OK', 'types':types, 'found':len(types), 'new':new, 'path':path }
 return ret

#
def sync_menuitems(aDict):
 from os import listdir, path as ospath
 from importlib import import_module
 from ..core.dbase import DB
 path  = ospath.abspath(ospath.join(ospath.dirname(__file__), '../site'))
 items = []
 for file in listdir(path):
  pyfile = file[:-3]
  if file[-3:] == ".py" and pyfile[:2] != "__":
   try:
    mod  = import_module("sdcp.site.{}".format(pyfile))
    icon = getattr(mod,'__icon__',None)
    if not icon: continue
    else:  items.append({'name':pyfile, 'icon':icon})
   except: pass
 new   = 0
 with DB() as db:
  sql ="INSERT INTO resources(title,href,icon,type,user_id,inline) VALUES ('{}','{}','{}','menuitem',1,1) ON DUPLICATE KEY UPDATE id = id"
  for item in items:
   try:
    item['db'] = db.do(sql.format(item['name'].title(),"sdcp.cgi?call=%s_main"%item['name'],item['icon']))
    new += item['db']
   except: pass
 return {'result':'OK', 'menuitems':items, 'found':len(items), 'new':new, 'path':path }

#
# db_table(columns)
# - columns is a string list x,y,z,..
#
def db_table(aDict):
 from ..core.dbase import DB
 cols = aDict.get('columns','*')
 tbl  = aDict.get('table','devices')
 ret  = {'result':'OK'}
 with DB() as db:
  ret['found'] = db.do("SELECT {} FROM {}".format(cols,tbl))
  ret['db'] = db.get_rows() if ret['found'] > 0 else []
 return ret
