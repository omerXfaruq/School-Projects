sleep 0.01
#echo processMessages $1.$2.$3.$4.$5
var=$1
name=$2
mainTerminal=$3
ipAdress=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/')

#echo new message $message
#word1=$(echo $message | cut -d " " -f1) #MessageType
#word2=$(echo $message | cut -d " " -f2) #ipAdressorname
#word3=$(echo $message | cut -d " " -f3) #NameorMessage
    
#Here are my quick notes about the protocol we designed in class:
#+ Use port 12345
#+ The "announce" packet format is [name, IP, announce]
#+ The "response" packet format is [name, IP, response]
#+ The "message" packet format is [name, IP, message, 'hello world'] where the message itself goes where "hello world" would go, in quotes. 
#+ One can only "announce" at most once per minute
#---

var=$(echo $var | tr -d '[')
var=$(echo $var | tr -d ']')
#echo $var
senderName=$(echo "${var%%,*}")
#echo $senderName  
var=$(echo "${var#*,}")
#echo $var
senderIP=$(echo "${var%%,*}")
#echo $senderIP
var=$(echo "${var#*,}")
#echo $var
type=$(echo "${var%%,*}")
#echo $type
var=$(echo "${var#*,}")
sentMessage=$(echo $var | tr -d "'")
#echo $sentMessage

#---
if [ $type == 'announce' ]
then
	./answerToBroadcast.sh $ipAdress $name $senderIP
	#echo answerToBroadcast.sh $ipAdress $name $senderIP
elif [ $type == 'response' ]
then
	echo "Got a contact"
	echo His name is $senderName, his ip is $senderIP
	echo $senderIP - $senderName >> logs/$name/contacts.conn
	#echo $senderIP - $senderName - logs/$name/contacts.conn
elif [ $type == 'message' ]
then
	echo Got A Message from $senderName, message: $sentMessage
	echo $senderName  - $(date +"%Y-%m-%d-%T") : $sentMessage >> logs/$name/$senderName.chatt
else
	echo "Got a message which does not apply to ÖF protocol"		
fi
sleep 1