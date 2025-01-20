list = set([])
symbolTableStruct = {'Scope': 0, 'Value Part': "", 'Type': ""}
scope = 0
scopeStack = [0]
symbolTable = []
class SyntaxAnalyser:
    tokens = []
    i = 0
    length = 0

    def lookUPDEF(self, scope, valuePart,type):
        tempStack = []
        flag = True
        idx =0
        # print(symbolTable)
        while len(scopeStack) > 0:
            top = scopeStack[len(scopeStack)-1]
            tempStack.append(top)
            scopeStack.pop()
            for value in symbolTable:
                if  value['Value Part'] == valuePart:
                    flag = False
                    break
                if flag == False:
                 break

        while len(tempStack) > 0:
             top = tempStack[idx]
             scopeStack.append(top)
             tempStack.pop()
             idx += 1

        if flag == True:
             val = dict()
             val['Scope'] = scope
             val['Value Part'] = valuePart
             val['Type'] = type
             symbolTable.append(val)
             return True

        list.add(valuePart + ' already defined in scope '+str(scope))
        return False

        def lookUPUSE(self,scope,valuePart,type):
         tempStack = []
         flag = False
         idx = 0
        # print(symbolTable)
         while len(scopeStack) > 0:
            top = scopeStack[len(scopeStack)-1]
            tempStack.append(top)
            scopeStack.pop()
            for value in symbolTable:
                if value['Value Part'] == valuePart:
                    flag = True
                    break
                if flag == True:
                 break



        while len(tempStack) > 0:
            top = tempStack[idx]
            scopeStack.append(top)
            tempStack.pop()
            idx+=1
        
        if flag == True:
            val = dict()
            val['Scope']=scope
            val['Value Part'] = valuePart
            val['Type']= type
            symbolTable.append(val)
            return True

        list.add(valuePart+ ' already defined in scope '+str(scope))
        return False
            
    def setTokens(self, token):
        self.tokens = token
        self.length = len(token)

    def ParseInp(self):
        global list
        if self.START():
            return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))
        print(list)
        return False

    def START(self):
        global list
        if self.tokens[self.i]['Class Part']== '$':
            return True
        # print(self.tokens[self.i]['Class Part'])
        if self.MLS():
            if self.START():
                return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No'])) 
        return False
    def DECL(self):
        type = ""
        name = ""
        temp = self.tokens
        if temp[self.i]['Class Part'] == 'DT':
               #  print('here')
                type = temp[self.i]['Value Part']
                self.i += 1
                if temp[self.i]['Class Part'] == 'ID':
                    name = temp[self.i]['Value Part']
                    if self.lookUPDEF(scope,name,type):
                     self.i += 1
                     if temp[self.i]['Class Part'] == ',':
                        if self.LIST(temp):
                            return True
                     else:
                        if self.lookUPDEF(scope,name,type):
                         return True    
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))  
        return False

    def INIT(self):
        # print(self.tokens[self.i]['Class Part'] )
        if self.tokens[self.i]['Class Part'] == 'set':
            self.i += 1
            if self.initA():
                return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']) ) 
         
        return False

    def initA(self):
        temp = self.tokens
        type=""
        name=""
        if (temp[self.i]['Class Part'] == 'DT') or (temp[self.i]['Class Part'] == 'ID') or (temp[self.i]['Class Part'] == 'list'):
            #decl + init (var)
            if temp[self.i]['Class Part'] == 'DT':
                type = temp[self.i]['Value Part']
                self.i += 1
                if temp[self.i]['Class Part'] == 'ID':
                    if self.lookUPDEF(scope,name,type):
                     self.i += 1
                     if temp[self.i]['Class Part'] == ',':
                      if self.LIST(type):
                        if temp[self.i]['Class Part'] == 'to':
                            self.i += 1
                            if self.EXPRESSION():
                                return True
                     else:
                        if temp[self.i]['Class Part'] == 'to':
                            self.i += 1
                            if self.EXPRESSION():
                                return True



                            # init (list + var)
            elif temp[self.i]['Class Part'] == 'ID':
                name = temp[self.i]['Value Part']
                # if self.lookUPDEF(scope, name, type):
                self.i += 1
                if temp[self.i]['Class Part'] == ',':
                  if self.LIST():
                   if temp[self.i]['Class Part'] == 'to':
                        self.i += 1
                        if self.initB(type):
                            # self.i+=1
                            return True
                else:
                    if temp[self.i]['Class Part'] == 'to':
                        self.i += 1
                        if self.initB(type):
                            # self.i+=1
                            
                            return True



                        #decl + init (list)
            elif temp[self.i]['Class Part'] == 'list':
                self.i += 1
                # print('val')
                if temp[self.i]['Class Part'] == 'ID':
                    name = temp[self.i]['Value Part']
                    # if self.lookUPDEF(scope, name, type):
                    self.i += 1
                    if temp[self.i]['Class Part'] == ',':
                      if self.LIST(temp):
                       if temp[self.i]['Class Part'] == 'to':
                        self.i += 1
                        if temp[self.i]['Class Part'] =='[':
                            self.i+=1
                            if self.oEXP():
                                if temp[self.i]['Class Part'] ==']':
                                    self.i+=1
                                    return True
                    else:
                        if temp[self.i]['Class Part'] == 'to':
                         self.i += 1
                         if temp[self.i]['Class Part'] == '[':
                            self.i += 1
                            if self.oEXP():
                                if temp[self.i]['Class Part'] == ']':
                                    self.i += 1
                                    
                                    return True
        
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False

    def initB(self,type):
        if self.tokens[self.i]['Class Part'] =='$':
         return True
        if self.tokens[self.i]['Class Part'] == '[':
            self.i+=1
            if self.oEXP():
                if self.tokens[self.i]['Class Part'] == ']':
                    self.i+=1
                    return True
        if self.EXPRESSION():
            return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))  
        return False

    def oEXP(self):
        if self.tokens[self.i]['Class Part'] == ']':
            return True
        if self.EXPRESSION() and self.oEXP_A() :
            return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    def oEXP_A(self):
        if self.tokens[self.i]['Class Part'] == ']' or self.tokens[self.i]['Class Part'] == '$':
            return True
        if self.tokens[self.i]['Class Part'] == ',':
            self.i+=1
            if self.EXPRESSION():
                if self.oEXP_A():
                 return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
            
    def LIST(self,type):
        temp = self.tokens
        if temp[self.i]['Class Part'] == '$' or temp[self.i]['Class Part'] == 'to' or temp[self.i]['Class Part'] == 'set' or temp[self.i]['Class Part'] == 'when':
            return True
        if temp[self.i]['Class Part'] == ',':
            self.i += 1
            if (temp[self.i]['Class Part'] == 'ID'):
                name = temp[self.i]['Value Part']
                if self.lookUPDEF(scope,name,type):
                 self.i += 1
                if self.LIST(type):
                    return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    


    #EXPRESSION CFG
    def EXPRESSION(self):
        # print('exp1',self.tokens[self.i]['Class Part'])
        if self.T() and self.Edash():
            # print(self.tokens[self.i]['Class Part'],'true')
            return True
        # print('exp2', self.tokens[self.i]['Class Part'])

        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    
    def Edash(self):
        if self.tokens[self.i]['Class Part'] == '$' or self.tokens[self.i]['Class Part'] == ']' or self.tokens[self.i]['Class Part'] == ',' or self.tokens[self.i]['Class Part'] == '{' or self.tokens[self.i]['Class Part'] == 'till' or self.tokens[self.i]['Class Part'] == 'RO' or  self.tokens[self.i]['Class Part'] == '}' or self.tokens[self.i]['Class Part'] == 'from'  or self.tokens[self.i]['Class Part'] == 'when' or self.tokens[self.i]['Class Part'] == 'match' or self.tokens[self.i]['Class Part'] == 'until' or self.tokens[self.i]['Class Part'] == 'set' or self.tokens[self.i]['Class Part'] == 'ID' or self.tokens[self.i]['Class Part'] == 'DT' or self.tokens[self.i]['Class Part'] == 'task':
            return True
        if self.tokens[self.i]['Class Part'] == 'ADDSUB':
           self.i+=1
           if self.T() and self.Edash():
               return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    def T(self):
        if self.F() and self.Tdash():
            return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    def Tdash(self):
        if self.tokens[self.i]['Class Part'] == '$' or self.tokens[self.i]['Class Part'] == 'ADDSUB' or self.tokens[self.i]['Class Part'] == ']' or self.tokens[self.i]['Class Part'] == ',' or self.tokens[self.i]['Class Part'] == '{' or self.tokens[self.i]['Class Part'] == 'till' or self.tokens[self.i]['Class Part'] == 'RO' or self.tokens[self.i]['Class Part'] == '}' or self.tokens[self.i]['Class Part'] == 'from' or self.tokens[self.i]['Class Part'] == 'when' or self.tokens[self.i]['Class Part'] == 'match' or self.tokens[self.i]['Class Part'] == 'until' or self.tokens[self.i]['Class Part'] == 'set' or self.tokens[self.i]['Class Part'] == 'ID' or self.tokens[self.i]['Class Part'] == 'task' or self.tokens[self.i]['Class Part'] == 'DT':
             return True
        if self.tokens[self.i]['Class Part'] == 'DIVMOD' or self.tokens[self.i]['Class Part'] == 'MUL':
           self.i += 1
           if self.F() and self.Tdash():
               return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))  
        return False
    def F(self):
        temp = self.tokens
        if 'const' in temp[self.i]['Class Part']:
            self.i+=1
            return True
        elif temp[self.i]['Class Part'] == 'ID':
            self.i+=1
            if self.INC():
                return True
        elif temp[self.i]['Class Part'] == 'INCDEC':
            self.i+=1
            if temp[self.i]['Class Part'] == 'ID':
                self.i+=1
                return True
        elif temp[self.i]['Class Part'] == 'not':
            self.i+=1
            if temp[self.i]['Class Part'] =='ID':
                self.i+=1
                return True

        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    def INC(self):
        if self.tokens[self.i]['Class Part'] == 'DIVMOD' or self.tokens[self.i]['Class Part'] == 'ADDSUB' or self.tokens[self.i]['Class Part'] == 'MUL' or self.tokens[self.i]['Class Part'] == '$' or self.tokens[self.i]['Class Part'] == ']' or self.tokens[self.i]['Class Part'] == ',' or self.tokens[self.i]['Class Part'] == '{' or self.tokens[self.i]['Class Part'] == 'till' or self.tokens[self.i]['Class Part'] == 'RO' or self.tokens[self.i]['Class Part'] == '}' or self.tokens[self.i]['Class Part'] == 'from' or self.tokens[self.i]['Class Part'] == 'when' or self.tokens[self.i]['Class Part'] == 'match' or self.tokens[self.i]['Class Part'] == 'until' or self.tokens[self.i]['Class Part'] == 'set' or self.tokens[self.i]['Class Part'] == 'ID' or self.tokens[self.i]['Class Part'] == 'task' or self.tokens[self.i]['Class Part'] == 'DT':
            return True
            
        if self.tokens[self.i]['Class Part'] == 'INCDEC':
            self.i+=1
            return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False

