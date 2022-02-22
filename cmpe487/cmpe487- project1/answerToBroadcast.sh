# $1 is ipAdress
# $2 is name
# $3 destination ipAdress
#+ The "response" packet format is [name, IP, response]

sent="[$2, $1, response]"
#echo $sent
echo $sent | nc -N $3 12345 &

