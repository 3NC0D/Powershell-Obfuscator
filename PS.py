# version 7 - 02272019

import random, sys, math

predefined = ['home', 'profile', 'pshome', 'host', 'psversiontable']
predefined.extend(['true', 'false', 'null', '_', 'env', 'erroractionpreference'])
predefined.extend(['args', 'myinvocation', 'input', 'pwd'])
predefined.extend(['foreach', 'matches', 'lastexitcode', 'error'])

predefinedString = ['SilentlyContinue']

def isLower(ch):
    return (ch >= 'a' and ch <= 'z')

def isUpper(ch):
    return (ch >= 'A' and ch <= 'Z')

def isAlphabet(ch):
    return isLower(ch) or isUpper(ch)

def isDigit(ch):
    return ch >= '0' and ch <= '9'

def isValidVar(ch, isFunc = False):
    funcVars = '-'
    return isDigit(ch) or isAlphabet(ch) or ch == '_' or (isFunc and ch in funcVars)

def randomRename(name):
    output = list()
    for ch in name:
        if isAlphabet(ch) and random.randint(0, 2) > 0:
            if isLower(ch):
                ch = chr(ord(ch) - ord('a') + ord('A'))
            else:
                ch = chr(ord(ch) + ord('a') - ord('A'))
        output.append(ch)
    return ''.join(output)

def randomName():
    notStart = '_0987654321'
    valids = notStart + 'qwertyuioplkjhgfdsazxcvbnmQAZXSWEDCVFRTGBNHYUJMKIOLP'
    n = random.randint(6, 20)
    res = valids[random.randint(len(notStart), len(valids) - 1)]
    for _ in range(n):
        res += valids[random.randint(0, len(valids) - 1)]
    return  res

def navigateComment(inp, idx):
    ch = ' '
    if idx > 0:
        ch = inp[idx - 1]
    idx += 1
    res = '#'
    if(ch == '<'):
        while idx < len(inp) and inp[idx - 1] != '#' or inp[idx] != '>':
            res += inp[idx]
            idx += 1
        return res + '>'
    else:
        while idx < len(inp) and inp[idx] != '\n':
            res += inp[idx]
            idx += 1
        return res + '\n'

def encodeString(inp):
    if inp == '':
        return ''
    inp = inp.encode('hex')
    r = random.randint(40, 76)
    output = chr(r)
    for ch in inp:
        output += chr(int(ch, 16) + r)
    return output

def navigateString(inp, idx):
    ch = inp[idx]
    res = ''
    idx += 1
    while idx < len(inp) and inp[idx] != ch:
        res += inp[idx]
        idx += 1
    return res

def navigateVariable(inp, idx, isFunc = False):
    res = ''
    idx += 1
    while idx < len(inp) and isValidVar(inp[idx], isFunc):
        res += inp[idx]
        idx += 1
    return res

def parseTotal(inputString):
    return inputString
    # inputString = inputString.replace('\r', '').strip()
    # inputString = inputString.split('\n')
    # return inputString


def dirtyInline(inputString):
    inputString = inputString.replace('\r', '').strip()
    result = list()
    vars = dict()
    for item in predefined:
        vars[item] = item
    idx = 0
    while idx < len(inputString):
        while idx < len(inputString):
            if inputString[idx] == "'" or inputString[idx] == '"':
                temp = navigateString(inputString, idx)
                result.append(inputString[idx] + temp + inputString[idx])
                idx += len(temp) + 2
            elif inputString[idx] == '#':
                temp = navigateComment(inputString, idx)
                if result[-1].endswith('<'):
                    result[-1] = result[-1][:-1]
                while result[-1] == '' or result[-1] == ' ' or result[-1] == '\t' or result[-1] == ';':
                    result = result[:-1]
                if result[-1] != '{' and result[-1] != '}':
                    result.append(';')
                idx += len(temp)
            elif inputString[idx] == '\n':
                while result[-1] == '' or result[-1] == ' ' or result[-1] == '\t' or result[-1] == ';':
                    result = result[:-1]
                if result[-1] != '{' and result[-1] != '}':
                    result.append(';')
                idx += 1
            elif (inputString[idx] == ' ' or inputString[idx] == '\t') and (inputString[idx - 1] == ' ' or inputString[idx - 1] == '\t'):
                idx += 1
            elif (inputString[idx] == ' ' or inputString[idx] == '\t') and (result[-1] == ';' or result[-1] == '{' or result[-1] == '}'):
                idx += 1
            else:
                result.append(inputString[idx])
                idx += 1
    result = ''.join(result)
    return result.replace('}$', '};$').replace(';{', '{')

