import re
from tokens import Token
from remover import Remover
from syntaxanalyser import SyntaxAnalyser
errorOccurred = False
token = Token()
lineNo = 1
parser = SyntaxAnalyser()
class LexicalAnalyser:
    def __init__(self):
        global errorOccurred
        global lineNo
        # all the wordbreaks, whenever encountered, new token is created
        wordBreakers = [' ', ',', '(', '{', '[', ']', '}', ')', ';',
                        '=', '+', '-', '/', '*', ':', '>', '<', '\'', '\"', ':', '.','`']

        code = open('Sample.txt')
        remover = Remover()
        code = remover.removeComments(code)
        _length = 0
        while _length < len(code):
            i = 0
            fileLine = code[lineNo-1]
            if not fileLine:
                break
            length = 1 if len(fileLine) == 1 else len(fileLine)  # length of the line
            word = ""  # word to hold each word as we are reading character by character
            while i < length:
                # if the current character enforces word break
                if fileLine[i] in wordBreakers:
                    wordBreaker = fileLine[i]

                    if len(word) <= 1:
                        #checking for length 2 RO and INCDEC
                        if ((i+1 < length) and ((fileLine[i] == '+' and fileLine[i+1] == '+') or (fileLine[i] == '-' and fileLine[i+1] == '-') or ((fileLine[i] == '*' or fileLine[i] == '/' or fileLine[i] == '+' or fileLine[i] == '-') and fileLine[i+1] == '=') or ((fileLine[i]=='<' and fileLine[i+1]=='=') or (fileLine[i]=='>' and fileLine[i+1]=='=')))):
                            wordBreaker += fileLine[i+1]
                            i += 1
                    #ensuring the existance for floating point values 
                    if(wordBreaker == '.' and (word.isnumeric() or len(word)==0)):
                         
                        if i+1 < length and fileLine[i+1]!=' ':
                           tempWord = word+wordBreaker
                           while((i+1) < length and fileLine[i+1] not in wordBreaker):
                              tempWord+=fileLine[i+1]
                              i+=1
                           if(token.createToken(tempWord.strip(),lineNo)==False):
                               errorOccurred=True
                           word =""
                           wordBreaker=""

                    if (word != ""):
                        if(token.createToken(word.strip(), lineNo) == False):
                            errorOccurred=True 
                    # if the word breaker is a single ", indicates that a string constant is appearing
                    if fileLine[i] == '"':
                        tempWord = '"'
                        i += 1
                        while i < length:
                            if (fileLine[i] == '"'):
                                tempWord += fileLine[i]
                                break
                            tempWord += fileLine[i]
                            i += 1
                        if(token.createToken(tempWord.strip(), lineNo) == False):
                            errorOccurred=True
            # if the word breaker is a single ', indicates that a char constant is appearing
                    elif fileLine[i] == "'":
                        tempWord = "'"
                        i += 1
                        count =2
                        if fileLine[i] =='\\':
                         count = 3
                        while i < length and count:
                            tempWord += fileLine[i]
                            i += 1
                            count-=1
                        # print(fileLine[i], lineNo, tempWord)
                        if(token.createToken(tempWord.strip(), lineNo) == False):
                            errorOccurred=True;
                    else:
                        if(token.createToken(wordBreaker.strip(), lineNo)==False):
                            errorOccurred=True

                    word = ""
                # if the current character ain't a word breaker then keep on appending to the word
                else:
                    word += fileLine[i]
                i += 1

            # if a word breaker hasn't appeared and line has ended
            if (word):
                if(token.createToken(word.strip(), lineNo)==False):
                    errorOccurred=True   
            lineNo += 1
            _length += 1


analyser = LexicalAnalyser()
#the last tokens to specify, no further tokens will be coming up
token.addToken(lineNo, '$', '$')
if not errorOccurred: 
  print('Lexical Phase Passed!')
  token.printTokens()
  tokenX = token.getTokens()
#   taaoken.printTokens()
  parser.setTokens(tokenX)
  if print(parser.ParseInp()):
      print('Syntax Phase Passed!')
      print('Semantic Phase Passed!')
      print('Compiled Successfully')
      


   
