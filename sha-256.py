'''
sha256 algorithm

'''

# BASE CONVERSION

def bintodec(binstring):
    return(int(binstring,2))

def hextodec(hexstring):
    return(int(hexstring,16))
    
def dectohex(dec):
    return(str(format(dec,'x')))
    
def binary(dec):
    return(str(format(dec,'b')))

def binary8bit(dec):
    return(str(format(dec,'08b')))

def binary32bit(dec):
    return(str(format(dec,'032b')))

def binary64bit(dec):
    return(str(format(dec,'064b')))

#STRING FORMAT

def g2(str1):
    list1=[]
    for i in range(len(str1)):
        list1.append(str1[i])
    return(list1)

def g1(list1):
    str1=''
    for i in range(len(list1)):
        str1+=list1[i]
    return(str1)
    
def G3(a,x):
    b=[]
    c=0
    d=x
    while d<len(a)+1:
        b.append(a[c:d])
        c=d
        d+=x
    return(b)

# MATHEMATICAL OPERATORS 
    
def And(str1,str2):
    andlist=[]
    for i in range(len(str1)):
        if str1[i]=='1' and str2[i]=='1':
            andlist.append('1')
        else:
            andlist.append('0')

    return(g1(andlist))

def Or(str1,str2):
    orlist=[]
    for i in range(len(str1)):
        if str1[i]=='0' and str2[i]=='0':
            orlist.append('0')
        else:
            orlist.append('1')
    return(g1(orlist))

def Not(str1):
    notlist=[]
    for i in range(len(str1)):
        if str1[i]=='0':
            notlist.append('1')
        else:
            notlist.append('0')
    return(g1(notlist))

def xor(str1,str2):  
    xorlist=[]
    for i in range(len(str1)):
        if str1[i]=='0' and str2[i]=='0':
            xorlist.append('0')
        if str1[i]=='1' and str2[i]=='1':
            xorlist.append('0')
        if str1[i]=='0' and str2[i]=='1':
            xorlist.append('1')
        if str1[i]=='1' and str2[i]=='0':
            xorlist.append('1')
    return(g1(xorlist))

# SHIFTING AND ROTATING

def rotateright(str1,n):
    list1 = g2(str1)
    count=0
    while count <= n-1:
        list2=list(list1)
        var_0=list2.pop(-1)
        list2=list([var_0]+list2)
        list1=list(list2)
        count+=1
    return(g1(list2))

def shiftright(str1,n):
    list1=g2(str1)
    count=0
    while count <= n-1:
        list1.pop(-1)
        count+=1
    append=['0']*n
    return(g1(append+list1))

# OPERATORS FOR CREATING NEW WORDS  
    
def Conditional(x,y,z):
    return(xor(And(x,y),And(Not(x),z)))

def Majority(x,y,z):
    return(xor(xor(And(x,y),And(x,z)),And(y,z)))

def sig0(x):
    return(xor(xor(rotateright(x,7),rotateright(x,18)),shiftright(x,3)))

def sig1(x):
    return(xor(xor(rotateright(x,17),rotateright(x,19)),shiftright(x,10)))

def e0(x):
    return(xor(xor(rotateright(x,2),rotateright(x,13)),rotateright(x,22)))

def e1(x):
    return(xor(xor(rotateright(x,6),rotateright(x,11)),rotateright(x,25)))

def modadd(x):
    a=0
    for i in range(len(x)):
        a+=x[i]
    return(a%2**32)

# CREATING 256 BITS PADDED MESSAGE

def padding(list1):
    pad1 = list1 + '1'
    lenofp1 = len(pad1)
    k=0
    while ((lenofp1+k)-448)%512 != 0:
        k+=1
    append0 = '0'*k
    append1 = binary64bit(len(list1))
    return(pad1+append0+append1)

def lenofmsg(str1):
    list1=[]
    for i in range(len(str1)):
        list1.append(binary8bit(ord(str1[i])))
    return(g1(list1))
 
def msglen1(str1):
    a = lenofmsg(str1)
    return(padding(a))

def msglen2(str1):
    return(G3(msglen1(str1),32))

def msgwords(index,msg):
    wnew = binary32bit(modadd([int(sig1(msg[index-2]),2),int(msg[index-7],2),int(sig0(msg[index-15]),2),int(msg[index-16],2)]))
    return(wnew)

