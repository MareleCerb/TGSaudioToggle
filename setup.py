import warnings
warnings.filterwarnings("ignore")

import json
import os
import sys
import shutil
import winreg
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pycaw.pycaw import AudioUtilities

CONFIG_DIR = os.path.join(os.environ["APPDATA"], "TGSaudioToggle")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")
APP_NAME = "TGSaudioToggle"
APP_VERSION = "1.0.0"

README_CONTENT = """TGSaudioToggle v2.0.0
By The Great Stag (TGS)
https://www.thegreatstag.com

---

WHAT IS THIS?

TGSaudioToggle lets you switch between audio output devices instantly
using any macro key, hotkey tool, or shortcut launcher.

No bloat. No tray icon. No UI. Just press your key and your audio switches.

---

HOW TO USE IT

1. Point your macro key or hotkey to TGSaudioToggle.exe
2. Press it to cycle through your selected audio devices
3. That's it

Works with any tool or device that can launch a program, including:

Keyboard & mouse software:
- Razer Synapse (BlackWidow, Huntsman, Naga, etc.)
- Logitech G Hub (G915, G Pro, G502, etc.)
- Corsair iCUE (K100, K95, Scimitar, etc.)
- SteelSeries GG (Apex, Rival series)
- Roccat Swarm (Vulcan, Kone series)
- HyperX NGENUITY
- ASUS Armory Crate (ROG/TUF keyboards)
- MSI Center
- Wooting Analog SDK / Wootility

Macro & automation tools:
- AutoHotkey (free, Windows native scripting)
- AutoIt
- Keyboard Maestro (Mac)
- PowerToys Run (Windows)

Stream decks & control surfaces:
- Elgato Stream Deck (all models)
- Loupedeck (Live, CT, +)
- Tourbox
- X-Keys

Voice & accessibility tools:
- VoiceAttack (voice commands)
- NVIDIA RTX Voice shortcuts

Any tool that has a "Launch Program", "Run Application",
or "Open File" action can run TGSaudioToggle.exe.

---

TO RECONFIGURE

Run setup.exe again from wherever you downloaded it.
Your previous selection will be overwritten.

Power users: you can also edit the config file directly.
Location: %APPDATA%\\TGSaudioToggle\\config.json

The config is a plain JSON file with a list of device IDs in cycle order:
{
  "devices": [
    "{0.0.0.00000000}.{your-device-id-1}",
    "{0.0.0.00000000}.{your-device-id-2}"
  ]
}

Device IDs can be found using tools like list_devices.py or
by checking the Windows Registry under:
HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\MMDevices\\Audio\\Render

---

TO UNINSTALL

Go to Windows Settings > Apps > TGSaudioToggle > Uninstall.
This will remove the app and all its files cleanly.

---

TROUBLESHOOTING

Audio not switching?
- Make sure you selected at least 2 devices during setup
- Make sure the selected devices are still plugged in and active
- Run setup.exe again to reconfigure
- Check that config.json exists at: %APPDATA%\\TGSaudioToggle\\config.json
- Open config.json with notepad and verify it contains at least 2 device IDs

Macro key not working?
- Make sure your macro tool is set to "Launch Program" or "Run Application"
- Point it to TGSaudioToggle.exe, not setup.exe
- Make sure the path has no typos and the file exists in the install folder
- Try running TGSaudioToggle.exe manually by double-clicking it first and checking that the default device changes correctly.

Device not showing up in setup?
- The device must be active and plugged in during setup
- Disabled devices are hidden -- enable them in Windows Sound settings first
  (Right-click speaker icon > Sounds > Playback tab > right-click > Show Disabled Devices)
- Virtual audio devices (VB-Cable, Voicemeeter) are supported if set to Active

App installed but nothing happens when macro fires?
- Check that TGSaudioToggle.exe is still in the install folder
- Check Windows Defender or antivirus -- it may have quarantined the exe
- Try adding TGSaudioToggle.exe as an exception in your antivirus software

After Windows update, devices stopped switching?
- Windows updates can reset device states or change device IDs
- Run setup.exe again to re-detect and reselect your devices

Running multiple audio interfaces?
- If you have an external DAC, USB interface, or audio card, make sure
  it shows as Active in Windows Sound settings before running setup

---

ANTICHEAT SAFE?

Yes. TGSaudioToggle only calls the Windows audio API.
It does not interact with any game process, memory, or input.
It is safe to use with Vanguard, EAC, VAC, BattlEye, Steam, and all
major anticheats.

---

BUILT BY THE GREAT STAG (TGS)
A platform for systems-thinkers, automation builders, and gaming-minded operators.

https://www.thegreatstag.com

---
"""

def get_playback_devices():
    devices = AudioUtilities.GetAllDevices()
    return [
        (d.FriendlyName, d.id)
        for d in devices
        if d.id
        and d.FriendlyName
        and d.id.startswith("{0.0.0.")
        and str(d.state) == "AudioDeviceState.Active"
    ]

