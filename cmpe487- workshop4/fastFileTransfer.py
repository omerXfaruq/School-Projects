#By FarukOzderim, date 29.11.19
#File sharing over udp on local with acknownledged messages
#Bypassed tcp with udp
import math
import subprocess
import hashlib
import datetime
import time
import sys
import socket
import threading
import os
import select


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    # return '25.35.113.203'
    return s.getsockname()[0]


CONTACTS = dict()		#For holding online users, and their UP
HOST = get_ip_address()
PORT = 12345
BUFFERSIZE = 1500
ENCODING = 'utf-8'
DELIMITER = ";!;"
ENCODEDDELIMITER = DELIMITER.encode(ENCODING)
MESSAGEQUEUE = dict()			#For sending messages in frequency of 1 seconds until acknown of the messages comes
threadLock = threading.Lock()	#Used for syncronization of MESSAGEQUEUE
threadLock2= threading.Lock()	#Used for syncronization of file receiving and ui
# PACKAGESET = set()

filePackets = [-1]	#For holding file's packages in an array
filePacketNo = -1


def acknownProcess(message):				#Incoming Message Handler, do the necessary job for each message type
    message = message.decode(ENCODING)
    # print("Message Incoming: " + message)
    words = message.split(DELIMITER, 5)  # Split by DELIMITER
    # print("Delimited Message: ", words)
    if words[0] != HOST:  # Check that sender is not myself
        if words[1] == "message":  # TODO: process the message
            print("Incoming message")
            returnHash = hashlib.sha1(words[5].encode(ENCODING)).hexdigest()
            if words[3] != returnHash:
                print("Package loss in package no: " + words[2])
                return
            createAcknownAndSendMessage("acknown", words[2], returnHash, words[0])
            # PACKAGESET.add(words[2])

        elif words[1] == "broadcast":  # TODO: add the contact to CONTACTS
            print('Incoming message: Broadcast - from: ' + words[0] + ' - ' + words[1])
            CONTACTS[words[5]] = words[0]
            createAndSendMessagePacket("response", words[0], USERNAME,
                                       words[0])  # Send a response with package number broadcasterIP

        elif words[1] == "response":
            print("Incoming Response")
            returnHash = hashlib.sha1(words[5].encode(ENCODING)).hexdigest()		#Check the hash
            if words[3] != returnHash:
                print("Package loss in package no: " + words[2])
                return
            CONTACTS[words[5]]=words[0]		#Add to contacts
            createAcknownAndSendMessage("acknown", words[2], returnHash, words[0])

        elif words[1] == "acknown":
            #print("Incoming acknown")
            # print(MESSAGEQUEUE)
            # print((MESSAGEQUEUE[words[2]]))
            threadLock.acquire()
            if words[2] in MESSAGEQUEUE and MESSAGEQUEUE[words[2]][0] == words[4]:
                MESSAGEQUEUE.pop(words[2], None)			#Delete from messagequeue
                #print("Size of the MESSAGEQUEUE: " + str(len(MESSAGEQUEUE)))
            threadLock.release()

        elif words[1] == "list":
            returnHash = hashlib.sha1(words[5].encode(ENCODING)).hexdigest()
            if words[3] != returnHash:
                print("Package loss in package no: " + words[2])
                return
            createAcknownAndSendMessage("acknown", words[2], returnHash, words[0])
            listedDir = subprocess.check_output("ls", shell=True)  # Send the file list in the directory
            #print(listedDir)
            #print(isinstance(listedDir, bytes))

			#Send the file list to other user
            createAndSendEncodedDataPacket("listedFiles", "-5", listedDir, words[0])


        elif words[1] == "listedFiles":
            threadLock2.acquire()
            returnHash = hashlib.sha1(words[5].encode(ENCODING)).hexdigest()
            if words[3] != returnHash:
                print("Package loss in package no: " + words[2])
                return
            createAcknownAndSendMessage("acknown", words[2], returnHash, words[0])
            fileName = input("\n\nEnter a file name:\n" + words[5])
            fileNames = words[5].split("\n")
            if not (fileName in fileNames):
                print("Wrong fileName")
                time.sleep(1)
                threadLock2.release()
                return
            print("Asking the file from the user, please wait")
            time.sleep(1)
            callcreateAndSendMessagePacketInBackground("fileRequest", "-5", fileName, words[0])
			#Ask for file from other user

        elif words[1] == "fileRequest":
            returnHash = hashlib.sha1(words[5].encode(ENCODING)).hexdigest()
            if words[3] != returnHash:
                print("Package loss in package no: " + words[2])
                return
            createAcknownAndSendMessage("acknown", words[2], returnHash, words[0])
            fileSize = os.path.getsize(words[5])
            noOfPackets = math.ceil(fileSize / 1024)
            callcreateAndSendMessagePacketInBackground("filePositions", "-5", words[5] + "-" + str(noOfPackets),
                                                       words[0])  # Send number of blocks in terms of packets
			#Send file information to other user

        elif words[1] == "filePositions":
            returnHash = hashlib.sha1(words[5].encode(ENCODING)).hexdigest()
            if words[3] != returnHash:
                print("Package loss in package no: " + words[2])
                return
            createAcknownAndSendMessage("acknown", words[2], returnHash, words[0])
            messages = words[5].split("-")
            fileName = messages[0]
            global filePacketNo
            filePacketNo = int(messages[1])
            print()
            print(filePacketNo)
            global filePackets
            filePackets = [-1] * int(filePacketNo)			#Initialize file informations
            # in background, run file writer method, where
			# incoming packets are written into file
            t1 = threading.Thread(target=fileWriter, args=(fileName, filePacketNo))
            t1.start()
            createAndSendMessagePacket("startTransfer", "-5", fileName, words[0])
			#Ask for the transfer from other user


        elif words[1] == "startTransfer":
            returnHash = hashlib.sha1(words[5].encode(ENCODING)).hexdigest()
            if words[3] != returnHash:
                print("Package loss in package no: " + words[2])
                return
            createAcknownAndSendMessage("acknown", words[2], returnHash, words[0])
            sendFileInPackets(words[5], words[0]) 			#Start transferin the file to other user

        elif words[1] == "filePart":
            returnHash = hashlib.sha1(words[5].encode(ENCODING)).hexdigest()
            if words[3] != returnHash:
                print("Package loss in package no: " + words[2])
                return
            createAcknownAndSendMessage("acknown", words[2], returnHash, words[0])
            # global filePackets
            if(int(words[2])>=int(filePacketNo)):
                return
            filePackets[int(words[2])] = words[5]
        # Put filepart into array filePackets for fileWriter method,
        else:
            print("Unsupported Message Incoming: " + message)


