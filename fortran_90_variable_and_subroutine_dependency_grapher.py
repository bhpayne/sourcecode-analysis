# create map of who calls what, generate graphviz output file to create picture

# -read in fortran 90 file which compiles
# -find subroutine, create list of subroutines
# -find function, create list of functions
# -for each subroutine, get list of arguments
# -for each function, get list of arguments
# for each subroutine, check that "implicit none" is in place
# for each subroutine, check that "implicit none" is in place
# for each subroutine, find all instances of "call X"
# -for each function, find all instance of that function

# advanced:
# -if function occurs within subroutine or main body, function must be declared

# array dimension 0: name
# array dimension 1: number of arguments
# array dimension 2: list of arguments
# array dimension 3: line start
# array dimension 4: line end
# array dimension 5: absolute line start
# array dimension 6: absolute line end
# array dimension 7: list of usedOnLine

# http://docs.python.org/faq/programming.html

# for compiling via system commands, getting hostname, testing existance of files
import os
# regular expressions
# see http://www.regular-expressions.info/python.html
import re

def formatInputF90(inputfile,allLines):
  lineIndx=0
  f = open(inputfile)
  line = f.readline()
  andFound=0 # false
  commentedLine=0
  while line:
    lineIndx=lineIndx+1
    line=line.rstrip() # remove end-of-line
    line=re.sub('^[\ ]+','',line) # replace " " with empty string, leaving word
    if re.search('!.*',line) or re.search('^$',line): # eliminate comments on same line as word
      commentedLine=1
    else: 
      commentedLine=0
    # if line ends with "&" then append next line (eliminate multi-line commands from the F90)
    if (andFound==1):
      line=lineWithAnd+line
    if commentedLine==0 and re.search('&',line,re.IGNORECASE):
      #print('AND found line %d' % lineIndx)
      andFound=1 # true
      line=re.sub('&','',line)
      lineWithAnd=line
    elif commentedLine==0:
      andFound=0 # false
      allLines.append(line)
      #print ("line %d: "+line) % (lineIndx) # show which line word is on
    line = f.readline()
  f.close()
  #print allLines
  return [allLines]
  # returns lines from the input file cleaned up for analyis

def formatInputRemoveInterface(allLines,reducedAllLines):
  lineIndx=0
  interfaceFound=0
  for line in allLines:
    lineIndx=lineIndx+1
    if re.search('^[\ ]*interface.*',line,re.IGNORECASE):
      interfaceFound=1 # true
    if interfaceFound==0:
      reducedAllLines.append(line)
    if re.search('^[\ ]*end[\ ]+interface.*',line,re.IGNORECASE):
      interfaceFound=0 # false
  return [reducedAllLines]

def formatInputF77(inputfile,allLines):
  lineIndx=0
  f = open(inputfile)
  line = f.readline()
  andFound=0 # false
  while line:
    lineIndx=lineIndx+1
    line=line.rstrip() # remove end-of-line
    #line=re.sub('!+.','',line) # eliminate comments
    line=re.sub('^[cC].+','',line) # eliminate comments
    line=re.sub('^[\*].+','',line) # eliminate comments
    line=re.sub('^[ ]+','',line) # replace " " with empty string
    line=re.sub('[\t]+',' ',line) # replace tabs with empty string
    if (andFound==1):
      line=lineWithAnd+line
    if re.search('[\ ]{5}[c\*&]',line): # line continuation
      andFound=1 # true
      line=re.sub('[c\*&]','',line)
      lineWithAnd=line
    else:
      andFound=0 # false
      if line != '':
        allLines.append(line)
        print line
      #print ("line %d: "+line) % (lineIndx) # show which line word is on
    line = f.readline()
  f.close()
  #print allLines
  return [allLines]
  # returns lines from the input file cleaned up for analyis

