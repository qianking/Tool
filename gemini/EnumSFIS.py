from enum import Enum, auto

base_url = "http://sfistsp-szascd0-n0.sz.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx/"


class eLogInOut(Enum):
    Login = 1
    Logout = 2


class GETVERSION(Enum):
    PSN = auto()
    ABBStatus = auto()
    SNA = auto()
    StationName = auto()
    ModelName = auto()
    SSN = auto()
    ITEMINFO = auto()
    MNAME = auto()
    CLEI = auto()
    ShippingCodeVersion = auto()
    ISN = auto()
    MO = auto()


class Enum_Url(Enum):

    WTSP_ASSIGN_DEVICE = base_url + "WTSP_ASSIGN_DEVICE"
    WTSP_CHKROUTE = base_url + "WTSP_CHKROUTE"
    WTSP_CHKROUTE_AOILOC = base_url + "WTSP_CHKROUTE_AOILOC"
    WTSP_DEVIF_MO = base_url + "WTSP_DEVIF_MO"
    WTSP_GETI1394 = base_url + "WTSP_GETI1394"
    WTSP_GETIMAC = base_url + "WTSP_GETIMAC"
    WTSP_GETIMAC_T = base_url + "WTSP_GETIMAC_T"
    WTSP_GETLABEL = base_url + "WTSP_GETLABEL"
    WTSP_GETVERSION = base_url + "WTSP_GETVERSION"
    WTSP_INPUTGSDATA = base_url + "WTSP_INPUTGSDATA"
    WTSP_LOADINFO = base_url + "WTSP_LOADINFO"
    WTSP_LOADKEY = base_url + "WTSP_LOADKEY"
    WTSP_LOGINOUT = base_url + "WTSP_LOGINOUT"
    WTSP_LOGINOUT_PROGID = base_url + "WTSP_LOGINOUT_PROGID"
    WTSP_ONLINE_REWORK_N = base_url + "WTSP_ONLINE_REWORK_N"
    WTSP_REPAIR = base_url + "WTSP_REPAIR"
    WTSP_REPAIR_LOC = base_url + "WTSP_REPAIR_LOC"
    WTSP_RESULT = base_url + "WTSP_RESULT"
    WTSP_RESULT_MASSDATA = base_url + "WTSP_RESULT_MASSDATA"
    WTSP_SEND_MAIL = base_url + "WTSP_SEND_MAIL"
    WTSP_SSD_INPUTDATA = base_url + "WTSP_SSD_INPUTDATA"
    WTSP_TSP_GET_INPUTDATA = base_url + "WTSP_TSP_GET_INPUTDATA"
