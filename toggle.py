import warnings
warnings.filterwarnings("ignore")
import json
import os
import sys
from comtypes import CoInitialize, CoUninitialize, CLSCTX_ALL, GUID
from pycaw.pycaw import AudioUtilities, IMMDeviceEnumerator, EDataFlow, DEVICE_STATE
import ctypes
import ctypes.wintypes

CONFIG_PATH = os.path.join(os.environ["APPDATA"], "AudioToggler", "config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        sys.exit("No config found. Run setup.exe first.")
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def get_all_playback_ids():
    from pycaw.pycaw import AudioUtilities
    devices = AudioUtilities.GetAllDevices()
    return {d.id: d for d in devices if d.id}

def get_default_device_id():
    from pycaw.pycaw import AudioUtilities
    devices = AudioUtilities.GetAllDevices()
    for d in devices:
        if d.id:
            # Check against Windows default via GetSpeakers ID
            pass
    # Use EDataFlow and IMMDeviceEnumerator directly
    from comtypes import CoCreateInstance
    from pycaw.pycaw import IMMDeviceEnumerator, EDataFlow, DEVICE_STATE
    enumerator = CoCreateInstance(
        GUID("{BCDE0395-E52F-467C-8E3D-C4579291692E}"),
        IMMDeviceEnumerator,
        CLSCTX_ALL
    )
    default = enumerator.GetDefaultAudioEndpoint(EDataFlow.eRender.value, 1)
    return default.GetId()

def set_default_device(device_id):
    import comtypes
    from comtypes import CoCreateInstance, CLSCTX_ALL, GUID, IUnknown
    
    CLSID_PolicyConfig = GUID("{870AF99C-171D-4F9E-AF0D-E63DF40C2BC9}")
    
    class IPolicyConfig(comtypes.IUnknown):
        _iid_ = GUID("{F8679F50-850A-41CF-9C72-430F290290C8}")
        _methods_ = [
            comtypes.STDMETHOD(comtypes.HRESULT, "GetMixFormat"),
            comtypes.STDMETHOD(comtypes.HRESULT, "GetDeviceFormat"),
            comtypes.STDMETHOD(comtypes.HRESULT, "ResetDeviceFormat"),
            comtypes.STDMETHOD(comtypes.HRESULT, "SetDeviceFormat"),
            comtypes.STDMETHOD(comtypes.HRESULT, "GetProcessingPeriod"),
            comtypes.STDMETHOD(comtypes.HRESULT, "SetProcessingPeriod"),
            comtypes.STDMETHOD(comtypes.HRESULT, "GetShareMode"),
            comtypes.STDMETHOD(comtypes.HRESULT, "SetShareMode"),
            comtypes.STDMETHOD(comtypes.HRESULT, "GetPropertyValue"),
            comtypes.STDMETHOD(comtypes.HRESULT, "SetPropertyValue"),
            comtypes.STDMETHOD(comtypes.HRESULT, "SetDefaultEndpoint",
                [ctypes.c_wchar_p, ctypes.c_uint]),
            comtypes.STDMETHOD(comtypes.HRESULT, "SetEndpointVisibility"),
        ]
    
    policy = CoCreateInstance(CLSID_PolicyConfig, IPolicyConfig, CLSCTX_ALL)
    policy.SetDefaultEndpoint(device_id, 0)  # 0 = eConsole

def main():
    CoInitialize()
    try:
        config = load_config()
        selected_ids = config["devices"]

        all_devices = get_all_playback_ids()
        available = [d_id for d_id in selected_ids if d_id in all_devices]

        if not available:
            sys.exit("No configured devices are currently available.")

        current_id = get_default_device_id()

        if current_id in available:
            idx = available.index(current_id)
            next_idx = (idx + 1) % len(available)
        else:
            next_idx = 0

        set_default_device(available[next_idx])

    finally:
        CoUninitialize()

if __name__ == "__main__":
    main()