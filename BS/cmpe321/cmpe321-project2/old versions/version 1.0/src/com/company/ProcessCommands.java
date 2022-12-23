package com.company;

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.StringTokenizer;

public class ProcessCommands {
    private String databaseAddress;

    private ArrayList<String> commands;

    private String testOutput;

    private int recordSize = 75;
    private int recordNumInPage = 10;
    private int pageNumInFile = 4;

    public ProcessCommands(String databaseAddress, String output, ArrayList<String> commands) throws FileNotFoundException {
        this.databaseAddress = databaseAddress + "/";
        this.testOutput = output;
        this.commands = commands;
    }

    public void processCommands() {
        for (int i = 0; i < commands.size(); i++) {
            processCommand(commands.get(i));    //Process commands one by one
        }

    }

    private void processCommand(String command) {
        //All operations:

        StringTokenizer tokenizer = new StringTokenizer(command);
        tokenizer.countTokens();
        String commandName1 = tokenizer.nextToken();
        String commandName2 = tokenizer.nextToken();

        if (commandName2.equals("type")) {
            if (commandName1.equals("create")) {
                command1(tokenizer);

            } else if (commandName1.equals("delete")) {
                command2(tokenizer);

            } else if (commandName1.equals("list")) {
                command3(tokenizer);
            }
        } else if (commandName2.equals("record")) {
            if (commandName1.equals("create")) {
                command4(tokenizer);

            } else if (commandName1.equals("delete")) {
                command5(tokenizer);

            } else if (commandName1.equals("update")) {
                command6(tokenizer);

            } else if (commandName1.equals("search")) {
                command7(tokenizer);

            } else if (commandName1.equals("list")) {
                command8(tokenizer);

            }
        }
    }

