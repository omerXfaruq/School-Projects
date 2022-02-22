import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;

public class storageManager {

    public static void main(String[] args) throws IOException {
        String line;

        new File("outputttt.txt").delete();
        File d = new File("database");
        d.mkdirs();
        File l = new File("database/systemcatalogue.txt");
        l.createNewFile();

		String myInput=args[0];
		String myOutput=args[1];

        Scanner inputScanner = new Scanner(new File(myInput));// Reads input and saves commands
        ArrayList<String> commands = new ArrayList<String>();
        while (inputScanner.hasNextLine()) {
            String stringline = inputScanner.nextLine();


            System.out.println(stringline);


            commands.add(stringline);
        }
        inputScanner.close();
        BufferedReader bufferedReader = new BufferedReader(new FileReader("database/systemCatalogue.txt"));
        while ((line = bufferedReader.readLine()) != null) {
            System.out.println(line);
        }
        bufferedReader.close();

        ProcessCommands work = new ProcessCommands("database", myOutput, commands);
        work.processCommands();

    }
}
