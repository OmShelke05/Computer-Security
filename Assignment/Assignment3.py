import random

p1 = "#include <stdio.h> main(int argc, char **argv){if (argc!=3) {exit(0);}}"
p2 = "509 2 521 3 5 1873 7 17 4831 23 157 29 37 109 313 11 653 2099 2887 5521"
p3 = "CS574 midterm will have around 10 short questions and 5 long questions'"
p4 = "I tried so hard and got so far. But in the end, it doesn't even matter."

print("plaintext length >>> " + str(len(p2)))

# lambda functions
toBin = lambda x: "".join("{0:08b}".format(int(c, 16)) for c in
                          x)  # turn a list of hex strings to a binary string ['23','25'...] => "00100011..."
xor = lambda x, y: ''.join([str(int(x[i]) ^ int(y[i])) for i in range(len(x))])  # xor of two binary strings

otp1 = ''.join([str(random.randint(0, 1)) for _ in range(len(p1) * 8)])
print("OTP1 >>> " + otp1)
otp2 = ''.join([str(random.randint(0, 1)) for _ in range(len(p1) * 8)])
print("OTP2 >>> " + otp2)

p1_ascii = [str(hex(ord(char))[2:]) for char in p1]
p2_ascii = [str(hex(ord(char))[2:]) for char in p2]
p3_ascii = [str(hex(ord(char))[2:]) for char in p3]
p4_ascii = [str(hex(ord(char))[2:]) for char in p4]

print("p1_ascii >>> ", p1_ascii)
# print("p2_ascii >>> ", p2_ascii)
# print("p3_ascii >>> ", p3_ascii)
# print("p4_ascii >>> ", p4_ascii)

print("p1_bin    >>> " + toBin(p1_ascii))
# print("p2_bin_ascii >>> " + toBin(p2_ascii))
# print("p3_bin_ascii >>> " + toBin(p3_ascii))
# print("p4_bin_ascii >>> " + toBin(p4_ascii))
# print("plaintext bin length >>> " + str(len(toBin(p1_ascii))))

p1_cipher = xor(toBin(p1_ascii), otp1)
p3_cipher = xor(toBin(p3_ascii), otp1)
p2_cipher = xor(toBin(p2_ascii), otp2)
p4_cipher = xor(toBin(p4_ascii), otp2)

print("p1_cipher >>> " + p1_cipher)
print("p2_cipher >>> " + p2_cipher)
print("p3_cipher >>> " + p3_cipher)
print("p4_cipher >>> " + p4_cipher)

# convert binary to hex
def hex2bin(ciphertext):  # turn "23 24 ... " => ["23", "24", ...] => "00100011..."
    hex_eachChar = ciphertext.split(' ')  # get rid of space
    res = ''
    for eachChar in hex_eachChar:  # 'D7'
        binString = toBin(eachChar)
        # print(eachChar + ' >>> ' + binString)
        res += binString
    print('res >>> ' + res)
    return res


def extractLeadingBits(binCipher, idx1, idx2):
    # plaintext byte in ASCII starts with 0: 01010100 01101000
    # a fixed pad                          : 1xxxxxxx 0xxxxxxx
    # xor result preserves the leading bit : 1xxxxxxx 0xxxxxxx
    # the leading bits in ciphertexts are the same, xor them we will get 0
    leadingBits = xor(binCipher[idx1], binCipher[idx2])[0::8]
    print(str(idx1) + " xor " + str(idx2) + "\'s Leadingbits >>> " + leadingBits)
    if set(leadingBits) == {'0'}:
        return True
    else:
        return False


def findPair(binCipher):  # take a list of ciphers in the form of binary string
    pair_list = []
    print(">>>>>> Start finding pairs...")
    for i in range(len(binCipher)):
        for j in range(i + 1, len(binCipher)):
            if extractLeadingBits(binCipher, i, j):
                pair_list.append([i, j])
                print("*** " + str(i) + " and " + str(j) + " are padded with the same key ***")
    print(">>>>>> Finished pairing!")
    return pair_list


def decrypt(binCipher1, binCipher2):
    # (M1 xor otp) xor (M2 xor otp) = M1 xor M2 = C1 xor C2
    xor_result = xor(binCipher1, binCipher2)
    guessingWord = input("Please tell me a guess:")
    print("Length of input >>> " + str(len(guessingWord)))

    hex_guessingWord = [str(hex(ord(char))[2:]) for char in guessingWord]
    print("Hex ASCII list of input >>> ", hex_guessingWord)

    for i in range(0, len(xor_result) - len(guessingWord) * 8 + 8, 8):
        flag = True
        # starting from position i
        possible_bin = xor(toBin(hex_guessingWord), xor_result[i: i + len(guessingWord) * 8])
        # print("Binary String of the possible word >>> " + possible_bin)
        charString = ""
        for j in range(0, len(possible_bin), 8):
            v = int(possible_bin[j:j + 8], 2)  # int value of the 8 bits
            if v > 127 or v <= 31:
                # print("Position " + str(i) + ": Impossible ASCII decoding...")
                flag = False
                break
            else:
                charString += str(chr(v))
        if flag:
            print(("Position " + str(i // 8) + " to " + str(i // 8 + len(guessingWord)) + ": Possible word >>> " + charString))


binCipher = [p1_cipher, p2_cipher, p3_cipher, p4_cipher]
pair_list = findPair(binCipher)
print("Pairing result >>> ", pair_list)
decrypt(binCipher[1], binCipher[3])
