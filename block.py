import socket, select,time    
from rc4test import RC4  
current_milli_time = lambda: int(round(time.time() * 1000))
# next create a socket object 
s = socket.socket()          
print("Socket successfully created")
  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 2050               
  
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
s.bind(('', port))
#s.setblocking(0)
print("Socket bound")
  
# put the socket into listening mode 
s.listen(5)      
print("Socket lisltening")        

import xml.etree.ElementTree as ET
a = ET.parse("packets.xml")
a = a.getroot()
id_dict={}
packetdict={}
for i in a:
    id_dict[int(i[1].text)]=i[0].text
    packetdict[i[0].text]=int(i[1].text)
def id2packet(num):
    return id_dict.get(int(num))
def packet2id(num):
    return packetdict.get(num)
    
curt=0
# a forever loop until we interrupt it or  
# an error occurs 
cipher=RC4(bytes.fromhex("6a39570cc9de4ec71d64821894c79332b197f92ba85ed281a023"[0:26]))
decipher=RC4(bytes.fromhex("6a39570cc9de4ec71d64821894c79332b197f92ba85ed281a023"[26:]))
cipherP=RC4(bytes.fromhex("6a39570cc9de4ec71d64821894c79332b197f92ba85ed281a023"[0:26]))
decipherP=RC4(bytes.fromhex("6a39570cc9de4ec71d64821894c79332b197f92ba85ed281a023"[26:]))

HOST="3.128.144.191"   # use4
#HOST="3.92.195.197" #usw3
PORT = 2050 # The port used by the server
sh=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sh.connect((HOST, PORT))
sh.setblocking(0)
def trans(x):
   return int.from_bytes(x,byteorder='big')

if True: 

   # Establish connection with client. 
   c, addr = s.accept()
   
   print(addr)
   
   len1=c.recv(1024)
   print(len1)
   if b"policy" in len1:
      c.send(str.encode('''<cross-domain-policy>
     <allow-access-from domain="*" to-ports="*" />
</cross-domain-policy>\x00'''))
      x=c.recv(1024)
   else:
      x=len1
   print(x)
   size=x[0:4]
   id=x[4]
   print("client: ",trans(x[:4]),id2packet(x[4]),cipher.crypt(x[5:]))
   cipherP.crypt(x[5:])
