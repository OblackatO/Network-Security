from PyPDF2 import PdfFileMerger

file1 = open('pdf1.pdf','rb')
file2 = open('pdf2.pdf','rb')
file3 = open('Finaloutput.pdf','wb')
filem = PdfFileMerger()
#Method like filer.appendPagesFromReader()
try:
	filem.append(file2)
	filem.merge(2,file1,pages=(2,5))
	filem.addNamedDestination('test_dest',2)
	filem.write(file3)
except Exception as e:
	print('Not possible to append or merge or addNamedDestination or write to the file:',e)
file1.close()
file2.close()
file3.close()


