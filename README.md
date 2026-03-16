# 🔊 TGSaudioToggle

**Switch between audio output devices instantly with a single keypress.**

No bloat. No tray icon. No UI. Just press your macro key and your audio switches.

Built by [The Great Stag (TGS)](https://www.thegreatstag.com)

---

## What is it?

TGSaudioToggle lets you cycle through your selected audio output devices using any macro key, hotkey tool, or shortcut launcher.

- 2 devices → ping-pong back and forth
- 3+ devices → cycle through in order
- Unplugged devices are skipped automatically

---

## How to install

1. Download `setup.exe` from the [latest release](https://github.com/MareleCerb/TGSaudioToggle/releases)
2. Run it
3. Select the audio devices you want to cycle through
4. Choose an install folder
5. Click **Install**

---

## How to use

Point your macro key or hotkey to `TGSaudioToggle.exe` in the install folder.

Works with any tool that can launch a program:

| Category | Tools |
|---|---|
| Keyboard & mouse | Razer Synapse, Logitech G Hub, Corsair iCUE, SteelSeries GG, Roccat Swarm, HyperX NGENUITY, ASUS Armory Crate, MSI Center, Wooting Wootility |
| Macro & automation | AutoHotkey, AutoIt, PowerToys |
| Stream decks | Elgato Stream Deck, Loupedeck, Tourbox, X-Keys |
| Voice | VoiceAttack, NVIDIA RTX Voice |

If it has a "Launch Program" or "Run Application" action — it works.

---

## To reconfigure

Run `setup.exe` again. Your previous selection will be overwritten.

**Power users:** you can also edit the config file directly.

Location: `%APPDATA%\TGSaudioToggle\config.json`
```json
{
  "devices": [
    "{0.0.0.00000000}.{your-device-id-1}",
    "{0.0.0.00000000}.{your-device-id-2}"
  ]
}
```

---

## To uninstall

Go to **Windows Settings > Apps > TGSaudioToggle > Uninstall.**

This removes the app, the config, and all associated files cleanly.

---

## Troubleshooting

**Audio not switching?**
- Make sure you selected at least 2 devices during setup
- Make sure the selected devices are still plugged in and active
- Run `setup.exe` again to reconfigure
- Check that `config.json` exists at `%APPDATA%\TGSaudioToggle\config.json`

**Macro key not working?**
- Make sure your macro tool is set to "Launch Program" or "Run Application"
- Point it to `TGSaudioToggle.exe`, not `setup.exe`
- Try running `TGSaudioToggle.exe` manually first to confirm it works

**Device not showing up in setup?**
- The device must be active and plugged in during setup
- Enable disabled devices: right-click speaker icon > Sounds > Playback tab > right-click > Show Disabled Devices
- Virtual audio devices (VB-Cable, Voicemeeter) are supported if set to Active

**Nothing happens when macro fires?**
- Check that `TGSaudioToggle.exe` is still in the install folder
- Check Windows Defender / antivirus -- it may have quarantined the exe
- Add `TGSaudioToggle.exe` as an exception in your antivirus

**After a Windows update, devices stopped switching?**
- Windows updates can reset device states or change device IDs
- Run `setup.exe` again to re-detect and reselect your devices

---

## Anticheat safe?

Yes. TGSaudioToggle only calls the Windows Core Audio API. It does not interact with any game process, memory, or input. Safe with Vanguard, EAC, VAC, BattlEye, Steam, and all major anticheats.

---

## Tech stack

- Python 3.14
- [pycaw](https://github.com/AndreMiras/pycaw) — Windows Core Audio API
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — dark mode UI
- [PyInstaller](https://pyinstaller.org) — compiled to .exe

---

## License

Free to use. Built by [The Great Stag (TGS)](https://www.thegreatstag.com).
