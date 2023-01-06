# import from KeySchedule Module 
from keyScheduling import * 
print(listRoundKeys)
print(cipherKey)

def addRoundKey(listRoundKeys, cipherKey, roundno, cipherText): 
    xor = int(listRoundKeys[roundno], 16) ^ int(cipherKey, 16)
    cipherText = hex(xor)[2:]
    return cipherText

def subBytes(SBox, cipherKey, subCipherKey): 
    for i in cipherKey: 
        j = int(i, 16)
        subCipherKey += hex(SBox[j])[2:]
    return subCipherKey
        
def shiftRow(subCipherKey, shiftCipherKey): 
    shiftCipherKey += subCipherKey[0] + subCipherKey[5] + subCipherKey[10] + subCipherKey[15]   # first four 
    shiftCipherKey += subCipherKey[4] + subCipherKey[9] + subCipherKey[14] + subCipherKey[3]    # second four 
    shiftCipherKey += subCipherKey[8] + subCipherKey[13] + subCipherKey[2] + subCipherKey[7]    # third four
    shiftCipherKey += subCipherKey[12] + subCipherKey[1] + subCipherKey[6] + subCipherKey[11]   # fourth four
    return shiftCipherKey

def mixColumns(shiftCipherKey, mixList): 
    mixColumnMatrix = [0x2, 0x3, 0x1, 0x1, 0x1, 0x2, 0x3, 0x1, 0x1, 0x1, 0x2, 0x3, 0x3, 0x1, 0x1, 0x2]
    for i in range(4): 
        for j in range(4): 
            for k in range(4): 
                mixI = j * 4 + k    
                shiftI = i * 4 + k      
                
                quotient1 = mixColumnMatrix[mixI] // 2 
                remainder1 = mixColumnMatrix[mixI] % 2 
                tempShift = int(shiftCipherKey[shiftI], 16) << quotient1
                if remainder1 == 1 and quotient1 != 0: 
                    tempShift = tempShift ^ int(shiftCipherKey[shiftI], 16) 
                if tempShift > 15: 
                    tempShift = tempShift ^ 0x13
                 
                if k == 0: 
                    mixListValue = tempShift 
                else: 
                    mixListValue = mixListValue ^ tempShift 
                    tempShift = 0 
            mixListValueString = hex(mixListValue)[2:]
            mixList.append(mixListValueString)
    return mixList

def listToString(list1, mixString): 
    for i in list1: 
        mixString += i 
    return mixString
            
# Declare variables 
SBox = [0xE, 0x4, 0xB, 0x2, 0x3, 0x8, 0x0, 0x9, 0x1, 0xA, 0x7, 0xF, 0x6, 0xC, 0x5, 0xD]
cipherTextList = [] 
pt = str(input("Enter plaintext: "))

# round 0 
roundno = 0 
addKey = addRoundKey(listRoundKeys, pt, 0, '')
if len(addKey) < 16: 
    N = 16 - len(addKey)
    addKey = addKey.zfill(N + len(addKey))
print("addKey: ", addKey)

# round 1-9 (inclusive of 1 and 9)
for i in range(1, 10): 
    sub = subBytes(SBox, addKey, '')
    print("Sub: ", sub)
    shift = shiftRow(sub, '')
    print("Shift: ", shift)
    mix = mixColumns(shift, [])
    print("Mix: ", mix)
    mixListToString = listToString(mix, '')
    print("MixString: ", mixListToString)
    cipherTextList.append(mixListToString)
    addKey = addRoundKey(listRoundKeys, mixListToString, i, '')
    if len(addKey) < 16: 
        N = 16 - len(addKey)
        addKey = addKey.zfill(N + len(addKey))
    print("Add: ", addKey)
    
# round 10 
sub = subBytes(SBox, addKey, '')
shift = shiftRow(sub, '')
addKey = addRoundKey(listRoundKeys, shift, 10, '')
cipherTextList.append(addKey)

print(cipherTextList)