#from till loop
    def FROM_TILL(self):
        # print(self.tokens[self.i]['Class Part'])
        if self.tokens[self.i]['Class Part'] == 'from':

            self.i+=1
            if self.EXPRESSION():
                if self.tokens[self.i]['Class Part'] == 'till':
                    self.i+=1
                    if self.EXPRESSION(): 
                     if self.BY():
                        if self.tokens[self.i]['Class Part'] =='{':
                            # print(self.tokens[self.i]['Class Part'],self.tokens[self.i]['Line No'])
                            scope += 1
                            self.i+=1
                            # print(self.tokens[self.i]['Class Part'],self.tokens[self.i]['Line No'])
                            if self.MLS():
                                
                               if self.tokens[self.i]['Class Part'] == '}':
                                   scope -= 1
                                   self.i+=1
                                   return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False

    def BY(self):
        if self.tokens[self.i]['Class Part'] == '{' :
            
            return True
        if self.EXPRESSION():
            return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False 
    
    def MLS(self):

        if self.tokens[self.i]['Class Part'] == '}' or self.tokens[self.i]['Class Part'] == '$':
            return True
        if self.tokens[self.i]['Class Part'] ==']'  :
            self.i+=1
            return True
        if self.tokens[self.i]['Class Part'] == 'DT' or self.tokens[self.i]['Class Part'] == 'list' or self.tokens[self.i]['Class Part'] == 'set' or self.tokens[self.i]['Class Part'] == 'when' or self.tokens[self.i]['Class Part'] == 'until' or self.tokens[self.i]['Class Part'] =='from' or self.tokens[self.i]['Class Part'] =='match':
            # print(self.tokens[self.i]['Class Part'])
            if self.SLS():
            #    print(self.tokens[self.i]['Class Part'])
               if self.MLS():
                   
                   return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    
    def SLS(self):
        if self.tokens[self.i]['Class Part'] == 'DT' or self.tokens[self.i]['Class Part'] == 'list':
           if self.DECL():
               return True
        elif self.tokens[self.i]['Class Part'] == 'set':
            # print(self.tokens[self.i]['Class Part'])
            if self.INIT():
                # print('here',self.tokens[self.i]['Class Part'])
                return True
        elif self.tokens[self.i]['Class Part'] == 'when':
            if self.WHEN_ELSE():
                return True
        elif self.tokens[self.i]['Class Part'] == 'from':
            if self.FROM_TILL():
                return True
        elif self.tokens[self.i]['Class Part'] == 'until':
            if self.UNTIL():
                return True
        elif self.tokens[self.i]['Class Part'] == 'match':
            if self.MATCH_FOR():
                return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    

    #until loop
    def UNTIL(self):
        if self.tokens[self.i]['Class Part'] == 'until':
            self.i+=1
            if self.COND():
                if self.tokens[self.i]['Class Part'] == '{':
                    scope+=1
                    self.i+=1
                    if self.MLS():
                        if self.tokens[self.i]['Class Part'] == '}':
                            scope -= 1
                            self.i+=1
                            return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False                 


    def COND(self):
        if self.EXPRESSION():
            if self.CONDdash():
                return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    
    def CONDdash(self):
        if self.tokens[self.i]['Class Part'] == 'RO':
            self.i+=1
            if self.EXPRESSION():
                return True
        if self.tokens[self.i]['Class Part'] == '{':
            scope+=1
            self.i+=1
            return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    
    #match-for 

    def MATCH_FOR(self):
        if self.tokens[self.i]['Class Part'] == 'match':
            self.i+=1
            if self.EXPRESSION():
                if self.tokens[self.i]['Class Part'] == '{':
                    scope+=1
                    self.i+=1
                    if self.FOR():
                        if self.DEFAULT():
                            if self.tokens[self.i]['Class Part'] == '}':
                                scope -= 1
                                self.i+=1
                                return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False

    def FOR(self):
           if self.tokens[self.i]['Class Part'] == '}' :
               return True
           if self.tokens[self.i]['Class Part'] == 'for':
               self.i+=1
               if self.EXPRESSION():
                if self.tokens[self.i]['Class Part'] == '{':
                    scope += 1
                    self.i+=1
                    if self.MLS():
                        if self.tokens[self.i]['Class Part'] == '}':
                            scope -= 1
                            self.i+=1
                            if self.FOR():
                                return True
           if self.tokens[self.i]['Class Part'] == 'default':
               if self.DEFAULT():
                return True
           list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
           return False

    def DEFAULT(self):
        if self.tokens[self.i]['Class Part'] == '}':
             return True
        if self.tokens[self.i]['Class Part'] ==  'default':
            self.i+=1 
            if self.tokens[self.i]['Class Part'] == '{':
                scope+=1
                self.i+=1
                if self.MLS():
                    if self.tokens[self.i]['Class Part'] == '}':
                        scope -= 1
                        self.i+=1
                        return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False


