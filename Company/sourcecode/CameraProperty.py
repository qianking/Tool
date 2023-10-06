import clr
clr.AddReference(r".\dll\AForge.Video")
clr.AddReference(r".\dll\AForge.Video.DirectShow")

from AForge.Video import *
from AForge.Video.DirectShow import *

def get_camera_property_range(MonikerString):

    MonikerString = fr"@device:pnp:{MonikerString}"
    #videoDevices = FilterInfoCollection(FilterCategory.VideoInputDevice)
    #videoDevice = VideoCaptureDevice(videoDevices[1].MonikerString)

    cameraproperty = dict()
    videoDevice = VideoCaptureDevice(MonikerString)
    property = videoDevice.GetVideoPropertyRange(VideoProcAmpProperty.Brightness)
    cameraproperty['Brightness'] = (property[1], property[2], property[3], property[4])
    property = videoDevice.GetVideoPropertyRange(VideoProcAmpProperty.Contrast)
    cameraproperty['Contrast'] = (property[1], property[2], property[3], property[4])
    property = videoDevice.GetVideoPropertyRange(VideoProcAmpProperty.Saturation)
    cameraproperty['Saturation'] = (property[1], property[2], property[3], property[4])
    property = videoDevice.GetVideoPropertyRange(VideoProcAmpProperty.Saturation)
    cameraproperty['Saturation'] = (property[1], property[2], property[3], property[4])
    property = videoDevice.GetCameraPropertyRange(CameraControlProperty.Exposure)
    cameraproperty['Exposure'] = (property[1], property[2], property[3], property[4])
    property = videoDevice.GetVideoPropertyRange(VideoProcAmpProperty.Gain)
    cameraproperty['Gain'] = (property[1], property[2], property[3], property[4])
    property = videoDevice.GetVideoPropertyRange(VideoProcAmpProperty.WhiteBalance)
    cameraproperty['WhiteBalance'] = (property[1], property[2], property[3], property[4])
    return cameraproperty

# def get_camera_property_range1():
#     videoDevices = FilterInfoCollection(FilterCategory.VideoInputDevice)
#     videoDevice = VideoCaptureDevice(videoDevices[1].MonikerString)
#     print(videoDevices[1].MonikerString)
#     cameraproperty = dict()
#     #videoDevice = VideoCaptureDevice(MonikerString)
#     property = videoDevice.GetVideoPropertyRange(VideoProcAmpProperty.Brightness)
#     cameraproperty['Brightness'] = (property[1], property[2], property[3], property[4])
#     property = videoDevice.GetVideoPropertyRange(VideoProcAmpProperty.Contrast)
#     cameraproperty['Contrast'] = (property[1], property[2], property[3], property[4])
#     property = videoDevice.GetVideoPropertyRange(VideoProcAmpProperty.Saturation)
#     cameraproperty['Saturation'] = (property[1], property[2], property[3], property[4])
#     property = videoDevice.GetVideoPropertyRange(VideoProcAmpProperty.Saturation)
#     cameraproperty['Saturation'] = (property[1], property[2], property[3], property[4])
#     property = videoDevice.GetCameraPropertyRange(CameraControlProperty.Exposure)
#     cameraproperty['Exposure'] = (property[1], property[2], property[3], property[4])
#     property = videoDevice.GetVideoPropertyRange(VideoProcAmpProperty.Gain)
#     cameraproperty['Gain'] = (property[1], property[2], property[3], property[4])
#     property = videoDevice.GetVideoPropertyRange(VideoProcAmpProperty.WhiteBalance)
#     cameraproperty['WhiteBalance'] = (property[1], property[2], property[3], property[4])
#     return cameraproperty

#print(get_camera_property_range(r"\\?\usb#vid_046d&pid_0825&mi_00#6&2129e6f8&0&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\global"))

#get_camera_property_range1()