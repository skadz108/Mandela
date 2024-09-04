# Mandela
A simple iOS customization tool based on [Codename Nugget](https://github.com/leminlimez/Nugget). Works up to iOS 18.0db8.

## Usage
- Install `pymobiledevice3` in your Python environment
- Run `app.py`
- On first run, you'll be prompted to get the MobileGestalt file from your device. Send the shortcut link to your device, run it with Shortcuts, and put the file in the same folder as `app.py`
- Select your tweaks
- Apply tweaks
- Reboot device
- Profit

**Find My must be disabled before applying. This is a limitation of stock iOS when restoring backups. You may re-enable Find My after applying your tweaks.**

**If you enable Always-On Display or Stage Manager, you'll need to re-run the shortcut to enable full functionality.**

## Adding custom Gestalt keys
Mandela uses a simple array to store the default tweaks. However, this is open to allow for anyone to add their own keys and use them. Follow the steps below to add your own. Please beware that incorrect/invalid modifications to MobileGestalt can cause permanent damage to your device. Mandela and its authors are not responsible for any damages caused by your usage of this feature.

- Open `app.py` in a code editor of choice.
- You'll find `baseKeys`. This is a list of `GestaltKey` objects separated by commas.
- Make a new GestaltKey object with the `path` (dot-separated) of the entry you'd like to add (e.g. `CacheExtra.QHxt+hGLaBPbQJbXiUJX3w` or `CacheExtra.mmu76v66k1dAtghToInT8g`), the `value` you'd like to set the key to (`True` or `False` for boolean keys), and the `name` you'd like to display in the menu.
- Save your changes and run the script.
- You should see your new tweak appear in the menu. Congratulations, you can now add new tweaks to Mandela!

## Credits
- [Codename Nugget](https://github.com/leminlimez/Nugget) for the exploit library and some UI components
- [dootskyre](https://github.com/dootskyre) for the helper shortcut
- Special thanks to [Lrdsnow](https://github.com/Lrdsnow), [Little_34306](https://github.com/34306), [BrocoDev](https://github.com/Broco8Dev), [MildPepperCat](https://github.com/ktrrbypass), and [lunginspector](https://github.com/lunginspector) for assistance and support.

### Disclaimer
This project is intended for educational and personal purposes only. The code provided in this repository is designed to demonstrate the concepts of software exploitation and system vulnerabilities within a controlled, legal, and ethical environment.
