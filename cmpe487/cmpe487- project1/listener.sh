mainTerminal=$1
ipAdress=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/')
name=$2
#LogDirectory
while true
do
	message=$(nc -l 12345)
	echo "new message going to process : $message"
	./processMessages.sh "$message" $name $mainTerminal &
done

echo Exited from listener