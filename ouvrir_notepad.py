"""Here is defined the funtion to opend the configuration file with the 
standard software to open up text file (eg NotePad)
NB : it currently only works under Windows
"""

__version__ = '0.1'
__author__ = 'Ugo'

import subprocess

def ouvrir_notepad():
	nf = 'C:/WINDOWS/system32/notepad.exe'
	arg = './configuration/config.json'
	subprocess.call([nf,arg])

##############################################################################
# Test
##############################################################################
# ouvrir_notepad()