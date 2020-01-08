# nc-chat-bash
_By FarukOzderim_  

This is a bash LAN chat program using netcat. 

# Environment

BSD NetCat   

The code itself uses several other commands, eg. `ifconfig`, `printf`, `trap`, internally and most of them come with any basic
shell.

The app should be run via direct execution. It may work with `source` executable, but that's not for sure. After pulling the
repo, the script file should be granted with execution permissions:

``` Bash
chmod +x *.sh
./mainChat.sh
```

If there is left bacground processes and it causes error, you can use 

./cleanNc.sh

The sufficient amount of how-to-use instructions are given within the app.


# Inabilities
- Names with spaces are not avaliable.
- 's are not recognized in the received message.


# Protocol

Data should be in the given format below:

``` regex
[username, local_ip, message_type, optional_argument]
```

There are a total of three message types, namely `announce`, `response` and `message`. `message` type of data should 
also contain a fourth parameter, `optional_argument`. Some samples of each of those are given below.

``` regex
[player, 192.168.1.1, announce]
```

``` regex
[player, 192.168.11.22, response]
```

``` regex
[player, 192.168.12.21, message, hi there. How are you doing?]
```


# Tester: 

Tested with Bahadır Hocamoğlu
