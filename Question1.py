
m=[]
def encrypt(shift1,shift2):
    global m
    with open('raw_text.txt','r') as f:
        x=list(f.read())
        # print(list(x))
        # print(x)
        for i in x:
            # print(i)
            if(i.isalpha()):
                if(i.islower()):
                    if(ord(i)<108):
                        shift_val=shift2*shift1
                        i=chr((ord(i)+shift_val-97)%26+97)
                    else:
                        shift_val=shift2+shift1
                        i=chr((ord(i)-shift_val-97)%26+97)
                else:
                    if(ord(i)<78):
                        shift_val=shift1
                        i=chr((ord(i)-shift_val-65)%26+65)
                        
                    else:
                        shift_val=(ord(i)+shift2**2-65)%26+65
                        i=chr(shift_val)
            
            
            m.append(i)
               
                    
    m="".join(m)
    print(m)
    
encrypt(100,290)
with open('encrypted_text.txt','a') as f:
    f.write(m)
    
