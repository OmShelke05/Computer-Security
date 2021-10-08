from pydoc import plain

def primeCheck(a):
    if(a==2):
        return True
    elif((a<2) or ((a%2)==0)):
        return False
    elif(a>2):
        for i in range(2,a):
            if not(a%i):
                return False
    return True

def calculateMod(p,q):
    #RSA Modulus
    n = p * q
    print("RSA Modulus(n):",n)
    return n
    
def calculateTotient(p,q):
    #Eulers Toitent
    r= (p-1)*(q-1)
    print("Eulers Toitent(r):",r)
    print("----------------------------------------------\n")
    return r

#GCD
def egcd(e,r):
    while(r!=0):
        e,r=r,e%r
    return e

def calculateE(r):
    #e Value Calculation
    for i in range(2,r):
        if(egcd(i,r)==1):
            e=i
            break
    print("The value of e is:",e)
    return e


#Multiplicative Inverse
def mult_inv(a,b):
    def xgcd(x, y):
        s1, s0 = 0, 1
        t1, t0 = 1, 0
        while y:
            b = x // y
            x, y = y, x % y
            s1, s0 = s0 - b * s1, s1
            t1, t0 = t0 - b * t1, t1
        return x, s0, t0      
 
    s, t = xgcd(a, b)[0:2]
    assert s == 1
    if t < 0:
        t += b
    
    print("The value of d is:",t)
    print("----------------------------------------------\n")
    return t

    
def encrypt(pub_key,n_text):
    e,n=pub_key
    x=[]
    m=0
    for i in n_text:
        if(i.isupper()):
            m = ord(i)-65
            c=(m**e)%n
            x.append(c)
        elif(i.islower()):               
            m= ord(i)-97
            c=(m**e)%n
            x.append(c)
        elif(i.isspace()):
            #spc=400
            x.append(400)
    return x    

def decrypt(priv_key,c_text):
    d,n=priv_key
    txt=c_text.split(', ')
    x=''
    m=0
    for i in txt:
        if(i=='400'):
            x+=' '
        else:
            m=(int(i)**d)%n
            m+=65
            c=chr(m)
            x+=c
    return x


def encryptMessage(originalFileReference):
    msg=originalFileReference.read()
    cipherText=encrypt(public,msg)
    print("Your encrypted message is: ",cipherText)
    
    #Writing to the file
    encryptedFileReference=open('encryptedFile.txt','w')
    encryptedFileReference.write(str(cipherText)[1:-1])
    encryptedFileReference.close()

def decryptMessage(encryptedFileReference):
    msg=encryptedFileReference.read()
    plainText=decrypt(private,msg)
    print("Your decrypted message is:",plainText)
    
    #Writing to the file
    decryptedFileReference=open('decryptedFile.txt','w')
    decryptedFileReference.write(plainText)
    encryptedFileReference.close()
    

print("-------------------Welcome to RSA----------------------")

#Input Prime Numbers

print("\n..........Initialization Step..........")
p = int(input("Enter a prime number for p: "))
q = int(input("Enter a prime number for q: "))
print("----------------------------------------------\n")
check_p = primeCheck(p)
check_q = primeCheck(q)

while(((check_p==False)or(check_q==False))):
    print("\nOne of the entered number is not prime. Please try again!")
    print("----------------------------------------------\n")
    p = int(input("Enter a prime number for p: "))
    q = int(input("Enter a prime number for q: "))
    check_p = primeCheck(p)
    check_q = primeCheck(q)

n=calculateMod(p,q)
r=calculateTotient(p,q)
e=calculateE(r)
d = mult_inv(e,r)

public = (e,n)
private = (d,n)
print("Private Key is:",private)
print("Public Key is:",public)
print("----------------------------------------------\n")

file_reference=open('key.txt','w')
file_reference.write("Public Key: "+str(public)+"\nPrivate Key: "+str(private))
file_reference.close()


while("True"):
    print("----------------------------------------------\n1. Encryption")
    print("2. Decryption")
    print("3. Exit")
    print("Enter choice ::: ")
    value=int(input())
    print("\nEntered choice is ::: "+str(value))
    
    if(value==1):
        originalFileReference=open('originalFile.txt','r')
        originalFileReference.seek(0)
        encryptMessage(originalFileReference)
        originalFileReference.close()
        
        
    elif(value==2):
        encryptedFileReference=open('encryptedFile.txt','r')
        encryptedFileReference.seek(0)
        decryptMessage(encryptedFileReference)
        encryptedFileReference.close()
        
    elif(value==3):
        print("Exiting.....")    
        break
    
    else:
        print("Invalid choice entered. Please enter again.")  
