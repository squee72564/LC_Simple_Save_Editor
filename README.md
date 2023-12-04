# Lethal Company Simple Save Editor
This is a simple python tool that allows you to change parameters within the encrypted LC save files.

## Requirements:
1. [Python](https://www.python.org/downloads/)
2. [pycryptodome package](https://pypi.org/project/pycryptodome/)
3. Existing Lethal Company save file

## How to use
1. Clone this git repo into desired directory with "git clone https://github.com/squee72564/LC_Simple_Save_Editor.git"
2. Install pycryptodome package. This can be done by typing "pip install requirements.txt" in the base directory.
3. Navigate to the src directory
4. Run the python script SSE.py with the file path of the save file to change as a command line argument, ie: 
 python .\SSE.py '~\AppData\LocalLow\ZeekerssRBLX\Lethal Company\LCSaveFile1' 
5. Change the text fields and check boxes as desired.
6. Press the submit button.

The save file should now be re-encrypted with the edited information.