    private void command1(StringTokenizer command) { //create type
        String typename = command.nextToken();

        System.out.println(typename);
        ArrayList<String> fieldValues = new ArrayList<String>();

        int numberOfFields = Integer.parseInt(command.nextToken());

        System.out.println(numberOfFields);

        String line = typename + " " + numberOfFields;
        for (int i = 0; i < numberOfFields; i++) {
            line += " " + command.nextToken();
        }
        line += " " + 0;

        System.out.println(line);

        //append to txt
        try {
            PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(databaseAddress + "systemcatalogue.txt", true)));
            out.println(line);
            out.close();
        } catch (IOException e) {
            e.printStackTrace();
        }


    }

    private void command2(StringTokenizer command) {//delete type
        String typename = command.nextToken();

        System.out.println("Deleting the type");
        try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(databaseAddress + "replicate.txt", true)))) {
            BufferedReader bufReader = new BufferedReader(new FileReader(databaseAddress + "systemcatalogue.txt"));
            String line;
            StringTokenizer tokenize;
            while ((line = bufReader.readLine()) != null) {
                tokenize = new StringTokenizer(line);
                if (tokenize.nextToken().equals(typename)) {
                    int fieldNumber = Integer.parseInt(tokenize.nextToken());
                    for (int i = 0; i < fieldNumber; i++) {
                        tokenize.nextToken();   //pass field names
                    }
                    int fileNumber = Integer.parseInt(tokenize.nextToken());
                    for (int i = 0; i < fileNumber; i++) {
                        tokenize.nextToken();//pass line number, get the file name and delete it
                        new File(databaseAddress + tokenize.nextToken() + ".txt").delete();
                    }
                } else {
                    out.println(line);
                }
            }
            out.close();
            bufReader.close();
            new File(databaseAddress + "systemcatalogue.txt").delete();
            new File(databaseAddress + "replicate.txt").renameTo(new File(databaseAddress + "systemcatalogue.txt"));

            //new File(databaseAddress + "replicate.txt").delete();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }


    }


    private void command3(StringTokenizer command) {//list type
        System.out.println("Listing all types");

        ArrayList<String> typeNames = new ArrayList<>();
        try (BufferedReader bufReader = new BufferedReader(new FileReader(databaseAddress + "systemcatalogue.txt"))) {


            String line;
            while ((line = bufReader.readLine()) != null) {
                StringTokenizer tokenizer = new StringTokenizer(line);
                typeNames.add(tokenizer.nextToken());
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        Collections.sort(typeNames);
        try (PrintWriter realOutput = new PrintWriter(new BufferedWriter(new FileWriter(testOutput, true)))) {
            for (int i = 0; i < typeNames.size(); i++) {
                realOutput.println(typeNames.get(i));
                System.out.println(typeNames.get(i));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    private void command4(StringTokenizer command) {//create record)//

        String typename = command.nextToken();//Get typename
        System.out.println("Creating a record");
        try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(databaseAddress + "replicate.txt", true)))) {
            BufferedReader bufReader = new BufferedReader(new FileReader(databaseAddress + "systemcatalogue.txt"));
            String fileName = "";
            boolean everyFileIsFull = true;
            boolean increaseFileNumber = false;
            int lineNumber = -1;
            int fileNumber = -1;
            String line;
            int thisFileNumber = -1;

            String newTypeLine = ""; //Edited type line
            StringTokenizer tokenize;
            String fileNames = "";

            String newToken;
            while ((line = bufReader.readLine()) != null) { //Read system catalogue
                tokenize = new StringTokenizer(line);
                if ((newToken = tokenize.nextToken()).equals(typename)) {
                    newTypeLine += newToken + " ";  //creating newTypeLine
                    int fieldNumber = Integer.parseInt(tokenize.nextToken());
                    newTypeLine += fieldNumber + " ";  //add to new type line
                    for (int i = 0; i < fieldNumber; i++) {
                        newTypeLine += tokenize.nextToken() + " ";   //pass field names, and add to newTypeLine
                    }
                    fileNumber = Integer.parseInt(tokenize.nextToken());
                    if (fileNumber == 0) {      // There is no file or record
                        fileNames += "1 " + typename + "1 ";//1 line and name "typename1"
                        increaseFileNumber = true;
                        everyFileIsFull = false;
                        new File(databaseAddress + typename + "1.txt").createNewFile();
                        //append to file
                        try {
                            PrintWriter fileOut = new PrintWriter(new BufferedWriter(new FileWriter(databaseAddress + typename + "1.txt", true)));

                            while (command.hasMoreTokens()) {
                                fileOut.print(command.nextToken() + " ");//Create a new file, and write record to there.
                            }
                            fileOut.println();
                            fileOut.close();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }

                    }
                    for (int i = 0; i < fileNumber; i++) {
                        lineNumber = Integer.parseInt(tokenize.nextToken());//get line number in the file
                        fileName = tokenize.nextToken();
                        if (lineNumber < recordNumInPage * pageNumInFile) {//Add record to file if it is not full
                            lineNumber++;
                            everyFileIsFull = false;
                            //append record to file's last page
                            try {
                                PrintWriter fileOut = new PrintWriter(new BufferedWriter(new FileWriter(databaseAddress + fileName + ".txt", true)));
                                while (command.hasMoreTokens()) {//Append record to file's last page
                                    fileOut.print(command.nextToken() + " ");
                                }
                                fileOut.println();
                                fileOut.close();

                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }
                        fileNames += (lineNumber + " " + fileName + " ");
                    }

                    if (everyFileIsFull) { // Create a new file with increasing number if every file is full
                        increaseFileNumber = true;
                        fileName.replace(typename, "");
                        thisFileNumber = Integer.parseInt(fileName) + 1;
                        File newFile = new File(databaseAddress + typename + thisFileNumber + ".txt");
                        newFile.createNewFile();
                        PrintWriter printFile = new PrintWriter(newFile);
                        while (command.hasMoreTokens()) {//Append record to files first page
                            printFile.print(command.nextToken() + " ");
                        }
                        printFile.close();
                        fileNames += " 1 " + typename + thisFileNumber;
                    }
                    if (increaseFileNumber) { // Type's New line in system catalogue
                        newTypeLine += (fileNumber + 1) + " " + fileNames;
                    } else {
                        newTypeLine += fileNumber + " " + fileNames;
                    }

                } else {
                    out.println(line);//Print different types' lines to new system cat
                }
            }

            out.println(newTypeLine);//Print this type's new line new system cat
            out.close();
            bufReader.close();
            new File(databaseAddress + "systemcatalogue.txt").delete();//Delete old system cat, change name of the new one
            new File(databaseAddress + "replicate.txt").renameTo(new File(databaseAddress + "systemcatalogue.txt"));

        } catch (IOException e) {
            e.printStackTrace();
        }


    }


    private void command5(StringTokenizer command) {//delete record

    }

    private void command6(StringTokenizer command) {//update record
    }

    private void command7(StringTokenizer command) {//search record

    }

    private void command8(StringTokenizer command) {//list record

    }

    private void deleteAllFiles(StringTokenizer files) {
    }


    private String increaseRecordSizeToLimit(String line) {//fix recordSize

        int difference = line.length() - 2 - recordSize;// "\n" holds 2 space
        String additionSpace = " ";
        int spaceLenght = 1;
        while (spaceLenght < difference) {
            if (spaceLenght * 2 < difference) {
                additionSpace = additionSpace + additionSpace;
            } else {
                while (spaceLenght < difference) {
                    additionSpace += " ";
                }
            }
        }
        return line+additionSpace;
    }
}



