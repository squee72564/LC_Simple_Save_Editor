
# Lethal Company Simple Save Editor
This is a simple python tool that allows you to change parameters within the encrypted LC save files.

## Updated for v50!
New features added include:
- New planets
- New kitchen knife and easter egg items

## Requirements:
1. [Python](https://www.python.org/downloads/) (I use version 3.11.2 and there may be conflicts with older versions)
2. [pycryptodome package](https://pypi.org/project/pycryptodome/)
3. Existing Lethal Company save file

## How to use
1. Clone this git repo into desired directory with:
    
```
git clone https://github.com/squee72564/LC_Simple_Save_Editor.git
```

2. Install necessary python packages. This can be done by typing `pip install -r requirements.txt` in the base directory.
3. Navigate to the src directory
4. Run the python script SSE.py with the file path of the save file to change as a command line argument, ie:

```
python .\SSE.py ~\AppData\LocalLow\ZeekerssRBLX\Lethal Company\LCSaveFile1
```
* Alternatively you can just run the python script without passing in a file path and you will be prompted to select a file in the gui. (Doing it this way may be problematic if the folder where the save file is located is hidden.)

```
python .\SSE.py
```

5. Change the text fields, check boxes, and edit items as desired.
6. Press the overwrite button.

The save file should now be re-encrypted with the edited information.

Within LC_Simple_Save_Editor/src/encryption/encryptTools.py are the functions to actually encrypt and decrypt the save files.

### Example Images

![LC Simple Save Editor](https://github.com/squee72564/LC_Simple_Save_Editor/blob/main/img/cap.png)
![LC Simple Save Editor 2](https://github.com/squee72564/LC_Simple_Save_Editor/blob/main/img/cap2.png)
