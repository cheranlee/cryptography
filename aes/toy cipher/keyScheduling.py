def keySchedule(nextCipherKey, cipherKey, roundConstant, SBox, listRoundKeys, rkeyno): 
    
    # Declare Column of set 1  
    c0 = cipherKey[0:4]
    c1 = cipherKey[4:8]
    c2 = cipherKey[8:12]
    c3 = cipherKey[12:16]
    originalColumns = [c0, c1, c2, c3]
    
    
    # Declare next set  
    c4templist = []
    c4temp = 0 
    tempxor = 0 
    nextCipherKey = ""
    count = 3 
    
    for b in range(4):     # b represents that there should be 4 columns in 1 key 
        
        # for column 4 (first column of new key)
        if b == 0: 
            
            # RotateRow
            c3 = c3[1:] + c3[:1] 

            # SubBytes 
            for i in c3: 
                x = int(i, 16) 
                c4templist.append(SBox[x])
                
            #XOR with roundconstant 
            cxor = c4templist[0] ^ roundConstant[rkeyno]
            c4templist.insert(0,cxor)
            del c4templist[1]
            
            # XOR c4temp with c0 
            for a in c4templist: 
                c4temp += a * (16 ** count)  
                count -= 1

            # Final c4
            tempxor1 = c4temp ^ int(c0, 16)
            tempxor = hex(tempxor1)[2:]
            if len(tempxor) < 4: 
                N = 4 - len(tempxor)
                tempxor = tempxor.zfill(N + len(tempxor))
            nextCipherKey += str(tempxor)
            print('c0: ', nextCipherKey)
            nextColumn = tempxor1
            print('c0val: ', nextColumn)
        
        # XOR for all columns -- columns 5, 6, 7
        else: 
            print('originalColumns: ', originalColumns[b])
            nextColumn = nextColumn ^ int(originalColumns[b],16)
            partCipherKey = hex(nextColumn)[2:]
            print('val: ', nextColumn)
            print('valstr: ', partCipherKey)
            if len(partCipherKey) < 4: 
                N = 4 - len(partCipherKey)
                partCipherKey = partCipherKey.zfill(N + len(partCipherKey))
            nextCipherKey += partCipherKey 
        
    # add to list
    listRoundKeys.append(nextCipherKey)   
    

# Declare stuff 
cipherKey = str(input('Enter cipher key: '))
roundConstant = [0x1, 0x2, 0x4, 0x8, 0x3, 0x6, 0xC, 0xB, 0x5, 0xA]
SBox = [0xE, 0x4, 0xB, 0x2, 0x3, 0x8, 0x0, 0x9, 0x1, 0xA, 0x7, 0xF, 0x6, 0xC, 0x5, 0xD]
listRoundKeys = [] 

# round key 0  
rkeyno = 0 
listRoundKeys.append(cipherKey) 

# declare rkeyno (round key number) here 
while rkeyno < 10: 
    keySchedule("", cipherKey, roundConstant, SBox, listRoundKeys, rkeyno)
    cipherKey = listRoundKeys[rkeyno+1]
    rkeyno += 1 