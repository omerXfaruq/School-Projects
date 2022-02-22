# cmpe322- project1

**Writing Terminal Program**

This a terminal program written in c, using basic exec and fork functionalities.  
_By FarukOzderim_  
**Running**  
make  
./project1  

**Available Commands:**

● listdir  
○This command will print out the contents of the current directory, same as the “ls” command in bash.  
○ Example usage: >>> listdir  

● listdir -a  
○ The listdir command can take a flag if provided, as “-a” (as done with “ls -a”). This flag provides the opportunity of listing the directories or files that starts with “.”, which means that they are the hidden contents.  
○ Example usage: >>> listdir -a  

● currentpath  
○ This command will print out the current working directory. This functionality is provided  by the “pwd” command in most of the shells.  
○ Example usage: >>> currentpath  

● printfile (fileName)  
○ This command will take a file name as an argument, read its content and write them on the standard output. This functionality is provided by the “cat” command in most of the shells.  
○ Example usage: >>> printfile myText.c  

● printfile(fileName) > (newFileName)  
○ This command will take a file name as an argument, and redirect the standard output to a new file using the redirection operator, >, (greater than symbol). This functionality is provided by the “cat” command in most of the shells.  
○ Example usage: >>> printfile myText.c > myTextNew.c  

● footprint  
○ This command will simply print up to maximum 15 commands that are executed before. The output will be the list of commands in which each line has a history number (starting with 1) and the corresponding command. This functionality is provided by the “history” command in most of the shells.  
○ Example usage: >>> footprint  

● listdir | grep “argument”  
○ This command includes pipe between to processes. The output of the listdir command will be redirected to grep, and it will search for a pattern provided as the “argument”. Since you are already familiar with, grep command requires an input to search for a pattern, and that input should be provided by the output of the listdir command.  
○ This command should be also available for “listdir -a” command.  
○ Example usage: >>> listdir | grep “.c”  
○ Example usage: >>> listdir -a | grep “txt”  

● exit  
○ Your shell process will be terminated after the user enters the exit command.  
○ Example usage: >>> exit  