def save_config(device_ids):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump({"devices": device_ids}, f, indent=2)

def write_readme(install_dir):
    readme_path = os.path.join(install_dir, "README.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(README_CONTENT)
    return readme_path

def register_uninstaller(install_dir):
    uninstall_key = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\TGSaudioToggle"
    config_dir = os.path.join(os.environ["APPDATA"], "TGSaudioToggle")
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, uninstall_key)
        winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, APP_NAME)
        winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, APP_VERSION)
        winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, install_dir)
        winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ,
            f'cmd /c rmdir /s /q "{install_dir}" & '
            f'rmdir /s /q "{config_dir}" & '
            f'reg delete "HKCU\\{uninstall_key}" /f')
        winreg.SetValueEx(key, "NoModify", 0, winreg.REG_DWORD, 1)
        winreg.SetValueEx(key, "NoRepair", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Warning: could not register uninstaller: {e}")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("TGSaudioToggle Setup")
        self.geometry("500x580")
        self.resizable(False, False)

        self.devices = get_playback_devices()
        self.checkboxes = {}
        self.install_dir = ctk.StringVar(
            value=os.path.join(os.environ["LOCALAPPDATA"], "TGSaudioToggle")
        )
        self.readme_path = None

        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="🔊 TGSaudioToggle Setup",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(30, 5))
        ctk.CTkLabel(self, text="Select the devices you want to cycle through.",
                     font=ctk.CTkFont(size=13),
                     text_color="gray").pack(pady=(0, 20))

        frame = ctk.CTkScrollableFrame(self, width=420, height=220)
        frame.pack(padx=30, pady=(0, 20))

        if not self.devices:
            ctk.CTkLabel(frame, text="No active playback devices found.",
                         text_color="red").pack(pady=10)
        else:
            for name, device_id in self.devices:
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(frame, text=name, variable=var,
                                     font=ctk.CTkFont(size=12))
                cb.pack(anchor="w", padx=10, pady=6)
                self.checkboxes[device_id] = var

        ctk.CTkLabel(self, text="Install location:",
                     font=ctk.CTkFont(size=13)).pack(anchor="w", padx=30)

        folder_frame = ctk.CTkFrame(self, fg_color="transparent")
        folder_frame.pack(fill="x", padx=30, pady=(5, 25))

        ctk.CTkEntry(folder_frame, textvariable=self.install_dir,
                     width=330).pack(side="left")
        ctk.CTkButton(folder_frame, text="Browse", width=80,
                      command=self._browse).pack(side="left", padx=(10, 0))

        ctk.CTkButton(self, text="Install", height=45,
                      font=ctk.CTkFont(size=15, weight="bold"),
                      command=self._install).pack(padx=30, fill="x")

    def _browse(self):
        folder = filedialog.askdirectory()
        if folder:
            self.install_dir.set(folder)

    def _show_success(self, install_dir, toggle_dst):
        win = ctk.CTkToplevel(self)
        win.title("Installation Complete")
        win.geometry("420x280")
        win.resizable(False, False)
        win.grab_set()

        ctk.CTkLabel(win, text="✅ TGSaudioToggle installed!",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(30, 10))

        ctk.CTkLabel(win, text=f"Location: {install_dir}",
                     font=ctk.CTkFont(size=12),
                     text_color="gray").pack(pady=(0, 5))

        ctk.CTkLabel(win, text=f"Point your macro to:\n{toggle_dst}",
                     font=ctk.CTkFont(size=12),
                     text_color="gray").pack(pady=(0, 20))

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Read README",
                      width=160, height=38,
                      fg_color="transparent",
                      border_width=2,
                      command=lambda: subprocess.Popen(["notepad.exe", self.readme_path])
                      ).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="Close",
                      width=160, height=38,
                      command=lambda: [win.destroy(), self.destroy()]
                      ).pack(side="left", padx=10)

    def _install(self):
        selected = [dev_id for dev_id, var in self.checkboxes.items() if var.get()]

        if len(selected) < 2:
            messagebox.showerror("Error", "Please select at least 2 devices.")
            return

        install_dir = self.install_dir.get()

        try:
            os.makedirs(install_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Error", f"Could not create install folder:\n{e}")
            return

        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")

        toggle_src = os.path.join(base_dir, "toggle.exe")
        toggle_dst = os.path.join(install_dir, "TGSaudioToggle.exe")

        if not os.path.exists(toggle_src):
            messagebox.showerror("Error", f"toggle.exe not found at:\n{toggle_src}")
            return

        try:
            shutil.copy2(toggle_src, toggle_dst)
        except Exception as e:
            messagebox.showerror("Error", f"Could not copy TGSaudioToggle.exe:\n{e}")
            return

        save_config(selected)
        self.readme_path = write_readme(install_dir)
        register_uninstaller(install_dir)

        self._show_success(install_dir, toggle_dst)

if __name__ == "__main__":
    app = App()
    app.mainloop()