def sendFileInPackets(fileName, destinationIP):
    packetNo = 0
    file = open(fileName, "r")
    data = file.read(1024)
    #print("First chunk")
    #print(data)
    callcreateAndSendMessagePacketInBackground("filePart", str(packetNo), data, destinationIP)
    while (data):
        packetNo += 1
        data = file.read(1024)
        callcreateAndSendMessagePacketInBackground("filePart", str(packetNo), data, destinationIP)
    file.close()


def fileWriter(fileName, filePacketNo):
    file = open(fileName, 'w')
    index = 0
    #print("file packetsss")
    #print(filePackets)
    while (index < int(filePacketNo)):
        if(index%(int(filePacketNo/100)+1)==0):
            print("%"+str(100*(index + 1)/filePacketNo))    #print(index)
        if (filePackets[index] != -1):
            file.write(filePackets[index])
            index += 1
        else:
            time.sleep(0.1)     #Wait for package to come


    print("File writing is finished")
    file.close()
    time.sleep(1)
    threadLock2.release()		#Let main continue after file transfer is finished

def sendMessageInBackground(message, destinationIP):  # Send message via udp in background
    # print("Sending message: "+ message + "to destination:  "+ destination)
    t = threading.Thread(target=sendMessage, args=(message, destinationIP))
    t.start()


def sendMessage(message, destinationIP):  # Sends message via udp
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    if (isinstance(message, str)):
        message = message.encode(ENCODING)
    sock.sendto(message, (destinationIP, PORT))
    sock.close()
    #print("Sent message to: " + destinationIP + " this message: " + str(message))


def broadcast():  # Broadcasts ip and username
    global CONTACTS
    CONTACTS=dict()
    global LAST_REFRESH_TIME
    LAST_REFRESH_TIME=time.time()
    type = "broadcast"
    packageNumber = "-1"
    data = USERNAME
    words = ["", "", "", "", "", ""]
    words[0] = HOST.encode(ENCODING)
    words[1] = type.encode(ENCODING)  # broadcast,message,acknown,response
    words[2] = packageNumber.encode(ENCODING)
    words[3] = "".encode(ENCODING)  # hash
    words[4] = "".encode(ENCODING)  # returnHash
    words[5] = data.encode(ENCODING)
    message = words[0]
    for i in range(1, 6):
        message = message + ENCODEDDELIMITER + words[i]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 0))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(message, ('<broadcast>', 12345))


	#Can open triple broadcast for certainty,
    # time.sleep(1)
    # sock.sendto(message, ('<broadcast>', 12345))
    # time.sleep(1)
    # sock.sendto(message, ('<broadcast>', 12345))
    sock.close()


