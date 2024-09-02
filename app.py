from exploit.restore import restore_file
from pathlib import Path
import plistlib
from dataclasses import dataclass
from typing import List, Any
running = True
passed_check = False
current_model_name = ''
gestalt_path = Path.joinpath(Path.cwd(), 'com.apple.MobileGestalt.plist')

def applyOperation(plist, key_path, value):
    path_parts = key_path.split('.')
    for part in path_parts[:-1]:
        if part not in plist:
            plist[part] = {}
        plist = plist[part]
    
    plist[path_parts[-1]] = value

@dataclass
class GestaltKey:
    path: str
    value: Any

baseKeys = {
    "dynamicIsland": GestaltKey(
        path="CacheExtra.oPeik/9e8lQWMszEjbPzng.ArtworkDeviceSubType",
        value=2556
    ),
    "deviceModelName": GestaltKey(
        path="CacheExtra.oPeik/9e8lQWMszEjbPzng.ArtworkDeviceProductDescription",
        value=current_model_name
    ),
    "alwaysOnDisplay": GestaltKey(
        path="CacheExtra.j8/Omm6s1lsmTDFsXjsBfA",
        value=True
    ),
    "stageManager": GestaltKey(
        path="CacheExtra.qeaj75wk3HF4DwQ8qbIi7g",
        value=True
    ),
    "wallpaperParallax": GestaltKey(
        path="CacheExtra.mmu76v66k1dAtghToInT8g",
        value=False
    ),
    "bootChime": GestaltKey(
        path="CacheExtra.QHxt+hGLaBPbQJbXiUJX3w",
        value=True
    ),
    "supportsApplePencil": GestaltKey(
        path="CacheExtra.yhHcB0iH0d1XzPO/CFd3ow",
        value=True
    ),
    "80ChargeLimit": GestaltKey(
        path="CacheExtra.37NVydb//GP/GrhuTN+exg",
        value=True
    ),
    "internalBuildVeryDangerousPleaseDontSueMeWhenYouGetBootlooped": GestaltKey(
        path="CacheExtra.LBJfwOEzExRxzlAnSuI7eg",
        value=True
    )
}

selectedTweaks: List[GestaltKey] = []
def toggleTweakSelection(id):
    tweak = list(baseKeys.values())[id]
    if tweak not in selectedTweaks:
        selectedTweaks.append(tweak)
    else:
        selectedTweaks.remove(tweak)

def isSelected(id):
    return list(baseKeys.values())[id] in selectedTweaks

def applyTweaks(plist):
    for index, gestalt_key in enumerate(baseKeys.values()):
        if isSelected(index):
            applyOperation(plist, gestalt_key.path, gestalt_key.value)

while running:
    print(r"""
  __  __                 _      _                
 |  \/  |               | |    | |               
 | \  / | __ _ _ __   __| | ___| | __ _          
 | |\/| |/ _` | '_ \ / _` |/ _ \ |/ _` |         
 | |  | | (_| | | | | (_| |  __/ | (_| |         
 |_|  |_|\__,_|_| |_|\__,_|\___|_|\__,_| _       
                               | |    (_) |      
                               | |     _| |_ ___ 
                               | |    | | __/ _ \
                               | |____| | ||  __/
                               |______|_|\__\___|
             Public Release

       Uses sparserestore by JJTech
             Written by Skadz
   Special thanks to Lrdsnow & Little_34306
    """)
    if not passed_check and Path.exists(gestalt_path) and Path.is_file(gestalt_path):
        passed_check = True
    if passed_check:
        print(f"1. {('[Y] ' if isSelected(0) else '')}Toggle Dynamic Island")
        print(f"2. {('[Y] ' if current_model_name != '' else '')}Set Device Model Name")
        print(f"3. {('[Y] ' if isSelected(2) else '')}Toggle Always On Display")
        print(f"4. {('[Y] ' if isSelected(3) else '')}Toggle Stage Manager")
        print(f"5. {('[Y] ' if isSelected(4) else '')}Disable Wallpaper Parallax")
        print(f"6. {('[Y] ' if isSelected(5) else '')}Toggle Boot Chime")
        print(f"7. {('[Y] ' if isSelected(6) else '')}Enable Apple Pencil (doesn't actually function)")
        print(f"8. {('[Y] ' if isSelected(7) else '')}Enable 80% Charging Limit")
        print(f"9. {('[Y] ' if isSelected(8) else '')}(DANGEROUS) Enable Internal Build (USE AT YOUR OWN RISK)")
        print('10. Apply')
        print('11. Exit\n')
        print('12. (Debug) Print Selected Tweaks\n')
        page = int(input('Enter a number: '))
        
        match page:
            case 1:
                toggleTweakSelection(0)
            case 2:
                print('\n\nSet Model Name')
                print('Leave blank to turn off custom name.\n')
                name = input('Enter Model Name: ')
                current_model_name = name               
            case 3:
                toggleTweakSelection(2)
            case 4:
                toggleTweakSelection(3)
            case 5:
                toggleTweakSelection(4)
            case 6:
                toggleTweakSelection(5)
            case 7:
                toggleTweakSelection(6)
            case 8:
                toggleTweakSelection(7)
            case 9:
                toggleTweakSelection(8)
            case 10:
                print()
                with open(gestalt_path, 'rb') as in_fp:
                    plist = plistlib.load(in_fp)
                applyTweaks(plist)
                with open(gestalt_path, 'wb') as out_fp:
                    plistlib.dump(plist, out_fp)
                restore_file(fp=gestalt_path, restore_path='/var/containers/Shared/SystemGroup/systemgroup.com.apple.mobilegestaltcache/Library/Caches/', restore_name='com.apple.MobileGestalt.plist')
                input("Success! Reboot your device to see the changes.\n\nIf you've enabled Always-On Display or Stage Manager, use our helper shortcut at https://routinehub.co/shortcut/19597/ to enable functionality.")
            case 11:
                print('Goodbye!')
                running = False
            case 12:
                print(selectedTweaks)
    else:
        print(r"""
  ______                     
 |  ____|                    
 | |__   _ __ _ __ ___  _ __ 
 |  __| | '__| '__/ _ \| '__|
 | |____| |  | | | (_) | |   
 |______|_|  |_|  \___/|_|   
                                  
""")
        print('No MobileGestalt file found!')
        print('You can get the file from your device with this shortcut: https://routinehub.co/shortcut/19597/')
        print(f"Place the file in '{Path.cwd()}' with the name 'com.apple.MobileGestalt.plist'")
        print('Remember to make a backup!!\n')
        print('1. Retry')
        print('2. Enter path\n')
        choice = int(input('Enter number: '))
        if choice == 2:
            new_path = input('Enter new path to file: ')
            gestalt_path = Path(new_path)
