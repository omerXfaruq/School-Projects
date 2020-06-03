#+ The "announce" packet format is [name, IP, announce]
#./sendIP.sh $ipAdress $name $ip1 $ip2 $ip3 1 &
sent="[$2, $1, announce]"
#echo $sent >> sendIP.txt
echo $sent | nc -N $3.$4.$5.$6 12345 &