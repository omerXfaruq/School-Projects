package main;

import java.io.*;
import java.security.NoSuchAlgorithmException;
import java.util.*;
import java.util.concurrent.TimeUnit;


import project.MerkleTree;

public class Main {

	public static void main(String[] args) throws IOException, NoSuchAlgorithmException, InterruptedException {





		for(int i=0;i<4;i++) {
			MerkleTree m1 = new MerkleTree("data/"+i+".txt");
			System.out.println(m1.checkAuthenticity("data/"+i+"meta.txt"));
		}MerkleTree m0 = new MerkleTree("sample/white_walker.txt");
		MerkleTree m2=new MerkleTree("data/1_bad.txt");
		System.out.println(m2.findCorruptChunks("data/1meta.txt").size());
		MerkleTree m3=new MerkleTree("data/9.txt");
		System.out.println(m3.checkAuthenticity("data/9meta.txt"));
		String hash0 = m0.getRoot().getData();
		String hash1=m0.getRoot().getLeft().getData();
		String hash2=m0.getRoot().getRight().getData();
		String hash3=m0.getRoot().getLeft().getLeft().getData();
		String hash4=m0.getRoot().getLeft().getRight().getData();
		String hash5=m0.getRoot().getRight().getLeft().getData();
		String hash6=m0.getRoot().getRight().getRight().getData();
		System.out.println(hash0);
		System.out.println(hash1);
		System.out.println(hash2);
		System.out.println(hash3);
		System.out.println(hash4);
		System.out.println(hash5);
		System.out.println(hash6);


		boolean valid = m0.checkAuthenticity("sample/white_walkermeta.txt");
		System.out.println(valid);

		System.out.println("\n\n\n\n");


		// The following just is an example for you to see the usage.
		// Although there is none in reality, assume that there are two corrupt chunks in this example.

		MerkleTree corrupted= new MerkleTree("data/1_bad.txt");
		ArrayList<Stack<String>> corrupts = corrupted.findCorruptChunks("data/1meta.txt");

		for(Stack<String> stack: corrupts) {
			System.out.println("Corrupt hash stack: "+stack +"\n\n\n");
		}




		download("secondaryPart/data/download_from_trusted.txt");

	}

	public static void downloadFileFromUrl(String link, String path) throws InterruptedException {
		File dir=new File(path.substring(0,path.lastIndexOf("/")));
		dir.mkdirs();
		new Thread(new Download(link, new File(path))).start();
		TimeUnit.MILLISECONDS.sleep(100);//Wait after download, otherwise it gives error.
	}

	public static void download(String path) throws IOException, InterruptedException, NoSuchAlgorithmException {
		// Entry point for the secondary part
		Scanner read = new Scanner(new File(path));
		Queue<String[]> txtQueue = new LinkedList<>();
		while (read.hasNext()) {
			String[] arr = new String[3];
			for (int i = 0; i < 3; i++) {
				arr[i] = read.nextLine();
			}
			txtQueue.add(arr);
			if (read.hasNext())
				read.nextLine();

		}
		String directory = path.substring(0, path.lastIndexOf("/"));
		String savings = "/savings";

		while (!txtQueue.isEmpty()) {
			String[] arr = txtQueue.poll();

			String exampleNo = arr[0].substring(arr[0].lastIndexOf("/"), arr[0].lastIndexOf("m"));
			System.out.println("Example: "+ exampleNo.substring(exampleNo.indexOf("/")+1));

			for (int i = 0; i < 3; i++) {
				String filePath = directory + savings + exampleNo + arr[i].substring(arr[i].lastIndexOf("/"));
				downloadFileFromUrl(arr[i], filePath);
			}
			PrintStream printStream=new PrintStream(new File(directory + savings + exampleNo + exampleNo + "tree.txt"));
			read = new Scanner(new File(directory + savings + exampleNo + exampleNo + ".txt"));
			while (read.hasNext()) {
				String mem = read.nextLine();
				downloadFileFromUrl(mem, directory + "/split" + exampleNo + mem.substring(mem.lastIndexOf("/")));
				printStream.println(directory + "/split" + exampleNo + mem.substring(mem.lastIndexOf("/")));
			}
			printStream.close();
			MerkleTree zero=new MerkleTree(directory + savings + exampleNo + exampleNo + "tree.txt");
			ArrayList<String> corruptPaths=zero.getCorruptPaths(directory + savings + exampleNo + exampleNo + "meta.txt");

			read = new Scanner(new File(directory + savings + exampleNo + exampleNo + "alt.txt"));
			int i=0;
			for(String s:corruptPaths){
				i++;
				System.out.print(i+" . download from other source: ");

				String line=read.nextLine();

				while(! s.substring((s.lastIndexOf("/"))).equals(line.substring(line.lastIndexOf("/")))){
					line=read.nextLine();
				}
				System.out.println(line.substring(line.lastIndexOf("/")));

				downloadFileFromUrl(line,directory + "/split" + exampleNo + line.substring(line.lastIndexOf("/")));

			}
			read.close();
			zero=new MerkleTree(directory + savings + exampleNo + exampleNo + "tree.txt");
			if(zero.checkAuthenticity(directory + savings + exampleNo + exampleNo + "meta.txt"))
				System.out.println("Download completed correctly");
		}


	}


}