#when-elsewhen-else
    def WHEN_ELSE(self):
        if self.tokens[self.i]['Class Part'] == 'when':
            self.i+=1
            if self.COND():
                if self.tokens[self.i]['Class Part'] == '{':
                    scope+=1
                    self.i+=1
                    if self.MLS():
                        # print(self.tokens[self.i]['Class Part'])
                        if self.tokens[self.i]['Class Part'] == '}':
                            scope -= 1
                            self.i+=1
                            # print(self.tokens[self.i]['Class Part'])
                            if self.oELSE():
                                return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    
    def oELSE(self):
        if self.tokens[self.i]['Class Part'] == 'DT' or self.tokens[self.i]['Class Part'] == 'list' or self.tokens[self.i]['Class Part'] == 'set' or self.tokens[self.i]['Class Part'] == 'when' or self.tokens[self.i]['Class Part'] == 'until' or self.tokens[self.i]['Class Part'] == 'match' or self.tokens[self.i]['Class Part'] == 'from' or self.tokens[self.i]['Class Part'] == 'ID' or self.tokens[self.i]['Class Part'] == '{' or self.tokens[self.i]['Class Part'] == 'INCDEC' or self.tokens[self.i]['Class Part'] == 'not' or 'const' in self.tokens[self.i]['Class Part'] or self.tokens[self.i]['Class Part']=='$':
            return True
        if self.tokens[self.i]['Class Part'] == '}':
            scope -= 1
            self.i+=1
            return True
        if self.tokens[self.i]['Class Part'] == 'else':
            if self.ELSE(): 
                return True
        if self.tokens[self.i]['Class Part'] == 'elsewhen':
            if self.ELSEWHEN():
                return True
            
    def ELSEWHEN(self):
        if self.tokens[self.i]['Class Part'] == 'elsewhen':
            self.i+=1
            if self.COND():
                if self.tokens[self.i]['Class Part'] == '{':
                    scope+=1
                    self.i+=1
                    if self.MLS():
                        if self.tokens[self.i]['Class Part'] == '}':
                            scope -= 1
                            self.i+=1
                            if self.oELSE():
                                return True
                            
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    
    def ELSE(self):
        if self.tokens[self.i]['Class Part'] == 'else':
            self.i+=1
            if self.tokens[self.i]['Class Part'] == '{':
                scope+=1
                self.i+=1
                print(self.tokens[self.i]['Class Part'])
                if self.MLS():
                    if self.tokens[self.i]['Class Part'] == '}':
                        scope -= 1
                        self.i+=1
                        return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    
    def TASK(self):
        if self.tokens[self.i]['Class Part'] == 'task':
            self.i+=1
            if self.tokens[self.i]['Class Part'] == 'ID':
                self.i+=1
                if self.tokens[self.i]['Class Part'] == '(':
                    self.i+=1
                    if self.ARGS():
                        if self.tokens[self.i]['Class Part'] == ')':
                            self.i+=1
                            if self.oBODY():
                                return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    
    def ARGS(self):
        if self.tokens[self.i]['Class Part'] == ')':
            return True
        if self.tokens[self.i]['Class Part'] == 'DT':
            self.i+=1
            if self.tokens[self.i]['Class Part'] ==  'ID':
                self.i+=1
                if self.ARGS2():
                    return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    
    def ARGS2(self):
        if self.tokens[self.i]['Class Part'] ==')':
            return True
        if self.tokens[self.i]['Class Part'] ==',':
            self.i+=1
            if self.tokens[self.i]['Class Part'] =='DT':
                self.i+=1
                if self.tokens[self.i]['Class Part'] =='ID':
                    self.i+=1
                    if self.ARGS2():
                        return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    
    def oBODY(self):
        if self.tokens[self.i]['Class Part'] == 'DT' or self.tokens[self.i]['Class Part'] == 'list' or self.tokens[self.i]['Class Part'] == 'set' or self.tokens[self.i]['Class Part'] == 'when' or self.tokens[self.i]['Class Part'] == 'until' or self.tokens[self.i]['Class Part'] == 'match' or self.tokens[self.i]['Class Part'] == 'from' or self.tokens[self.i]['Class Part'] == 'ID' or self.tokens[self.i]['Class Part'] == 'INCDEC' or self.tokens[self.i]['Class Part'] == 'not' or 'const' in self.tokens[self.i]['Class Part']:
            return True
        if self.tokens[self.i]['Class Part'] == '{':
            scope+=1
            self.i+=1
            # print(self.tokens[self.i]['Class Part'])
            if self.MLS():
                if self.PASS():
                    if self.tokens[self.i]['Class Part'] == '}':
                        scope -= 1
                        self.i+=1
                        return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    
    def PASS(self):
        if self.tokens[self.i]['Class Part'] == '}':
            return True
        if self.tokens[self.i]['Class Part'] == 'pass':
            self.i+=1
            if self.PASSa():
                return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False
    
    def PASSa(self):
        if self.tokens[self.i]['Class Part'] == '}':
            scope -= 1
            return True
        if self.EXPRESSION():
            return True
        list.add('Syntax Error @ line' + str(self.tokens[self.i]['Line No']))   
        return False