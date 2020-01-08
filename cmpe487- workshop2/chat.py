from datetime import datetime
import time
import sys
import socket
import threading
import os

CONTACTS=dict()
CHATS=dict()
# time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    #return '25.35.113.203'
    return s.getsockname()[0]

HOST=get_ip_address()
PORT=12345

def broadcast(name, HOST):
	global LAST_REFRESH_TIME
	LAST_REFRESH_TIME=time.time()
	CONTACTS.clear()
	subnet=HOST[0:HOST.rfind('.')+1]

	#remove

	#subnet='25.37.151.'
	for i in range(255):
		sendAnnounce(name, HOST, subnet+str(i+1))

def sendAnnounce(name, HOST, destination):
	message="["+name+", "+HOST+", announce]"
	sendMessageInBackground(message,destination)

def sendResponse(name, HOST, destination):
	message="["+name+", "+HOST+", response]"
	sendMessageInBackground(message,destination)

def sendMessage(name, HOST, message, destination, destinationName):
	if destinationName in CHATS:
		CHATS[destinationName]+='\n'+name+" - "+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+": "+ message
	else:
		CHATS[destinationName]='\n'+name+" - "+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+": "+ message

	#todo: add adding to chat if message is sent
	message="["+name+", "+HOST+", message, '"+message+"']" 	
	sendMessageInBackground(message,destination)

def sendMessageInBackground(message, destination):
    #print("Sending message: "+ message + "to destination:  "+ destination)
    t = threading.Thread(target=deliverMessage, args = (message,destination))
    t.start()

def deliverMessage(message, destination):
	try:
		message=message.encode('ascii','ignore')
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((destination, PORT))
			s.sendall(message)
			s.close()
	
		return True
	except:
		#print ("This is an error message!")
		return False

def processMessage(message):
	global CONTACTS
	global CHATS
	message=message.decode('ascii')
	if message=='':
		return
	
#	print('Incoming message: '+ message)
	message=message.replace("[","")
	message=message.replace("]","")
	words=message.split(", ")

	if words[2]=='announce':
		print('Incoming message: Announce from: '+words[0]+' - '+words[1])
		if words[1]!=HOST:
			CONTACTS[words[0]]=words[1]
			sendResponse(USERNAME, HOST, words[1])
	elif words[2]=='response':
		print('Incoming message: Response from '+words[0]+' - '+words[1])
		CONTACTS[words[0]]=words[1]
	elif words[2]=='message':
		incomingMessage=words[3].replace("'","")
		print('Incoming message: Message from '+words[0]+' - '+words[1]+": "+incomingMessage)
		if words[0] in CHATS:
			CHATS[words[0]]+='\n'+words[0]+" - "+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+": "+ incomingMessage
		else:
			CHATS[words[0]]='\n'+words[0]+" - "+datetime.now().strftime('%Y-%m-%d %H:%M:%S')+": "+ incomingMessage

	else:
		print('Unsupported Protocol message has come')






def listener():

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(('', PORT))
		s.listen()
		conn, addr = s.accept()
		with conn:
			#print('Connected by', addr)
			while True:
				data = conn.recv(1024)
				processMessage(data)
				if not data:
					break
		conn.close()
	s.close()

def background():
	while(True):
		listener()
		#time.sleep(0.1)



#code starts


USERNAME=input("Hello, please enter your username accepted by ascii:\n")


b = threading.Thread(name='background', target=background)

b.start()


#interface starts
broadcast(USERNAME, HOST)
LAST_REFRESH_TIME=time.time()
time.sleep(5)

while(True):
	time.sleep(1)

	os.system('cls' if os.name == 'nt' else 'clear')
	option=input("\nHello, pick one of these choices:\n1:Refresh the CONTACTS(Can override 1 min cooldown)\n2:Show a chat\n3:Start chatting\n4:Exit\n")
	time.sleep(1)
	os.system('cls' if os.name == 'nt' else 'clear')
	

	if option=='1':
		broadcast(USERNAME, HOST)
		time.sleep(5)
		print("Broadcast is success")

	elif option =='2':
		

		print("Chats:\n")
		for i in CHATS.keys():
			print (i)
		#print(CHATS.keys())
		contact=input("\nWrite a contact name\n")
		
		if contact in CHATS:
			print(CHATS[contact])
		else:
			print('There is no chat corresponding to that name')
		input('Press enter to continue')
	
	elif option=='3':
		if (time.time() - LAST_REFRESH_TIME >= 60):
			print("1 min has passed, refreshing the contacts")
			broadcast(USERNAME, HOST)
			time.sleep(5)
			os.system('cls' if os.name == 'nt' else 'clear')

		else:
			print("1 min has not passed, not refreshing the contacts")
		
	#	print(CONTACTS)

#		if bool(CONTACTS):
#			print("There is no contact")
#			continue
		print("Contacts:\n")
		for i in CONTACTS.keys():
			print (i)
		#print(CONTACTS.keys())
		contact=input("\nWrite a contact name\n")
		if contact in CONTACTS.keys():
			while True:
				if contact in CHATS.keys():
					print(CHATS[contact])
				else:
					print('There is no prior chat')
				currentMessage=input("\nEnter your message accepted by ascii\n")
				sendMessage(USERNAME, HOST, currentMessage, CONTACTS[contact], contact )
				answer=input('\nEnter 0 if you want to continue chatting, press enter if you want to return to main menu \n\n')
				if answer!='0':
					break
				os.system('cls' if os.name == 'nt' else 'clear')

		else:
			print('There is no contact corresponding to that name')

	elif option=='4':
		print("Good Bye")
		time.sleep(1)
		os._exit(0)


	else:
		print('Wrong Input')