# function to find "call" or "function" or "subroutine" in input file
def findAllWords(inputfile,allWords,word):
  # "inputfile"= cleaned up input F90, all lines
  # "allWords" is an empty array to fill with the results
  # "word" = what to look for
  lineIndx=0
  absStart=0
  absEnd=0
  if word.lower() == 'function':
    findme=("^[a-zA-Z0-9\*_: ]*%s[a-zA-Z0-9\*_: ]*" % word) # "function" can be proceeded by type
  else:
    findme=("^[ ]*%s" % word) # only lines with start with "word" get found.  
  for line in inputfile:
    lineIndx=lineIndx+1
    endline=0
    if re.search(findme,line,re.IGNORECASE):
      #print ("line %d: "+line) % (lineIndx) # show which line word is on
      if re.search('^end',line):
        print
      else:
        findEnd='^end '+word+'[a-zA-Z0-9\*_: ]*'
        if word.lower() != 'call':
          endline=findCorrespondingEnd(inputfile,lineIndx,findEnd)
        allWords.append([line,0,'',lineIndx,endline,absStart,absEnd,'']) 
        # line, number of arguments, arguments, start line, end line, absStart,absEnd,usedOnLine
  return [allWords]
  # returns the entire line, including the word "call" and arguments

def findCorrespondingEnd(inputfile,startline,word):
  # "inputfile"= cleaned up input F90, all lines
  # "allWords" is an empty array to fill with the results
  # "word" = what to look for
  lineIndx=0
  endline=0
  #print startline, ':'+word+':'
  findInHere=inputfile[startline-1:len(inputfile)]
  #print 'startline: '+str(startline)
  #print 'find: '+word
  for line in findInHere:
    lineIndx=lineIndx+1
    if re.search(word+'[a-zA-Z_,\ ]',line,re.IGNORECASE):
      #print lineIndx,line
      #print ("line %d: "+line) % (lineIndx) # show which line word is on
      endline=lineIndx+startline
      break
  if endline==0:
    print 'ERROR: end line not found:',word,' starting from',startline
    print findInHere[0]
  return endline

def parseEachItem(typeFCS,item):
  #print(item)
  #nameStrng=re.sub('^[a-zA-Z]+[\ ]+','',item) # replace replace words prior to (, leaving name(arg1,arg2)
  nameStrng=re.sub('^[a-zA-Z0-9\ _\*:]*[\ ]([a-zA-Z0-9_]*)','\\1',item) # replace replace words prior to (, leaving name(arg1,arg2)
  name=re.sub('\(([a-zA-Z,_\(\)0-9\.\+\*-:\'\ ]+)\)','',nameStrng)

  argsList=re.sub('[a-zA-Z0-9_\ \*:]+\(','',item) # everything before the first parenthesis
  argsList=re.sub('[\)][ ]*\Z','',argsList) # the last parenthesis
  argsList=argsList.split(',')

  indx=-1
  for item in argsList:
    indx=indx+1
    #print item
    if re.search('[a-zA-Z0-9_,]+\([a-zA-Z0-9_,]+[^\)]',item,re.IGNORECASE):
      argsList[indx:indx+2]=[','.join(argsList[indx:indx+2])]
  indx=-1
  for item in argsList:
    indx=indx+1
    #print item
    if re.search('[a-zA-Z0-9_,]+\([a-zA-Z0-9_,]+[^\)]',item,re.IGNORECASE):
      argsList[indx:indx+2]=[','.join(argsList[indx:indx+2])]
  #print('NAME = '+name)
  #print('ARGS = ')
  #print(argsList)
  return [name,argsList]

def parseArray(allLines,allWhat,typ):
  #print "\n"+typ+": \n****************"
  findAllWords(allLines,allWhat,typ)
  numFN=len(allWhat)
  #print numFN
  indx=0
  for item in allWhat:
    indx=indx+1
    output=parseEachItem(typ,item[0])
    item[0]=output[0] # name
    item[1]=len(output[1]) # number of arguments
    item[2]=output[1] # arguments
    #print item
  return [allWhat]

def findUse(allLines,allFUNCTIONS):
  for func in allFUNCTIONS:
    lineIndx=0
    #print func[0]
    instances=[]
    for line in allLines:
      lineIndx=lineIndx+1
      #print line
      anyString='[a-zA-Z0-9_,\(\)\ :=\*]*'
      if re.search(anyString+'[\ ]'+func[0]+anyString,line,re.IGNORECASE) and (lineIndx<func[3] or lineIndx>func[4]):
        #print 'found instance',lineIndx
        instances.append(lineIndx)
    #print instances
    func[7]=instances

# main body

# arrays
allFUNCTIONS=[]
allSUBROUTINES=[]
allCALLS=[]
prog=[]
allLines=[]
reducedAllLines=[]