def dirtyFunction(inputString):
    vars = dict()
    idx = 0
    while idx < len(inputString):
        while idx < len(inputString):
            if inputString[idx] == "'" or inputString[idx] == '"':
                temp = navigateString(inputString, idx)
                idx += len(temp) + 2
            elif inputString[idx] == '#':
                temp = navigateComment(inputString, idx)
                idx += len(temp)
            elif inputString[idx].lower() == 'f':
                temp = navigateVariable(inputString, idx)
                temp = temp.lower()
                if temp != 'unction':
                    idx += 1
                    continue
                idx += len('function')
                temp = navigateVariable(inputString, idx, True)
                temp = temp.lower()
                if not temp in vars:
                    vars[temp] = randomName()
                idx += len(temp)
            else:
                idx += 1
    result = list()
    idx = 0
    while idx < len(inputString):
        while idx < len(inputString):
            if inputString[idx] == "'" or inputString[idx] == '"':
                temp = navigateString(inputString, idx)
                result.append(inputString[idx] + temp + inputString[idx])
                idx += len(temp) + 2
            elif inputString[idx] == '#':
                temp = navigateComment(inputString, idx)
                result.append(temp)
                idx += len(temp)
            elif inputString[idx] == '$':
                temp = navigateVariable(inputString, idx)
                result.append('$' + temp)
                idx += len(temp) + 1
            elif isAlphabet(inputString[idx]):
                temp = inputString[idx] + navigateVariable(inputString, idx)
                if temp.lower() in vars:
                    result.append(randomRename(vars[temp.lower()]))
                else:
                    result.append(temp)
                idx += len(temp)
            else:
                result.append(inputString[idx])
                idx += 1
    comment = ''
    for x, y in vars.items():
        if not x in predefined:
            comment += ('%-23s' % y) + 'was ' + x + '\n'
    comment = '<#\n' + comment + '#>\n\n'
    return comment + ''.join(result)

def dirtyVariable(inputString):
    result = list()
    vars = dict()
    for item in predefined:
        vars[item] = item
    idx = 0
    while idx < len(inputString):
        while idx < len(inputString):
            if inputString[idx] == "'" or inputString[idx] == '"':
                temp = navigateString(inputString, idx)
                result.append(inputString[idx] + temp + inputString[idx])
                idx += len(temp) + 2
            elif inputString[idx] == '#':
                temp = navigateComment(inputString, idx)
                result.append(temp)
                idx += len(temp)
            elif inputString[idx] == '$':
                temp = navigateVariable(inputString, idx)
                temp = temp.lower()
                if temp == 'true':
                    pass
                if not temp in vars:
                    vars[temp] = randomName()
                result.append('$' + randomRename(vars[temp]))
                idx += len(temp) + 1
            else:
                result.append(inputString[idx])
                idx += 1
    result = ''.join(result)
    result = dirtyFunction(result)
    comment = ''
    for x, y in vars.items():
        if not x in predefined:
            comment += '$' + ('%-23s' % y) + 'was $' + x + '\n'
    comment = '<#\n' + comment + '#>\n\n'
    return comment + result