# ALOGORITH:

def sha256(str1):
    # PADDED MESSAGE OF 256 BITS:
    msg=msglen2(str1)
    # HASH VALUES:
    hashvalues=['6a09e667','bb67ae85','3c6ef372','a54ff53a','510e527f','9b05688c','1f83d9ab','5be0cd19']
    # CONVERION OF HASH FROM HEX TO DEC:
    a=binary32bit(hextodec(hashvalues[0]))
    b=binary32bit(hextodec(hashvalues[1]))
    c=binary32bit(hextodec(hashvalues[2]))
    d=binary32bit(hextodec(hashvalues[3]))
    e=binary32bit(hextodec(hashvalues[4]))
    f=binary32bit(hextodec(hashvalues[5]))
    g=binary32bit(hextodec(hashvalues[6]))
    h=binary32bit(hextodec(hashvalues[7]))
    # CONSTANT WORDS:
    constants=['428a2f98','71374491','b5c0fbcf','e9b5dba5','3956c25b','59f111f1'
               ,'923f82a4','ab1c5ed5','d807aa98','12835b01','243185be','550c7dc3'
               ,'72be5d74','80deb1fe','9bdc06a7','c19bf174','e49b69c1','efbe4786'
               ,'0fc19dc6','240ca1cc','2de92c6f','4a7484aa','5cb0a9dc','76f988da'
               ,'983e5152','a831c66d','b00327c8','bf597fc7','c6e00bf3','d5a79147'
               ,'06ca6351','14292967','27b70a85','2e1b2138','4d2c6dfc','53380d13'
               ,'650a7354','766a0abb','81c2c92e','92722c85','a2bfe8a1','a81a664b'
               ,'c24b8b70','c76c51a3','d192e819','d6990624','f40e3585','106aa070'
               ,'19a4c116','1e376c08','2748774c','34b0bcb5','391c0cb3','4ed8aa4a'
               ,'5b9cca4f','682e6ff3','748f82ee','78a5636f','84c87814','8cc70208'
               ,'90befffa','a4506ceb','bef9a3f7','c67178f2']
    # FORMING NEW WORDS:
    for i in range(0,64):
        if i <= 15: 
            t_1=modadd([int(h,2),int(e1(e),2),int(Conditional(e,f,g),2),int(constants[i],16),int(msg[i],2)])
            t_2=modadd([int(e0(a),2),int(Majority(a,b,c),2)])
            h=g
            g=f
            f=e
            e=modadd([int(d,2),t_1])
            d=c
            c=b
            b=a 
            a=modadd([t_1,t_2])
            a=binary32bit(a)
            e=binary32bit(e)
        if i > 15:
            msg.append(msgwords(i,msg))
            t_1=modadd([int(h,2),int(e1(e),2),int(Conditional(e,f,g),2),int(constants[i],16),int(msg[i],2)])
            t_2=modadd([int(e0(a),2),int(Majority(a,b,c),2)])
            h=g
            g=f
            f=e
            e=modadd([int(d,2),t_1])
            d=c
            c=b
            b=a 
            a=modadd([t_1,t_2])
            a=binary32bit(a)
            e=binary32bit(e)
    # FINAL MESSAGE DIGEST:
    h0 = modadd([hextodec(hashvalues[0]),int(a,2)])
    h1 = modadd([hextodec(hashvalues[1]),int(b,2)])
    h2 = modadd([hextodec(hashvalues[2]),int(c,2)])
    h3 = modadd([hextodec(hashvalues[3]),int(d,2)])
    h4 = modadd([hextodec(hashvalues[4]),int(e,2)])
    h5 = modadd([hextodec(hashvalues[5]),int(f,2)])
    h6 = modadd([hextodec(hashvalues[6]),int(g,2)])
    h7 = modadd([hextodec(hashvalues[7]),int(h,2)])
    # HEX FORMAT HASH VALUE : 64 BITS IN HEX / 256 BITS IN BIN :
    h = (dectohex(h0)+dectohex(h1)+dectohex(h2)+dectohex(h3)+dectohex(h4)+dectohex(h5)+dectohex(h6)+dectohex(h7))
    return(h)
    
# TAKING MESSAGE INPUT:
    
print('Enter the message to be encoded: ')    
x=str(input())
print()

# SHA 256 OUTPUT:

print('The encoded message is: ')
print(*sha256(x))

