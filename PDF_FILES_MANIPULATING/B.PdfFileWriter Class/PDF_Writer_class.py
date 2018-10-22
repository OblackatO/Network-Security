from PyPDF2 import PdfFileReader, PdfFileWriter

file1 = open('pdf1.pdf','rb')
file2 = open('output.pdf','wb')
filer = PdfFileReader(file1)
filew = PdfFileWriter()
#Cloning PDF reader with its properties ; see notes to see other ways to do this
try:
	filew.cloneDocumentFromReader(filer)
except Exception as e:
	print('Not possible to clone PDF File:',e)
try:
	filew.addBookmark('user name',1,color='1',bold=True,italic=False,fit='/Fit')
	filew.addLink(1,3,[30,30,70,70],border=['2','2','4','4'],fit='/Fit')
except Exception as e:
	print('Not possible to addBookmark or to addLink:',e)
#AddsJava script,executes when user opens it, here : printing windows
try:
	filew.addJS("this.print({bUI:true,bSilent:false,bShrinkToFit:true});")
	filew.addMetadata({'/Producer':'/User1','/CreationDate':'/30.08.1996','/CreationProgram':'Adobe Acrobat Reader DC (Windows)'})
except Exception as e:
	print('Not possible to addJS or Metadata:',e)
#Function updatePageFormFieldValues never worked
#try:
#	page = filew.getPage(2)
#	filew.updatePageFormFieldValues(page,{'/Texte1':'/Bond'})
#except Exception as e:
#	print('Not possible to update Field Values:',e)
try: 
	filew.removeImages()
	filew.removeText()
	filew.removeLinks()
except:
	print('Not possible to remove Img,Text or Links:',e)
try:
    filew.encrypt('1234',owner_pwd='1234',use_128bit=True)
    print('File encrypted')
except Exception as e:
    print('Not possible to encrypt file:',e)

filew.write(file2)
file2.close()
file1.close()


#MERGING SEVERAL PDF Files : 
"""def scan_several_pdf(file1):
	global file_c
	file_c = open(file1,'rb')
	filer = PdfFileReader(file_c)
	filew.appendPagesFromReader(filer)
	
	
def main():
	global filew
	filew = PdfFileWriter()
	for item in os.listdir():
		if '.pdf' in item:
			print(item)
			scan_several_pdf(item)
	output = open('output_file.pdf','wb')
	filew.write(output)
	output.close()
	file_c.close()

main()

Most important Metadata Fields on a PDF File :
1. /Producer
2. /CreationDate
3. /Author
4. /Location

"""

