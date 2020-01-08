# python-chat
_By FarukOzderim_  

Python socket chat program by Ömer Faruk Özdemir via TCP  

# Environment

The chat app is written with python3. It uses socket in the standart python library.

Required packages can be found from Requirements.txt

The app should be run with python. 

The app is volatile meaning your messages is not stored.

The app has a cooldown of broadcast of 1 minute. But you can bypass that in the program with  action selection.
``` Bash
python3 chat.py

```
The sufficient amount of how-to-use instructions are given within the app.


# Inabilities
-Dont use ',' in your name

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
[player, 192.168.12.21, message, 'hi there. How are you doing?']
```
