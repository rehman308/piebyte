import re

class Remover:

    def removeComments(self, code):
        #  print(type(code))
        code = self.removeSingleLineComments(code)
        code = self.removeMultiLineComments(code)
        return code

    def removeSingleLineComments(self, code):
      # matches single line comments
        pattern = r"(?<!!)~.*?$"

        # re.sub is used to replace the string,
        # first part, the pattern
        # second part, the replacement string, in our case we send "" so remove it
        # the string in which replacement has to occur
        code = [re.sub(pattern, "", line) for line in code]
        return code

    def removeMultiLineComments(self, code):
     new_code = []
     is_comment = False
     temp = ""
     for line in code:
      i = 0
      length = len(line)
      while i < length:
         if line[i:i+2] == '!~':
            is_comment = not is_comment
            i+=2
         elif not is_comment:
            temp += line[i]
            i+=1
         elif is_comment:
            i+=1
      if temp.strip() != "":
         new_code.append(temp)
      temp = ""
     return new_code
     

# def removeMultiLineComments(self, code):
