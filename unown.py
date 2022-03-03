import time
import random

# Determine how many of each letter exist per shPID
# Use that to determine how many exist for all ShTID

def num_to_letter(num):
    if num == 26:
        return'!'
    elif num == 27:
        return '?'
    return chr(num + 97)

def number_exist_per_letter():
    ''' Returns a list of how many Unown exist per letter'''
    lst = [0 for _ in range(0,28)]
    f = open("UnownLetters.txt", "a")
    for PID in range(0, 4_294_967_296):
        letter = pid_to_letter(PID)
        lst[letter] += 1
        #f.write(num_to_letter(letter) + "\n")
        if PID % 100000 == 0:
            print(PID)
    f.close()
    return lst

def get_unown_per_letter():
    results = number_exist_per_letter()
    f = open("UnownPerLetter.txt", "a")
    for i in range(0, len(results)):
        f.write(num_to_letter(i) + ": " + str(results[i])+"\n")
    f.close()
    print("DONE")    


def gen_letter_per_ShPID():
    ''' Used to generate a list of the letter spreads for each ShPID '''
    lst = []
    for i in range(0,65536):
        lst.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, i])
    for PID in range(0, 4_294_967_296):
        PID1 = int(PID/65536)
        PID2 = PID % 65536
        letter = pid_to_letter(PID)
        ShPID = PID1 ^ PID2
        lst[ShPID][letter] += 1
        if PID % 10000 == 0:
            print(PID)
    return lst

def pid_to_letter(rnd):
    return (((rnd&0x03000000)>>18)|((rnd&0x030000)>>12)|((rnd&0x0300)>>6)|(rnd&0x03))%28
    
def get_ShPID_results():
    results = gen_letter_per_ShPID()
    f = open("ShPID.txt", "a")
    for result in results:
        f.write(str(result)+"\n")
    f.close()
    print("DONE")

def read_ShPID_results():
    f = open("ShPID.txt", "r")
    lines = f.readlines()
    # Strips the newline character
    lines_stripped = []
    for line in lines:
        curr = list(line.strip().strip('][').split(', '))
        curr = [ int(x) for x in curr]
        lines_stripped.append(curr)
    return lines_stripped

def test_ShTID_vs_ShPID():
    ShPID_natures = read_ShPID_results()
    letter_by_ShTID = []
    # Get results for each ShTID
    for ShTID in range(0, 65_536):
        letter_by_ShTID.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ShTID])
        for ShPID in range(0, 65_536):
            if is_shiny(ShTID, ShPID):
                curr = letter_by_ShTID[ShTID]
                for i in range(0, 28):
                    curr[i] += ShPID_natures[ShPID][i]
                letter_by_ShTID[ShTID] = curr
        print(curr)
    return letter_by_ShTID

def get_ShTID_vs_results():
    results = test_ShTID_vs_ShPID()
    f = open("ShTID.txt", "a")
    for result in results:
        f.write(str(result)+"\n")
    f.close()
    print("DONE")

def is_shiny(ShTID, ShPID):
    return (ShTID ^ ShPID) < 8

def total_per_letter():
    results = read_ShPID_results()
    lst = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 29]
    print(len(results[0]))
    for x in range(0,65536):
        for i in range(0,28):
            lst[i] += results[x][i]
    print(lst)

def read_ShTID_results():
    f = open("ShTID.txt", "r")
    lines = f.readlines()
    # Strips the newline character
    lines_stripped = []
    for line in lines:
        curr = list(line.strip().strip('][').split(', '))
        curr = [ int(x) for x in curr]
        lines_stripped.append(curr)
    return lines_stripped

def group_ShTID_by_odds():
    sset = {}
    ShTIDs = read_ShTID_results()
    for result in ShTIDs:
        curr = str(result[:-1])
        try:
            sset[curr].append(result[-1])
        except:
            sset[curr] = []
            sset[curr].append(result[-1])
    return sset

def get_ShTID_grouped():
    results = group_ShTID_by_odds()
    f = open("ShTID_Grouped.txt", "a")
    for result in results:
        f.write(str(result)+": " + str(len(results[result])) + "\n")
    f.close()
    print("DONE")

def hex_to_int(hexa):
    return int('0x' + hexa, base=16)

def lettertest(hexa):
    return num_to_letter((pid_to_letter(hex_to_int(hexa))))


def UTID_test():
    '''Runs through each of the possible UIDs, returns
    how many UIDs exist for each letter that result in 
    UID(bits12) xor UID(bits56) xor ShinyTID(56) = 0
    '''
    # Define Lists
    lst = [[0 for _ in range(28)] for _ in range(4)]
    # Search Through All UIDs
    for UID in range(256):
        letter = UID % 28
        # Get Needed UID bits
        UIDbits1 = (UID >> 6 & int('0b11', 2))
        UIDbits2 = (UID >> 2 & int('0b11', 2))
        # XOR operations = 0 when both operands are equal
        # Add one to the list in slot where current UID is shiny eligible 
        lst[UIDbits1 ^ UIDbits2][letter] += 1
    return lst

def random_PID(num):
    num = int(input())
    for _ in range(0, num):
        time.sleep(0.3)
        rand = random.randint(0, (2**32))
        binary = str(bin(rand)[2:])
        binary = "0"*(32-len(binary)) + binary
        letter = num_to_letter((pid_to_letter(rand)))
        UID = str(int(('0b' + binary[6:8] + binary[14:16] + binary[22:24] + binary[30:]), 2))
        UID = "0"*(3-len(UID)) + UID
        print(" PID: " + binary + ", UID: " + str(UID) + ", Letter: " + letter.upper())
        
        
def all_UID():
    for rand in range(200, 256):
        time.sleep(0.3)
        binary = str(bin(rand)[2:])
        binary = "0"*(8-len(binary)) + binary
        letter = num_to_letter(rand%28)
        print(" UID: " + binary + ", UID in Decimal: " + "0"*(3-len(str(rand))) + str(rand) + ", UID % 28: " + "0"*(3-len(str(rand%28))) + str(rand%28) + ", Letter: " + letter.upper()) 

if __name__ == "__main__":
    all_UID()
    pass