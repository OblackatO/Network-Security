from bs4 import BeautifulSoup,Comment
bsinstance = BeautifulSoup(open('ltps_parse.html'),"lxml")

#Adds a string to the tags and a comment (can be done separetely): 
commenttoadd = Comment("Here's the comment my friend")
links = bsinstance.find('link')
links.append('test1')
links.append(commenttoadd)
print links 

"""#Insert a string to the tag (works like append except we can choose the position):
links = bsinstance.find('link')
links.append('test1')# IF i wrote : links.clear() : The contents would be deleted, but not the attrs
links.insert(0,'test2') 
print links """