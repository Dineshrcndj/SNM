import random
def gen_otp():
    gotp=''
    cap=[chr(i) for i in range(ord('A'),ord('Z')+1)]
    small=[chr(i) for i in range(ord('a'),ord('z')+1)]
    for i in range(2):
        gotp=gotp+random.choice(cap)
        gotp=gotp+random.choice(small)
        gotp=gotp+str(random.randint(0,9))
    return gotp


