from PyPDF2 import PdfFileReader
from PyPDF2.generic import Destination 
pwf = False #if it changes to True password found 
#Dictionaries for BruteForce attack
dict1 = ['hllo','helo','ehlo','lohe','hello']
dict2 = ['bb','buy','bey','buz','bhj','bye']
#Main program
file1 = open('Candidature.pdf','rb') # adapt the name of the file here. 
filer = PdfFileReader(file1)
print('Checking if file is encrypted or not:')
#Checking encryption of the file and make bruteforce attack if user wants to
if filer.isEncrypted == True:
	res = input('PDF File is encrypted, BruteForce it ? [Y/N]')
	if res == 'N':
		print('No BruteForce attack')
		pass
	if res == 'Y':
		res = input('Do you want to use default dictionaties of the program? (With most common passwords for PDF files)[Y/N]')
		if res == 'N':
			dicti = input('Input the full path location(since the parent folder) to your own dictionarie:')
			print('Starting BruteForce attack')
			user_dicti = open(dicti,'r')
			for item in user_dicti:
				try:
					decryptresult = filer.decrypt(item)
					if decryptresult == 0 :
						print('[>]Word:',str(item),'failed')
					if decryptresult == 1 :
						print('[>]Password Found:',str(item))
						pwf = True
					if decryptresult == 2 :
						print('[>]Owner password Found:',str(item))
						pwf = True
						sys.exit(0)
				except Exception as e :
					print(e)
		if res == 'Y':
			print('Starting BruteForce attack')
			for item in dict1:
				try:
					decryptresult = filer.decrypt(item)
					if decryptresult == 0 :
						print('[>]Word:',str(item),'failed')
					if decryptresult == 1 :
						print('[>]Password Found:',str(item))
						pwf = True
					if decryptresult == 2 :
						print('[>]Owner password Found:',str(item))
						pwf = True
				except NotImplementedError :
					print('Type of PDF file encryption not supported')
					pass
			if pwf == False : 
				print('Password not found, trying dict2 now')
				for item in dict2:
					try:
						decryptresult = filer.decrypt(item)
						if decryptresult == 0 :
							print('[>]Word:',str(item),'failed')
						if decryptresult == 1 :
							print('[>]Password Found:',str(item))
							pwf = True
						if decryptresult == 2 :
							print('[>]Owner password Found:',str(item))
							pwf = True
					except Exception as e :
						print(e)
				if pwf == False : 
					print('Password not found on dict2')
	print('')
else :
	print('File is not encrypted')
	print('')
try:
	print('Outlines : ')
	print(filer.getOutlines())
	print('')
except:
	print('Outlines not available')
	print('')
print('Named destinations : ')
print(filer.getNamedDestinations())
print('')
try:
	fand = filer.getFormTextFields()
except:
	print('Text fields are not available')
if fand != {} :
	print('Fields and their data:')
	for key in fand:
		print(key,':',fand[key])
	print('')
if fand == {}:
	print('No Text fields available on the PDF file')
print('File XMP Metadata')
try:
	metadata = filer.getXmpMetadata()
except Exception as e :
	print ('Cannot get XmpMetadata')
	print('Send this error message to pegom0896@gmail.com:',e)
	print('XmpMetada may also not be a parameter of the PDF File, sometimes that happens,\
	even if Text Fields are on the PDF File ')
if (metadata == None) or (metadata.custom_properties == {}):
	print('XMP metadata not available')
	print('')
else : 
	print('XmpMetadata : ')
	for item in metadata.custom_properties:
		print(item,':',metadata.custom_properties[item])
	print('')
	print(metadata.custom_properties) # In order to see the whole dictionary
print("File information (becomes metadata if XMP not available, can also have metadata even if Xmp's present)")
try:
	fileinfo = filer.getDocumentInfo()
except Exception as e:
	print('Cannot get DocumentInfo')
	print('Send this error message to pegom0896@gmail.com:',e)
	print('XmpMetada may also not be a parameter of the PDF File, sometimes that happens,\
	even if Text Fields are on the PDF File ')
if (fileinfo == None) or (fileinfo == {}) :
	print("Document's Info not available")
else : 
	for key in fileinfo:
		print(key,':',fileinfo[key])
	print('')
print('Page mode : ')
try:
	print(filer.getPageMode())
except:
	print('Page Mode is not available')
print('')
print('Page Layout : ')
try:
	print(filer.getPageLayout())
except:
	print('Page Layout is not available')
print('')
print('Text of each page of the file : ')
for page in range(1,filer.getNumPages()):
	try:
		cpage = filer.getPage(page)
	except Exception as e:
		print('Cannot get page')
		print('Send an email to .... with this error message:',e)
	print('Page number'+':'+str(page),'contents')
	try:
		print(cpage.getContents()) # the getContents function makes part of the Page Object class. 
	except Exception as e :
		print('Cannot get page contents')
		print('Send an email to ... with this error message',e)
	print('Page Text, number'+':'+str(page))
	try:
		extracted_text = cpage.extractText()
	except Exception as e :
		print('Cannot extract text from page')
		print('Send an email to ... with this error message',e)
	print(extracted_text)
	print('')
	print('Looking for specific string in the extracted text :')
	if 'stages' in extracted_text: #change the 'stage string to something you want to find on the PDF file'
		print ("string 'stages' in page",page) 
		print('')
	else : 
		print("string 'stages' not in page",page)
		print('')
file1.close()


#Read contents from PDF file

"""from PyPDF2 import PdfFileReader
pdffile = open('uncrypted_pdf_file2.pdf','rb')
pdfreader = PdfFileReader(pdffile)
for page in range(0,pdfreader.numPages):
	pagepdf = pdfreader.getPage(page)
	print ('Page number:'+str(page))
	pagetxt = pagepdf.extractText()
	print (pagetxt)
	print ('')
	print ('')"""