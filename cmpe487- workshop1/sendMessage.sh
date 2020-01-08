#$1 is the name, $2 is the message, $3 is the target_IP_ADRESS
myIpAdress=$(ip addr | grep 'state UP' -A2 | tail -n1 | awk '{print $2}' | cut -f1  -d'/')
message="'$2'"
sent="[$1, $myIpAdress, message, $message]"
#echo $sent
echo $sent | nc -N $3 12345 &


