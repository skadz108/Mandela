from exploit.restore import restore_file
from pathlib import Path
import json
import plistlib
from dataclasses import dataclass
from typing import List, Any
running = True
passed_check = False
current_model_name = ''
gestalt_path = Path.joinpath(Path.cwd(), 'com.apple.MobileGestalt.plist')
selected_tweaks_file = Path.joinpath(Path.cwd(), 'selected_tweaks.json')

def load_selected_tweaks():
    if selected_tweaks_file.exists():
        with open(selected_tweaks_file, 'r') as f:
            return json.load(f)
    return []

def save_selected_tweaks():
    with open(selected_tweaks_file, 'w') as f:
        json.dump([tweak.path for tweak in selectedTweaks], f)

@dataclass
class GestaltKey:
    path: str
    value: Any
    name: str

baseKeys = [
    GestaltKey(
        path = "CacheExtra.oPeik/9e8lQWMszEjbPzng.ArtworkDeviceSubType",
        value = 2556,
        name = "Toggle Dynamic Island"
    ),
    GestaltKey(
        path="CacheExtra.oPeik/9e8lQWMszEjbPzng.ArtworkDeviceProductDescription",
        value = current_model_name,
        name = "Set Model Name"
    ),
    GestaltKey(
        path = "CacheExtra.j8/Omm6s1lsmTDFsXjsBfA",
        value = True,
        name = "Toggle Always-On Display"
    ),
    GestaltKey(
        path = "CacheExtra.2OOJf1VhaM7NxfRok3HbWQ",
        value = True,
        name = "Always-On Display Fix"
    ),
    GestaltKey(
        path = "CacheExtra.qeaj75wk3HF4DwQ8qbIi7g",
        value = True,
        name = "Toggle Stage Manager (Unstable)"
    ),
    GestaltKey(
        path = "CacheExtra.mmu76v66k1dAtghToInT8g",
        value = False,
        name = "Disable Wallpaper Parallax"
    ),
    GestaltKey(
        path = "CacheExtra.QHxt+hGLaBPbQJbXiUJX3w",
        value = True,
        name = "Toggle Boot Chime"
    ),
    GestaltKey(
        path = "CacheExtra.yhHcB0iH0d1XzPO/CFd3ow",
        value = True,
        name = "Toggle Apple Pencil (doesn't actually function)"
    ),
    GestaltKey(
        path = "CacheExtra.37NVydb//GP/GrhuTN+exg",
        value = True,
        name = "Toggle 80% Charging Limit"
    ),
    GestaltKey(
        path = "CacheExtra.LBJfwOEzExRxzlAnSuI7eg",
        value = True,
        name = "(DANGEROUS, USE AT YOUR OWN RISK) Toggle Internal Build"
    )
]

selectedTweaks: List[GestaltKey] = []
def toggleTweakSelection(id):
    tweak = baseKeys[id]
    if tweak not in selectedTweaks:
        selectedTweaks.append(tweak)
    else:
        selectedTweaks.remove(tweak)
    save_selected_tweaks()

def initialize_tweaks():
    global selectedTweaks
    saved_tweaks = load_selected_tweaks()
    selectedTweaks = [tweak for tweak in baseKeys if tweak.path in saved_tweaks]

def isSelected(id):
    return baseKeys[id].path in [tweak.path for tweak in selectedTweaks]

def applyTweaks(plist):
    for gestalt_key in baseKeys:
        path_parts = gestalt_key.path.split('.')
        current = plist
        for part in path_parts[:-1]:
            if part not in current:
                if gestalt_key in selectedTweaks:
                    current[part] = {}
                else:
                    break
            current = current[part]
        
        if gestalt_key in selectedTweaks:
            current[path_parts[-1]] = gestalt_key.value
        elif path_parts[-1] in current:
            del current[path_parts[-1]]

while running:
    if not passed_check and Path.exists(gestalt_path) and Path.is_file(gestalt_path):
        passed_check = True
    if passed_check:
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
        for i, key in enumerate(baseKeys, 1):
            if key.name == "Set Model Name":
                is_selected = current_model_name != ''
            else:
                is_selected = isSelected(i - 1)
            
            selected_indicator = '[Y] ' if is_selected else ''
            print(f"{i}. {selected_indicator}{key.name}")
        print('11. Apply')
        print('12. Exit\n')
        print('13. (Debug) Print Selected Tweaks\n')
        page = None
        try:
            user_input = input('Enter a number: ')
            if user_input.strip():  # Check if input is not empty
                page = int(float(user_input))
            else:
                print("Please select an option.")
        except ValueError:
            print("Please enter a valid number.")

        if page is not None:
            if 1 <= page <= len(baseKeys):
                key = baseKeys[page - 1]
                if key.name == "Set Model Name":
                    print('\n\nSet Model Name')
                    print('Leave blank to turn off custom name.\n')
                    name = input('Enter Model Name: ')
                    current_model_name = name
                else:
                    toggleTweakSelection(page - 1)
            elif page == len(baseKeys) + 1:
                print()
                with open(gestalt_path, 'rb') as in_fp:
                    plist = plistlib.load(in_fp)
                applyTweaks(plist)
                with open(gestalt_path, 'wb') as out_fp:
                    plistlib.dump(plist, out_fp)
                restore_file(fp=gestalt_path, restore_path='/var/containers/Shared/SystemGroup/systemgroup.com.apple.mobilegestaltcache/Library/Caches/', restore_name='com.apple.MobileGestalt.plist')
                input("Success! Reboot your device to see the changes.\n\nIf you've enabled Always-On Display or Stage Manager, use our helper shortcut at https://routinehub.co/shortcut/19597/ to enable functionality.")
            elif page == len(baseKeys) + 2:
                print('Thank you for using Mandela!')
                running = False
            elif page == len(baseKeys) + 3:
                print(selectedTweaks)
        else:
            print("Please select an option")
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
