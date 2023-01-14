# gameshark_to_controllerpak

!!WARNING READ BEFORE DOING ANYTHING!!: This is a work in progress and CAN and LIKELY WILL CORRUPT your Gameshark!  It is provided to the community for information purposes.  Use at your own risk.  Before doing anything, have a device that can dump and reflash your Gameshark such as the RetroStage Programmer and back up of your Gameshark's rom before trying this in the likely event something goes wrong.  If you do corrupt your Gameshark, reflash it with your backup.

This was my attempt to create a python script that took Nintendo 64 Gameshark/Action Replay codes from a file exported by gamehacking.org or created by the user and importing it into a N64 controller pak (memory card) .mpk file.  Provide your own blank formatted .mpk file, which can be created by formatting a Controller Pak and dumping it with an Everdrive.  Provide a text or .yml file with the Gameshark codes.  Run the import.py script and it will generate a new .mpk file

```
python import.py formatted_controller_pak_filename.mpk gameshark_codes_filename.yml patched_controller_pak_filename.mpk
```

Copy that .mpk file to an Everdrive's SD card and use the Everdrive to import it to a Controller Pak.  Put in your Gameshark, go to Select Cheat Codes, press Z on your controller, Select Load Codes from Memory Card.  Then if you are very lucky it will actually work and load the codes onto your Gameshark.

This code is provided freely.  Feel free do what you want with it as long as you give credit to Triclon.

Questions?  Comments?  email me at triclon@gmail.com
