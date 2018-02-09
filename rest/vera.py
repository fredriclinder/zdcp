"""Module docstring.

Vera API module

"""
__author__ = "Zacharias El Banna"
__version__ = "18.02.09GA"
__status__ = "Production"

#
def rest(aDict):
 from ..devices.vera import Device
 try:
  controller = Device(aDict['host'])
  ret = controller.call(3480,aDict['api'],aDict['args'],aDict['method'])
 except Exception,e:
  ret = e[0] 
 return ret

#
#
def status(aDict):
 from ..devices.vera import Device
 try:
  controller = Device(aDict['host'])
  ret = controller.call(3480,"id=sdata")['data']
 except Exception,e:
  ret = e[0] 
 return ret
