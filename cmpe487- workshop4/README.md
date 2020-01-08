Submitted!

# tcp_over_udp
By FarukOzderim

This project is file sharing project in local network.
It is done over udp, bypassing tcp, there are 2 versions.  
1-fastFileTransfer.py  
2-reliableFileTransfer.py

Only text based files are supported in this program.  
It is better to use reliableFileTransfer.py for reliable transfer.


In fastFileTransfer file packets are sent in unique threads, however network connection errors cause thread explosion. Also couldnt limit  
maximum thread number, due to threads not recognizing global variables as same value(well spent a lot of time but still feels absurd). Thread explosion happens in bigger files.

ReliableFileTransfer sends filePackets in single thread. It is slow compared to fastFileTransfer. However it can handle network corruptions. And works fine.


To run it, use python, and run the code in different machines. You can request files from other machine in the directory where code is running.

Tested with myself.