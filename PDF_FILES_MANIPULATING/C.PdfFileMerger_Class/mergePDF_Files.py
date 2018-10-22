from PyPDF2 import PdfFileReader, PdfFileMerger
import os 

global filem
filem = PdfFileMerger()

def merge_file(filen):
	file1 = open(filen,'rb')
	filer = PdfFileReader(file1)
	filem.append(filer)
	file1.close()

for item in os.listdir():
	if '.pdf' in item :
		merge_file(item)
	else:
		pass

file1 = open('output.pdf','wb')
filem.write(file1)
file1.close()


