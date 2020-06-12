firstNo=2153293
lastNo=2153321

noForDir=1
with open("scriptForDownloadingDatabase.sh","w") as f:
	f.write("wget ftp://ftp.ensembl.org/pub/release-100/fasta/mus_musculus/cdna/Mus_musculus.GRCm38.cdna.all.fa.gz")
	f.write("\n")
	f.write("rm -rf fastqFiles")
	f.write("\n")
	f.write("mkdir -p fastqFiles")
	f.write("\n")
	f.write("cd fastqFiles")
	f.write("\n")
	while(firstNo<lastNo+1):
		
		f.write("mkdir -p fastqFiles"+str(noForDir))
		f.write("\n")
		f.write("cd fastqFiles"+str(noForDir))
		f.write("\n")
		
		stringCode="SRR"+str(firstNo)
		downloadUrl="ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR215/00"+str(firstNo%10)+"/"+stringCode+"/"+stringCode+".fastq.gz" 
		f.write("wget "+downloadUrl)
		f.write("\n")
		
		f.write("cd ..")
		f.write("\n")
		f.write("\n")
		firstNo+=1
		noForDir+=1

