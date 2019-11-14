import subprocess

def ouvrir_notepad():
	nf = 'C:/WINDOWS/system32/notepad.exe'
	arg = 'C:/Users/Ugo/Desktop/IMTA-PE-S3/IMTA-PE-S3/config.json'
	subprocess.call([nf,arg])

ouvrir_notepad()

