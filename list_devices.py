from pycaw.pycaw import AudioUtilities

devices = AudioUtilities.GetAllDevices()

for d in devices:
    print(f"Name: {d.FriendlyName}")
    print(f"ID:   {d.id}")
    print()