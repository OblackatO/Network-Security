from PyPDF2 import PdfFileReader
from PyPDF2.generic import Destination
from PyPDF2.generic import PdfObject
file1 = open('pdf1.pdf','rb')
filer = PdfFileReader(file1)
"""
dest = Destination(PdfObject(),25,'/Fit')#'Jointe au CV'
print(filer.getDestinationPageNumber(dest))

--> I cannot create a Destination(dest) because I cannot create
a PdfObject like the function Destination asks me for. 
I've already imported the PdfObject library and I tried to 
use it with an argument 'Jointe au CV', thr str I want to find
in the PDF file, but I got an error saying the PdfObject 
function does not accept parameters. I don't understand what
I Have to do in order to fullfill the parameter 'title' of the
function Destination.""" 