def createAcknownAndSendMessage(type, packageNumber, returnHash, destinationIP):
    # Might call createAndMessagePacket in background
    words = ["", "", "", "", "", ""]
    words[0] = HOST.encode(ENCODING)
    words[1] = type.encode(ENCODING)  # broadcast,message,acknown,response
    words[2] = packageNumber.encode(ENCODING)
    words[3] = "".encode(ENCODING)  # hash
    words[4] = returnHash.encode(ENCODING)  # returnHash
    words[5] = "".encode(ENCODING)
    message = words[0]
    for i in range(1, 6):
        message = message + ENCODEDDELIMITER + words[i]
    #print("Sending acknown message size  is: " + str(len(message)))
    sendMessage(message, destinationIP)
    # return message
    # addToAckWaitQueue


def callcreateAndSendMessagePacketInBackground(type, packageNumber, data, destinationIP):
    t1 = threading.Thread(target=createAndSendMessagePacket, args=(type, packageNumber, data, destinationIP))
    t1.start()


def callcreateAndSendEncodedDataPacket(type, packageNumber, data, destinationIP):
    t1 = threading.Thread(target=callcreateAndSendEncodedDataPacket, args=(type, packageNumber, data, destinationIP))
    t1.start()


def createAndSendEncodedDataPacket(type, packageNumber, data, destinationIP):
    words = ["", "", "", "", "", ""]
    words[0] = HOST.encode(ENCODING)
    words[1] = type.encode(ENCODING)  # broadcast,message,acknown,response
    words[2] = packageNumber.encode(ENCODING)
    words[3] = ""  # hash
    words[4] = "".encode(ENCODING)  # returnHash
    words[5] = data
    # words[5] = data.encode(ENCODING)
    hash = hashlib.sha1(words[5]).hexdigest()
    words[3] = hash.encode(ENCODING)  # TODO: create new method for acknown,
    message = words[0]
    for i in range(1, 6):
        message = message + ENCODEDDELIMITER + words[i]
    #print("Sending Size of the message is: " + str(len(message)))
    #print("Sending message to destinationIP,: " + str(message))
    threadLock.acquire()
    while (len(MESSAGEQUEUE) > 10):
        # print(str(len(MESSAGEQUEUE)))
        threadLock.release()
        #print("sleep for MESSAGEQUEUE")
        time.sleep(0.1)
        threadLock.acquire()
    MESSAGEQUEUE[packageNumber] = [hash, message, destinationIP]
    threadLock.release()
    # print(MESSAGEQUEUE)
    # print("Sending message packet size  is: " + str(len(message)))
    #print("Sending Encoded Data Packet to " + destinationIP)
    #print(message)
    sendMessage(message, destinationIP)
    # return message
    # addToAckWaitQueue


def createAndSendMessagePacket(type, packageNumber, data,
                               destinationIP):  # Might call createAndMessagePacket in background
    words = ["", "", "", "", "", ""]
    words[0] = HOST.encode(ENCODING)
    words[1] = type.encode(ENCODING)  # broadcast,message,acknown,response
    words[2] = packageNumber.encode(ENCODING)
    words[3] = ""  # hash
    words[4] = "".encode(ENCODING)  # returnHash
    words[5] = data.encode(ENCODING)
    hash = hashlib.sha1(words[5]).hexdigest()
    words[3] = hash.encode(ENCODING)  # TODO: create new method for acknown,
    message = words[0]
    for i in range(1, 6):
        message = message + ENCODEDDELIMITER + words[i]
   # print("Sending Size of the message is: " + str(len(message)))
    #print("Sending message to destinationIP,: " + str(message))
    threadLock.acquire()
    while (len(MESSAGEQUEUE) > 10):
        # print(str(len(MESSAGEQUEUE)))
        threadLock.release()
        #print("sleep for MESSAGEQUEUE")
        time.sleep(0.1)				#Wait for messageQueue to get smaller
        threadLock.acquire()
    MESSAGEQUEUE[packageNumber] = [hash, message, destinationIP]
    threadLock.release()
    # print(MESSAGEQUEUE)
    #print("Sending message packet size  is: " + str(len(message)))
    sendMessage(message, destinationIP)
    # return message
    # addToAckWaitQueue


def udpListener():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', PORT))
    s.setblocking(0)
    while (True):
     #   print("BUF size:" + str(s.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)))
        result = select.select([s], [], [])
        msg = result[0][0].recv(BUFFERSIZE)
        # msg = msg.decode(ENCODING)
        # print(len(msg))
        # print(isinstance(msg, str))
      #  print(msg)
        t = threading.Thread(target=acknownProcess, args=(msg,))
        t.start()
        # acknownProcess(msg)
        # sendAcknownInBackground(msg)

    # msg = result[0][0].recv(BUFFERSIZE)
    # msg = msg.decode(ENCODING)

    #    processMessage(msg)
    s.close()


def backgroundUdp():
    while (True):
        udpListener()