def dirtyNumber(inputString):
    result = list()
    idx = 0
    while idx < len(inputString):
        while idx < len(inputString):
            if inputString[idx] == "'" or inputString[idx] == '"':
                temp = navigateString(inputString, idx)
                result.append(inputString[idx] + temp + inputString[idx])
                idx += len(temp) + 2
            elif inputString[idx] == '#':
                temp = navigateComment(inputString, idx)
                result.append(temp)
                idx += len(temp)
            elif not isDigit(inputString[idx]):
                result.append(inputString[idx])
                idx += 1
            elif isDigit(inputString[idx]) and isValidVar(inputString[idx - 1]):
                while idx < len(inputString) and isDigit(inputString[idx]):
                    result.append(inputString[idx])
                    idx += 1
            else:
                break
        num = ''
        while idx < len(inputString) and isDigit(inputString[idx]):
            num += inputString[idx]
            idx += 1
        if num != '':
            if random.randint(0, 2) > 0:
                num = int(num)
                r = random.randint(1, 4)
                if r == 1:
                    i = random.randint(0, 2 * num) - num
                    j = num - i
                    result.append('(' + str(i) + ' + ' + str(j) + ')')
                elif r == 2:
                    i = random.randint(num + 1, 2 * num + 1)
                    j = i - num
                    result.append('(' + str(i) + ' - ' + str(j) + ')')
                elif r == 3 and num > 2:
                    i = random.randint(2, num)
                    j = i * num
                    result.append('([int](' + str(j) + ' / ' + str(i) + '))')
                elif r == 4 and num > 3:
                    r = random.randint(2, int(math.sqrt(num)) + 1)
                    for i in range(r, 0, -1):
                        if num % i == 0:
                            j = num // i
                            result.append('(' + str(i) + ' * ' + str(j) + ')')
                            break
                else:
                    result.append(str(num))
            else:
                result.append(num)
    result = ''.join(result)
    if random.randint(0, 2) == 0:
        result = dirtyNumber(result)
    return result

def getLastWord(inputString, idx):
    base = idx
    starts = ['$', '\n', '\r']
    seps = ['=', '(']
    while idx >= 0 and not inputString[idx] in starts:
        idx -= 1
    for item in seps:
        if inputString[idx: base].find(item) > -1:
            return 1
    if inputString[idx: base].lower().startswith('$env:public'):
        return -1
    return 0

def permuteString(inputString):
    if len(inputString) < 2:
        return "'" + inputString + "'"
    l = random.randint(1, len(inputString) // 2 + 1)
    x = []
    i = 0
    while i < len(inputString):
        x.append(inputString[i: i + l])
        i += l
    y = list(x)
    random.shuffle(y)
    t = list(enumerate(y))
    t = {i: j for (j, i) in t}
    f = ''
    s = ''
    for item in x:
        f += '{' + str(t[item]) + '}'
    for item in y:
        s += "'" + item + "',"
    result = "('" + f + "'-f" + s[:-1] + ")"
    return result

def dirtyString(inputString):
    decodeFunc = '''function [funcname]{
    param($inp)
    $r = [int]$inp[0]
    $output = ''
    for($i = 1; $i -lt $inp.length; $i += 2){
        $output += [char](16 * ([int]$inp[$i] - $r) + ([int]$inp[$i + 1] - $r))
    }
    return $output
}

'''
    funcname = randomName() + randomName()
    decodeFunc = decodeFunc.replace('[funcname]', funcname)
    result = list()
    idx = 0
    while idx < len(inputString):
        if inputString[idx] == "'" or inputString[idx] == '"':
            temp = navigateString(inputString, idx)
            h = getLastWord(inputString, idx)
            if temp in predefinedString:
                rt = permuteString(temp)
            elif inputString[idx - 1] != '.' and h == 1:
                rt = '(' + randomRename(funcname) + "('" + encodeString(temp) + "'))"
            elif h == 0:
                rt = permuteString(temp)
            else:
                rt = inputString[idx] + temp + inputString[idx]
            result.append(rt)
            idx += len(temp) + 2
        elif inputString[idx] == '#':
            temp = navigateComment(inputString, idx)
            result.append(temp)
            idx += len(temp)
        else:
            result.append(inputString[idx])
            idx += 1
    result = ''.join(result)
    return decodeFunc + result

try:
    inputAddress = sys.argv[1]
except:
    inputAddress = 'we.ps1'
with open(inputAddress, 'r') as i:
    with open(inputAddress + '.ps1', 'w') as o:
        kkk = i.read()
        # kkk = parseTotal(kkk)
        kkk = dirtyString(kkk)
        kkk = dirtyInline(kkk)
        kkk = dirtyNumber(kkk)
        kkk = dirtyVariable(kkk)
        o.write(kkk)
