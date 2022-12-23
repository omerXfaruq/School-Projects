import java.util.Scanner;

public class OFO2016400048{
	public static Scanner console = new Scanner(System.in); //Scanner in the whole code

	//This method does first actions asking age, position and returns for which position user is applying.
	public static String introduction() {
		System.out.println("What is your name?");
		String name = console.nextLine();
		System.out.println("Hello " + name + ". How old are you?");
		int age = console.nextInt();
		if (age > 17) {
			System.out.println("We are searching for Software Engineer, Accountant, Academic. For which position are you applying?");
			console.nextLine();//Eats the line after nextInt and fixes an error.
			return console.nextLine();
		} else {
			System.out.println("Unfortunately our company only accepts people who are older than 18. Good bye.");
			return "ageissue";
		}
	}

	public static int testline(String question,String answer,String wrongAnswer) {
		System.out.println(question);
		String flag=console.nextLine();
		while(!flag.equalsIgnoreCase(answer)&&!flag.equalsIgnoreCase(wrongAnswer)){
			System.out.println("Please enter one of possible answers");
			flag=console.nextLine();
		}
		if (flag.equalsIgnoreCase(answer)) {
			return 1;
		} else
			return 0;
	}

	//This method asks a question and tests if it is bigger than the given input.
	public static int testnumber(String question, int min) {
		System.out.println(question);
		if (console.nextInt() >= min) {
			console.nextLine();//Eats the line after nextInt and fixes an error.
			return 1;
		} else 
			return 0;
			}

	public static void accepted() {
		System.out.println("Congratulations you got the job.");
	}

	public static void declined() {
		System.out.println("Unfortunately you are not qualified for this job. Good bye.");
	}

	//This method asks gender and military service
	public static void maleOrNot() {
		if (testline("Are you male?(Yes/No)", "Yes","No") == 1) {
			if (testline("Have you done your military service?(Yes/No)", "Yes","No") == 1) {
				accepted();
			} else declined();
		} else accepted();
	}

	//This method asks questions for Software Engineer.
	public static void Software() {
		if (testline("Do you have a university degree on Software Engineering or Computer Engineering or Computer Science?(Yes/No)", "Yes","No") == 1) {
			if (testnumber("Very good. Then how many programming languages do you know?", 2) == 1) {
				if (testline("Do you have 3 years of Software Engineering experience or Software Engineer graduate degree?(Yes/No)", "Yes","No") == 1) {
					maleOrNot();
				} else declined();
			} else declined();
		} else declined();
	}

	//This method asks questions for Accountant.
	public static void Accountant() {
		if (testline("Do you have Accountant degree?(Yes/No)", "Yes","No") == 1) {
			if (testline("Do you know excel well?(Yes/No)", "Yes","No") == 1) {
				if (testline("Do you know fluent english or do you have a friend who can translate it for you?(Yes/No)", "Yes","No") == 1) {
					if (testnumber("How many people do you know working in the company?", 2) == 1) {
						if (testline("Do you have driving license?(Yes/No)", "Yes","No") == 1) {
							maleOrNot();
						} else declined();
					} else declined();
				} else declined();
			} else declined();
		} else declined();
	}

	//This method asks questions for Academic.
	public static void Academic() {
		if (testline("Do you speak english?(Yes/No)", "Yes","No") == 1) {
			if (testnumber("How many papers have you published?", 3) == 1) {
				if (testline("Do you love to teach?(Definitely/Not quite)", "Definitely","Not quite") == 1) {
					maleOrNot();
				} else declined();
			} else declined();
		} else declined();
	}

	public static void main(String[] args) {
		String position = introduction();
		if (position.equalsIgnoreCase("Software engineer")) {
			Software();
		} else if (position.equalsIgnoreCase("Accountant")) {
			Accountant();
		} else if (position.equalsIgnoreCase("Academic")) {
			Academic();
		} else if (position.equals("ageissue")) {
			System.out.println();
		} else {
			System.out.println("Unfortunately we are just recruiting Software Engineer, Accountant, Academic.");
		}
	}
}


