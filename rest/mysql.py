__author__ = "Zacharias El Banna"
__version__ = "18.05.31GA"
__status__ = "Production"
__add_globals__ = lambda x: globals().update(x)


#
#
def dump(aDict):
 from subprocess import check_output
 if aDict.get('username') and aDict.get('password') and aDict.get('database'):
  db,username,password = aDict['database'],aDict['username'],aDict['password']
 else:
  from zdcp.SettingsContainer import SC
  db,username,password = SC['system']['db_name'], SC['system']['db_user'], SC['system']['db_pass']
 try:
  mode = aDict.get('mode','structure')
  cmd  = ["mysqldump", "-u" + username, "-p" + password, db]
  output = []

  if   mode == 'structure':
   cmd.extend(['--no-data','--add-drop-database'])
  elif mode == 'database':
   output.append("SET sql_mode='NO_AUTO_VALUE_ON_ZERO';")
   cmd.extend(['-c','--skip-extended-insert'])

  if aDict.get('full',True):
   output.extend(["DROP DATABASE IF EXISTS %s;"%db,"CREATE DATABASE %s;"%db])
  else:
   cmd.extend(['--no-create-info','--skip-triggers'])
  output.append("USE %s;"%db)
  data = check_output(cmd)
  for line in data.split('\n'):
   if not line[:2] in [ '/*','--']:
    if "AUTO_INCREMENT=" in line:
     parts = line.split();
     for indx, part in enumerate(parts):
      if "AUTO_INCREMENT=" in part:
       parts.remove(part)
       break
     line = " ".join(parts)
    output.append(line)
  res = 'OK'
 except Exception as e:
  output = ["DumpError:{}".format(str(e))]
  res = 'NOT_OK'
 return {'res':res, 'output':output,'mode':mode,'full':aDict.get('full',True)}

#
#
def restore(aDict):
 from subprocess import check_output
 if aDict.get('username') and aDict.get('password'):
  username,password = aDict['username'],aDict['password']
 else:
  from zdcp.SettingsContainer import SC
  username,password = SC['system']['db_user'], SC['system']['db_pass']

 try:
  cmd  = ["mysql","--init-command='SET SESSION FOREIGN_KEY_CHECKS=0;'", "-u%s"%username, "-p%s"%password, '<',aDict['file']]
  output = check_output(" ".join(cmd), shell=True)
  return { 'res':'OK','output':output.split('\n') }
 except Exception as e:
  return {'res':'NOT_OK', 'output':[str(e)] }

#
#
def diff(aDict):
 from difflib import unified_diff
 with open(aDict['file']) as f:
  data = f.read() 
 ret = {}
 aDict.update({'mode':'structure'})
 db = dump(aDict)
 ret['database'] = db['res']
 ret['output'] = [line for line in unified_diff(db['output'],data.split('\n'),fromfile='dbase',tofile=aDict['file'])]
 ret['diffs'] = 0
 for line in ret['output']:
  if "@@" in line:
   ret['diffs'] += 1
 return ret