def backgroundResender():#Send packages again and again until acknown comes
    while (True):
        time.sleep(1)
        # print(MESSAGEQUEUE)
        threadLock.acquire()
        if (len(MESSAGEQUEUE)<5):
            threadLock.release()
            continue
        for package in MESSAGEQUEUE:
        #    print(package)
            # print(MESSAGEQUEUE[package])
            sendMessageInBackground(MESSAGEQUEUE[package][1], MESSAGEQUEUE[package][2])
        threadLock.release()


USERNAME = input("Hello, please enter your username accepted by UTF-8:\n")
print("\nWelcome " + USERNAME + ", program is starting")
b2 = threading.Thread(target=backgroundUdp)
b2.start()


LAST_REFRESH_TIME=time.time()

broadcast()


b4 = threading.Thread(target=backgroundResender)
b4.start()

# callcreateAndSendMessagePacketInBackground("message", "000", "helloThere", "192.168.43.165")

if USERNAME == "user2":
    print("Hrllleo")
    #    for i in range(10, 1000):
    # callcreateAndSendMessagePacketInBackground("message", "-5"),
    #                                                   "1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
    #                                               "192.168.43.165")
    # callcreateAndSendMessagePacketInBackground("message", "0000", "1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111", "10.10.1.244")
    # createAndSendMessagePacket("message", "0000", "helloThere", "10.10.0.191")

    callcreateAndSendMessagePacketInBackground("list", "-5", "xxx", "192.168.53.203")
    # callcreateAndSendEncodedDataPacket("filePart","000-1",b'aliVeli',"192.168.53.203")

    time.sleep(1)
    print("Size of the MEssageQUEUE: " + str(len(MESSAGEQUEUE)))
    print(MESSAGEQUEUE)
else:
    while(True):
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
        option = input(
            "\nHello, pick one of these choices:\n1:Refresh the CONTACTS(Can override 1 min cooldown)\n2:Start a file request\n3:Exit\n")
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

        if option == '1':
            broadcast()
            time.sleep(1)
            print("Broadcast is success")
            time.sleep(1)

        elif option == '2':
            if (time.time() - LAST_REFRESH_TIME >= 60):	#1 min cooldown on broadcast, might remove it because of acknowning
                print("1 min has passed, refreshing the contacts")	#an offline user will create a problem on sending packets
                broadcast()											#again and again
                time.sleep(1)
                os.system('cls' if os.name == 'nt' else 'clear')

            else:
                print("1 min has not passed, not refreshing the contacts")

            print("Contacts:\n")
            if(len(CONTACTS.keys())!=0):
                for i in CONTACTS.keys():
                    print(i + " - "+ CONTACTS[i])
                # print(CONTACTS.keys())
                contact = input("\nEnter a contact name\n")
                if contact in CONTACTS.keys():

                    callcreateAndSendMessagePacketInBackground("list", "-5", "xxx", CONTACTS[contact])
                    print("Iniating file request, please wait")
                    time.sleep(1)
                    threadLock2.acquire()#Wait till file transfer is finished
                    threadLock2.release()
                    time.sleep(1)
                    os.system('cls' if os.name == 'nt' else 'clear')
                else:
                    print('There is no contact corresponding to that name')
            else:
                print("There is no online user available")


        elif option == '3':
            print("Good Bye")
            time.sleep(1)
            os._exit(0)

        else:
            print('Wrong Input')
        '''
        if option == '1':
            broadcast(USERNAME, HOST)
            time.sleep(5)
            print("Broadcast is success")
        
        elif option == '2':
        
            print("Chats:\n")
            for i in CHATS.keys():
                print(i)
            # print(CHATS.keys())
            contact = input("\nWrite a contact name\n")
        
            if contact in CHATS:
                print(CHATS[contact])
            else:
                print('There is no chat corresponding to that name')
            input('Press enter to continue')
        
        elif option == '3':
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
                print(i)
            # print(CONTACTS.keys())
            contact = input("\nWrite a contact name\n")
            if contact in CONTACTS.keys():
                while True:
                    if contact in CHATS.keys():
                        print(CHATS[contact])
                    else:
                        print('There is no prior chat')
                    currentMessage = input("\nEnter your message accepted by ascii\n")
                    sendMessage(USERNAME, HOST, currentMessage, CONTACTS[contact], contact)
                    answer = input(
                        '\nEnter 0 if you want to continue chatting, press enter if you want to return to main menu \n\n')
                    if answer != '0':
                        break
                    os.system('cls' if os.name == 'nt' else 'clear')
        
            else:
                print('There is no contact corresponding to that name')
        
        elif option == '4':
            print("Good Bye")
            time.sleep(1)
            os._exit(0)
            
         else:
        print('Wrong Input')
        '''

        # print("Received package size: " + str(len(PACKAGESET)))
        # print(PACKAGESET)
