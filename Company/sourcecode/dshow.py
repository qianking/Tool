from pygrabber.dshow_graph import FilterGraph, SystemDeviceEnum, get_moniker_name
from comtypes.persist import IPropertyBag
from pygrabber.dshow_core import GUID
from pygrabber.dshow_ids import *

class _MyFilterGraph(FilterGraph):
    def __init__(self):
        self.system_device_enum = _MySystemDeviceEnum()
        
    def get_input_devices(self):
        return self.system_device_enum.get_available_filters(DeviceCategories.VideoInputDevice)

class _MySystemDeviceEnum(SystemDeviceEnum):
    def get_available_filters(self, category_clsid):
        filter_enumerator = self.system_device_enum.CreateClassEnumerator(GUID(category_clsid), dwFlags=0)
        moniker, count = filter_enumerator.Next(1)
        result = []
        counter = 0
        while count > 0:
            result.append((counter, get_moniker_name(moniker), _get_moniker_device_path(moniker), moniker))
            moniker, count = filter_enumerator.Next(1)
            counter += 1
        return result

def _get_moniker_device_path(moniker):
    property_bag = moniker.BindToStorage(0, 0, IPropertyBag._iid_).QueryInterface(IPropertyBag)
    try:
        return property_bag.Read("DevicePath", pErrorLog=None)
    except Exception as e:
        print(f"Unable to read 'DevicePath' for moniker. Error: {e}")
        return None
    
   
def get_camera_monikers():
    graph = _MyFilterGraph()
    return graph.get_input_devices()

if "__main__" == __name__:
    print(get_camera_monikers())