sh.send(x)
c.setblocking(0)
sh.setblocking(0)
passed=False
packetPart=b''
passed1=False
packetPart1=b''
while True:
   a,b,d=select.select([c,sh],[],[],0)
   if current_milli_time() - curt > 1000:
       #sh.send(b'\x00\x00\x00\x0e\x37'+cipherP.crypt(b'\x00\x00\x01\xb9\x08\x00\x00\n5'))
       #sh.send(b'\x00\x00\x00\x0e\x37'+cipherP.crypt(b'\x00\x00\x01\xb9\t\x00\x00\n5'))
       #sh.send(b'\x00\x00\x00\x0e\x37'+cipherP.crypt(b'\x00\x00\x01\xb9\n\x00\x00\n5'))
       #sh.send(b'\x00\x00\x00\x0e\x37'+cipherP.crypt(b'\x00\x00\x01\xb9\x0b\x00\x00\n5'))
       curt = current_milli_time()
   for sock in a:
       if sock==sh:
           rc=(sh.recv(100096))
           temp=rc
           cur=b""
           if passed:
               temp=packetPart+temp
               passed=False
               packetPart=b''
           while len(temp) >=5:
              if len(temp[5:trans(temp[:4])])+5 < trans(temp[:4]):
                 print(len(temp[5:trans(temp[:4])])+5)
                 passed=True
                 packetPart+=temp
                 break
              msg=decipher.crypt(temp[5:trans(temp[:4])])
              check = id2packet(int(temp[4]))!='ACTIVEPETUPDATE'
              if id2packet(int(temp[4]))!='NEWTICK':
                 print("server: ",trans(temp[:4]),id2packet(int(temp[4])),msg)
              if b'{"key":"server.invite_notfound","tokens":{"player":"Wtaifj"}}' in msg:
                 1
              elif b'{"key":"server.invite_hasguild","tokens":{"player":"Wtaifj"}}' in msg:
                 1
              elif b'Not enough Gold' in msg:
                 1
              elif id2packet(int(temp[4]))=='ACTIVEPETUPDATE':
                 1
              elif id2packet(int(temp[4]))=='BUYRESULT':
                 1
              #if id2packet(int(temp[4]))=='RECONNECT':
              #   1
              else:
                 cur+=temp[:5]+decipherP.crypt(msg)
              temp=temp[trans(temp[:4]):]
           """while len(temp) >=5:
              print("server: ",trans(temp[:4]),temp[4],decipher.crypt(temp[5:trans(temp[:4])]))
              temp=temp[trans(temp[:4]):]"""
           if len(temp) >0 and len(temp) < 5:
               passed=True
               packetPart+=temp
           rc=cur
           c.send(rc)
       else:
           x=c.recv(100024)
           temp = x
           cur=b""
           #13 15 b'\x00\x06Wtaifj' guildremove
           #17 37 b'\x00\x06Wtaifj\x00\x00\x00\x00', demotion to initiate, \x0n for promote
           # 13 5 b'\x00\x06Wtaifj' trade
           while len(temp) >=5:
              msg=cipher.crypt(temp[5:trans(temp[:4])])
              #if id2packet(int(temp[4]))=='INVSWAP':
              if id2packet(int(temp[4]))!='MOVE':
                  print("client: ",trans(temp[:4]),id2packet(int(temp[4])),msg)
              if temp[4]==10 and msg.endswith(b'/dupe'):
                 #sh.send(b'\x00\x00\x00\x0d\x0a'+cipherP.crypt(b'\x00\x06ppoopp'))
                 chi=b''
                 for i in range(8000):
                    f=cipherP.crypt(b'\x00\x06Wtaifj')
                    chi+=(b'\x00\x00\x00\x0d\x68'+f)
                 sh.send(chi)
              elif temp[4]==10 and msg.endswith(b'/doop'):
                 for i in range(20000):
                    sh.send(b'\x00\x00\x00\x09\x33'+cipherP.crypt(b'\x00\x00\x00\x00'))
              elif temp[4]==packet2id('PONG'):
                  msg1=(int.from_bytes(msg[:-4], "big")).to_bytes(4, byteorder='big')
                  msg1+=(int.from_bytes(msg[-4:], "big")).to_bytes(4, byteorder='big')
                  cur+=temp[:5]+cipherP.crypt(msg1)
                  #msg1=(int.from_bytes(msg[:-4], "big")*2+1).to_bytes(4, byteorder='big')
                  #msg1+=(int.from_bytes(msg[-4:], "big")).to_bytes(4, byteorder='big')
                  #cur+=temp[:5]+cipherP.crypt(msg1)
              elif temp[4]==10 and msg.endswith(b'/guildspam'):
                 for i in range(200):
                    cur+=(b'\x00\x00\x00\x0d\x0f'+cipherP.crypt(b'\x00\x06Wtaifj'))
                    cur+=(b'\x00\x00\x00\x0d\x68'+cipherP.crypt(b'\x00\x06Wtaifj'))
              elif temp[4]==10 and msg.endswith(b'/petspam'):
                 for i in range(2000):
                    cur+=(b'\x00\x00\x00\x0a\x18'+cipherP.crypt(b'\x01\x00\x00\x00\x00'))
                    cur+=(b'\x00\x00\x00\x0a\x18'+cipherP.crypt(b'\x02\x00\x00\x00\x00'))
                 #sh.send(cur)
                 #sh.close()
              elif temp[4]==10 and msg.endswith(b'/skinspam'):
                 for i in range(2000):
                    cur+=(b'\x00\x00\x00\x09\x33'+cipherP.crypt(b'\x00\x00\x00\x00'))
                    cur+=(b'\x00\x00\x00\x09\x33'+cipherP.crypt(b'\x00\x00\x03h'))
              elif temp[4]==10 and msg.endswith(b'/namespam'):
                 for i in range(2000):
                    cur+=(b'\x00\x00\x00\x09\x61'+cipherP.crypt(b'\x00\x02dd'))
                 #for i in range(2000):
                 #   msg=cipherP.crypt(b'\x00\x06Wtaifj')
                 #cur+=(b'\x00\x00\x00\x0d\x68'+msg)
              elif temp[4]==10 and msg.endswith(b'/vaultspam'):
                 for i in range(300):
                    cur+=b'\x00\x00\x00\x0e\x1b'
                    cur+=cipherP.crypt(b'\x00'*9)
                    cur+=b'\x00\x00\x00\x0e\x1b'
                    cur+=cipherP.crypt(b'\x00'*9)
              elif id2packet(int(temp[4]))=='EDITACCOUNTLIST':
                  for j in range(1):
                     dupe=b''
                     for i in range(100):
                        dupe+=temp[:5]+cipherP.crypt(msg)
                        dupe+=temp[:5]+cipherP.crypt(b'\x00\x00\x00\x01\x01'+msg[5:])
                        dupe+=temp[:5]+cipherP.crypt(msg[:4]+b'\x00'+msg[5:])
                        dupe+=temp[:5]+cipherP.crypt(b'\x00\x00\x00\x01\x00'+msg[5:])
                     sh.send(dupe)
                     dupe=b''
              elif id2packet(int(temp[4]))=='ACCEPTTRADE':
                  sh.send(b'\x00\x00\x00\x05\x5b')
                  sh.send(temp[:5]+cipherP.crypt(msg))         
              elif id2packet(int(temp[4]))=='BUY':
                  print("bum", msg)
                  for j in range(1):
                     dupe=b''
                     for i in range(1):
                        dupe+=temp[:5]+cipherP.crypt(msg[:4]+b'\x00\x00\x00\x00')
                        #dupe+=temp[:5]+cipherP.crypt(msg[:4]+b'\x00'+msg[5:])
                     sh.send(dupe)
                     dupe=b''
              elif temp[4]==10 and msg.endswith(b'/shotspam'):
                 for i in range(1000):
                    cur+=(b'\x00\x00\x00\x05\x34')
                 #for i in range(2000):
                 #   msg=cipherP.crypt(b'\x00\x06Wtaifj')
                 #cur+=(b'\x00\x00\x00\x0d\x68'+msg)
                 """elif temp[4]==10 and b'/doop' in msg:
                 sh.send(b'\x00\x00\x00\x0d\x68'+msg)
                 27 JOINGUILD b'\x00\x14Creamcheese Toenails'
                 39 INVITEDTOGUILD b'\x00\nMethDebate\x00\x14Creamcheese Toenails'
              elif temp[4]==5:
                 #cur+=temp[:5]+cipherP.crypt(b'\x00\x05/poop')
                 for i in range(10):
                    cur+=b'\x00\x00\x00\x0d\x05'+cipherP.crypt(b'\x00\x06Wtaifj')""" 
              else:
                 cur+=temp[:5]+cipherP.crypt(msg)
              temp=temp[trans(temp[:4]):]
           x=cur
           sh.send(x)
           # Close the connection with the client """
   
