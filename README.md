TGSaudioToggle v2.0.0
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
Location: %APPDATA%\TGSaudioToggle\config.json

The config is a plain JSON file with a list of device IDs in cycle order:
{
  "devices": [
    "{0.0.0.00000000}.{your-device-id-1}",
    "{0.0.0.00000000}.{your-device-id-2}"
  ]
}

Device IDs can be found using tools like list_devices.py or
by checking the Windows Registry under:
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\MMDevices\Audio\Render

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
- Check that config.json exists at: %APPDATA%\TGSaudioToggle\config.json
- Open config.json with notepad and verify it contains at least 2 device IDs

Macro key not working?
- Make sure your macro tool is set to "Launch Program" or "Run Application"
- Point it to TGSaudioToggle.exe, not setup.exe
- Make sure the path has no typos and the file exists in the install folder
- Try running TGSaudioToggle.exe manually by double-clicking it first and
  checking that the default device changes correctly

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
