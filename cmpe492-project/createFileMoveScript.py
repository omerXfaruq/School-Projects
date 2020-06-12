firstNo=2153293
lastNo=2153321

noForDir=1
with open("scriptForFileRenaming.sh","w") as f:
	f.write("cd fastqFiles")
	f.write("\n")
	while(firstNo<lastNo+1):
		
		f.write("mv fastqFiles"+str(noForDir)+" SRR"+str(firstNo))
		f.write("\n")
		firstNo+=1
		noForDir+=1