#inputfile='transfer.double.capture.f'
#formatInputF77(inputfile,allLines)

inputfile='quasi1d_vary_active_no_uf_SVN2319py_20110501.f90'
formatInputF90(inputfile,allLines)
formatInputRemoveInterface(allLines,reducedAllLines)
del allLines
allLines=reducedAllLines
#for line in allLines:
  #print line
#exit()

#print "\nMAIN \n***************"
findAllWords(allLines,prog,'program')
prog=prog[0] # there is only one program
prog[0]=re.sub('^[a-zA-Z]+[\ ]+','',prog[0]) # replace "function " with empty string, leaving name(arg1,arg2)
#print prog

parseArray(allLines,allFUNCTIONS,'function')
findUse(allLines,allFUNCTIONS)
#print 'functions ******************'
#for func in allFUNCTIONS:
  #print func

parseArray(allLines,allSUBROUTINES,'subroutine')
#print 'subroutines *****************'
#for subr in allSUBROUTINES:
  #print subr
parseArray(allLines,allCALLS,'call')


# ********* now we can do cool stuff **********************

#for line in range(prog[3],prog[4]): # all lines in the main body

mapName='F90_map'
file=open(mapName+'.gv','w')
file.write("strict digraph F90varDepend {")
# which subroutines get called from main?
for whichCall in range(len(allCALLS)):
  if (allCALLS[whichCall][3]>prog[3] and allCALLS[whichCall][3]<prog[4]):
    file.write(prog[0]+'->'+allCALLS[whichCall][0]+'\n')
# which functions get used main?
for whichFunc in range(len(allFUNCTIONS)):
  for whichUse in range(len(allFUNCTIONS[whichFunc][7])):
    if allFUNCTIONS[whichFunc][7][whichUse]>prog[3] and allFUNCTIONS[whichFunc][7][whichUse]<prog[4]:
      file.write(prog[0]+'->'+allFUNCTIONS[whichFunc][0]+'\n')
# subroutines use which functions?
for whichSub in range(len(allSUBROUTINES)):
  for whichFunc in range(len(allFUNCTIONS)):
    for whichUse in range(len(allFUNCTIONS[whichFunc][7])):
      if (allFUNCTIONS[whichFunc][7][whichUse]>allSUBROUTINES[whichSub][3] and allFUNCTIONS[whichFunc][7][whichUse]<allSUBROUTINES[whichSub][4]):
        file.write(allSUBROUTINES[whichSub][0]+'->'+allFUNCTIONS[whichFunc][0]+'\n')
# subroutines call other subroutines?
for whichSub in range(len(allSUBROUTINES)):
  for whichCall in range(len(allCALLS)):
    if (allCALLS[whichCall][3]>allSUBROUTINES[whichSub][3] and allCALLS[whichCall][3]<allSUBROUTINES[whichSub][4]):
      file.write(allSUBROUTINES[whichSub][0]+'->'+allCALLS[whichCall][0]+'\n')
# functions call subroutines?
for whichFunc in range(len(allFUNCTIONS)):
  for whichCall in range(len(allCALLS)):
    if (allCALLS[whichCall][3]>allFUNCTIONS[whichFunc][3] and allCALLS[whichCall][3]<allFUNCTIONS[whichFunc][4]):
      file.write(allFUNCTIONS[whichFunc][0]+'->'+allCALLS[whichCall][0]+'\n')
# functions use other functions?
for whichFunc in range(len(allFUNCTIONS)):
  for usesFunc in range(len(allFUNCTIONS)):
    for whichUse in range(len(allFUNCTIONS[whichFunc][7])):
      if (allFUNCTIONS[whichFunc][whichUse]<allFUNCTIONS[usesFunc][3] and allFUNCTIONS[whichFunc][whichUse]<allFUNCTIONS[usesFunc][4]):
        file.write(allFUNCTIONS[whichFunc][0]+'->'+allFUNCTIONS[usesFunc][0]+'\n')
 
file.write('overlap=false\nfontsize=12;')
file.write('label="function dependences\\nExtracted from quasi1d_template.f90 \\nlayed out by Graphviz\"')
file.write("\n}\n")
file.close()
cmd='neato -Tpng '+mapName+'.gv > '+mapName+'.png'
os.system(cmd)

