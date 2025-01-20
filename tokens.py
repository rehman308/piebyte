import re
tokens = []
errorOccurred = False
class Token:
    
    def addToken(self,lineNo,classPart,valuePart):
        tokens.append({"Line No": lineNo, "Class Part":classPart, "Value Part":valuePart});

    
    def printTokens(self):
        for val in tokens:
         print(val["Line No"],val["Class Part"],val["Value Part"])
         
    def getTokens(self):
     return tokens
    def createToken(self, word, lineNo):
        valid_identifier = r'^[_a-zA-Z][_a-zA-Z0-9]*$'
        DATATYPE = ['number','word','flag']
        PUNCTUATOR = ['(', '{', '[', ')', '}', ']', '.', ',', ':', ';', '`']
        RO = ['>=', '<=', 'equals', '!=']
        AO = ['+=', '-=', '*=', '/=']
        INCDEC = ['++', '--']
        ADDSUB = ['+', '-']
        DIVMOD = ['/', '%']
        MUL = ['*']
        KEYWORDS = ['when','else' , 'elsewhen','equals','match','for','default','from','till','by','until','greater','task','pass','set','to','or','and','not','list']
        if word in DATATYPE:
            self.addToken(lineNo, 'DT', word)
        elif word in PUNCTUATOR:
            self.addToken(lineNo, word, word)
        elif word in INCDEC:
            self.addToken(lineNo, 'INCDEC', word)
        elif word in AO:
            self.addToken(lineNo, 'AO', word)
        elif word in ADDSUB:
            self.addToken(lineNo, 'ADDSUB', word)
        elif word in DIVMOD:
            self.addToken(lineNo, 'DIVMOD', word)
        elif word in MUL:
            self.addToken(lineNo, 'MUL', word)
        elif word in RO:
            self.addToken(lineNo, 'RO', word)
    
        elif word == 'and':
            self.addToken(lineNo,'and',word)
        elif word == 'or':
            self.addToken(lineNo,'or',word)
        elif word == 'not':
            self.addToken(lineNo,'not',word)
        elif word == 'set':
            self.addToken(lineNo, 'set', word)
        elif word == 'to':
            self.addToken(lineNo, 'to', word)
        elif word == 'list':
            self.addToken(lineNo, 'list', word)
        elif word == 'from':
            self.addToken(lineNo, 'from', word)
        elif word == 'till':
            self.addToken(lineNo, 'till', word)
        elif word == 'until':
            self.addToken(lineNo, 'until', word)
        elif word == 'match':
            self.addToken(lineNo, 'match', word)
        elif word == 'for':
            self.addToken(lineNo, 'for', word)
        elif word == 'default':
            self.addToken(lineNo, 'default', word)
        elif word == 'when':
            self.addToken(lineNo, 'when', word)
        elif word == 'else':
            self.addToken(lineNo, 'else', word)
        elif word == 'elsewhen':
            self.addToken(lineNo, 'elsewhen', word)
        elif word == 'task':
            self.addToken(lineNo, 'task', word)
        elif word == 'pass':
            self.addToken(lineNo, 'pass', word)
        elif re.match(valid_identifier,word):
            self.addToken(lineNo, 'ID', word)
        elif word in KEYWORDS:
            self.addToken(lineNo, 'KW', word)
        elif self.isValidConstant(word, lineNo) != 'Error':
            self.addToken(lineNo, self.isValidConstant(word, lineNo), word)
        elif word == ' ' or len(word)<=1:
            return
        else:
             print(f'Invalid identifier {word} @ line no {lineNo}')
             return False

    def isValidConstant(self, word, lineNo):
        int_const = r'^[+-]?\d+$'
        float_const = r'^[+-]?(\d+\.\d+|\.\d+|\d+)$'
        char_const = r"^'(\\.|[^\\'])'$"
        string_const = r'^\"(.*(?<!\\))\"$'
        if re.match(int_const, word):
            return 'int_const'
        elif re.match(float_const, word):
            return 'float_const'
        elif re.match(char_const, word):
            return 'char_const'
        elif (re.match(string_const, word)):
            return 'string_const'
        else:
            return 'Error'
