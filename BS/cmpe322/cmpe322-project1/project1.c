//By FarukOzderim
char* stack[1000];			//Create an array of 1000 for stack	

char** sp=stack;			//İnitialize the beginning of the stack

	
#define push(sp, n) (*((sp)++) = (n))		//Define pop and push
#define pop(sp) (*--(sp))


#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>


#define MAX_COUNT 1000

int forking(char** command,char* newFile){	//Used for running programs,
	pid_t pid;								//If newFile==! , print the output
    int i;									//Otherwise write the output to newFile named file
    int y;
	pid = fork(); /* creating a child process */
	if (pid < 0) /* error occurred returns -1 */
	{  
		fprintf(stderr, "Fork Failed"); 
		return 1;
	}
	else if (pid == 0) /* execution of the child process */
	{ 
    /*Reference
		char *argv[] = { "/bin/ls", "-l", 0 };
		execv(argv[0], argv);
		execvp(argv[0], argv);
	*/
		
		if(newFile[0]!='!'){
			int fd;
			if((fd = open(newFile, O_RDWR | O_CREAT, S_IRUSR | S_IWUSR))==-1){
					printf("Failed to create a file, exit\n");
					return -1;
				}
			dup2(fd, 1);   // make stdout go to file
			dup2(fd, 2);   // make stderr go to file 


			close(fd);     // fd no longer needed - the dup'ed handles are sufficient
		}

		execv(command[0],command);
	}
	else /* execution of the parent process */
	{  
		wait(NULL); /* parent will wait for the child to complete */
	}

}

//**
//Print at most last 15 commands from stack
void printHistory(){
	for(int i=1;i<=sp-stack && i<16;i++){
			printf("%d - %s\n",i,(*(sp-i)));
	}
	

}

void handleInput(char newString[5][40]){			//Input handler, newString are words of the user input

	if(!strcmp(newString[0],"listdir")){					//If branches
		if(!strcmp(newString[1],"-a")){
			if(!strcmp(newString[2],"|")){
				if(strcmp(newString[3],"grep")){		//Check wrong input
					printf("Wrong Input\n, exiting");
					return;
				}
				char * arguments[]={"/bin/ls","-a",0};		//exec ls -a and write it to a temporary file				
				forking(arguments,"tempFile.txt");
				
															//Delete ""s from the searched keyword
				char newName[strlen(newString[4])-2];
				for(int i=0;i<strlen(newString[4])-2;i++){
					newName[i]=newString[4][i+1];
				}
				newName[strlen(newString[4])-2]='\0';
	
				char * arguments2[]={"/bin/grep",newName,"tempFile.txt",0};
				forking(arguments2,"!");									//grep from temporary file
			    if (remove("tempFile.txt") == 0) 							//delete the temporary file
				{}
				else
				    printf("Unable to delete the file\n"); 
			}else if((newString[2][0]=='\0')){
				char * arguments[]={"/bin/ls","-a",0};						//exec ls -a
				forking(arguments,"!");
			}else{
				printf("Wrong input\n");
			}
		}else if(!strcmp(newString[1],"|")){
			if(strcmp(newString[2],"grep")){		//Check wrong input
				printf("Wrong Input\n, exiting");
				return;
			}
			char * arguments[]={"/bin/ls",0};						//exec ls and write it to a temporary file				
			forking(arguments,"tempFile.txt");
			
																	//Delete ""s from the searched keyword
			char newName[strlen(newString[3])-2];
			for(int i=0;i<strlen(newString[3])-2;i++){
				newName[i]=newString[3][i+1];
			}
			newName[strlen(newString[3])-2]='\0';

			char * arguments2[]={"/bin/grep",newName,"tempFile.txt",0};
			forking(arguments2,"!");									//grep from temporary file
			if (remove("tempFile.txt") == 0) 							//delete the temporary file
			{}//printf("Deleted successfully\n"); 
			else
				printf("Unable to delete the file\n"); 
			
		}else if((newString[1][0]=='\0')){
			//printf("at listdir\n");
			char * arguments[]={"/bin/ls",0};						//exec ls and print
			forking(arguments,"!");
		}else{
			printf("wrong input\n");
		}
		
	}
	else if(!strcmp(newString[0],"currentpath")){			//If branches
		//printf("we are at current path option\n");
		char * arguments[]={"/bin/pwd",0};						//exec pwd 
		forking(arguments,"!");
		
		
	}else if(!strcmp(newString[0],"printfile")){
		if(!strcmp(newString[2],">")){
																	//printfile file > newFile		
			char * arguments[]={"/bin/cat",newString[1],0};			
			forking(arguments,newString[3]);							 //exec cat then write to temporary file
		}
		else if (newString[2][0]=='\0'){
			//printf("$$$ we are at printfile option\n");

			char * arguments[]={"/bin/cat",newString[1],0};			//exec cat 
			forking(arguments,"!");
			printf("\n");
		}
		else{
			printf("Wrong Input\n");
			return;
		}
			
	}else if(!strcmp(newString[0],"footprint")){				//print history from stack
		//printf("we are at footprint option\n");
		printHistory();
	}else if(!strcmp(newString[0],"exit")){						//exit
		//printf("we are at exit option\n");
		exit(0);
	}else
		printf("Wrong Input\n");
	
}

int main(){
	//Take input and process
	
	char* whoami[]={"/usr/bin/whoami",0};
	forking(whoami,"tempFile.txt");			//Write username to temporary file
    
	char name[255];
	FILE *fp;
	fp=fopen("tempFile.txt","r");
    fscanf(fp, "%s", name);
	if (remove("tempFile.txt") == 0) 		//delete the temporary file
	{}//printf("Deleted successfully\n"); 
	else
		printf("Unable to delete the file\n"); 
	
	
	while(1){
		char str1[200];					//User Input
		char newString[5][40];			//Will get splitted by words
		int i,j,ctr;			
		
		
		
		printf("%s >>> ",name);
		fgets(str1, sizeof str1, stdin);					//Get Input
		//printf("The input is: %s\n",str1);
		char* newstr2=malloc(200*sizeof(char));		
		strcpy(newstr2,str1);
		push(sp,newstr2);							//Put it into stack
		j=0; ctr=0;
		newString[0][0]='\0';						//Reset words for splitting word by word
		newString[1][0]='\0';
		newString[2][0]='\0';
		newString[3][0]='\0';
		newString[4][0]='\0';
		for(i=0;i<=(strlen(str1));i++)					//Split it word by word
		{
			// if space or NULL found, assign NULL into newString[ctr]
			if(str1[i]=='\n' || str1[i]==' '|| str1[i]=='\0')
			{
				if (j==0)						//For not writing an empty string as a word
					continue;
				newString[ctr][j]='\0';
				ctr++;  //for next word
				j=0;    //for next word, init index to 0
			}
			else
			{
//				printf("%d, $ctr\n",ctr);
				newString[ctr][j]=str1[i];					//split the word
				j++;
			}
		}
		
		handleInput(newString);						//Handle the input
		 
	}
	
	
	return 0;
}