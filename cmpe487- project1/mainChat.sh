trap "kill 0" 2
pkill nc
chmod +x *.sh
ttyNumber=$(tty)
echo "Please enter a name without space"
read name
echo Welcome $name

[ -d logs ] || mkdir logs
#mkdir logs >> unwanted.logs 
[ -d logs/$name ] || mkdir logs/$name
#mkdir logs/$name  
./listener.sh $ttyNumber $name &
listenerPid=$!

./broadcast.sh $name

while true
do
	sleep 1
	clear
	echo "What do you want to do"
	echo "1. Show Chat"
	echo "2. Send Message"
	echo "3. Exit"

	read option
    if [ $option == '1' ]
	then
#Gotta use a directory for chat files
		clear
		echo $(ls logs/$name | grep .chatt)
		echo "Write the name of the person of the chat,enter 0 for main menu"
		read var2

		if [ $var2 == '0' ]
		then
			clear
		elif [[ $(ls logs/$name | grep $var2.chatt ) ]]
		then

			echo ""
			cat logs/$name/$var2.chatt
			echo "Press enter to continue"
			read var4
		else
			echo There is no chat like that
			sleep 1
		fi	

	elif [ $option == '2' ]
	then
		./broadcast.sh $name 
		cat logs/$name/contacts.conn
		echo "Who Do You Want To Chat To, please enter a name, press enter 0 for main menu"
		read var3
		if [ $var3 == '0' ]
		then
			clear
 
		elif [[ $(cat logs/$name/contacts.conn | grep $var3 ) ]]
		then
			echo "Please enter your message"
			read message
			ipOfMessage=$(cat logs/$name/contacts.conn | grep $var3 | cut -d " " -f1) #GetTheIp
			nameOfTheContact=$(cat logs/$name/contacts.conn | grep $var3 | cut -d " " -f3) #GetTheName
			#echo NAME.MESSAGE.IP $name.$message.$ipOfMessage
			echo $name  - $(date +"%Y-%m-%d-%T") : $message >> logs/$name/$nameOfTheContact.chatt
			./sendMessage.sh $name "$message" $ipOfMessage


		else
			echo There is no contact like that
			sleep 1

		fi	

	elif [ $option == '3' ]
	then
		echo "Exiting"
		pkill bash 
		exit
		exit
	else
		echo Wrong Input
	fi
done

#flag=0
#while[flag!=3]
#clear
#echo "What do you want to do"
#echo "1. Show Chat"
#echo "2. Send Message"
#echo "3. Reload Contacts"
#echo "4. Exit"

#read option

#pkill nc
#kill -9 $listenerPid
