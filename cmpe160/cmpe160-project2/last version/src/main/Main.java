package main;

import naturesimulator.NatureSimulator;
import project.Snake;
import project.Plant;
import ui.ApplicationWindow;

import java.awt.*;


/**
 * The main class that can be used as a playground to test your project.
 * This class will be discarded and replaced with our own grading class.
 *
 * IMPORTANT: All the classes that you create should be put under the package named "project".
 * All the other packages will be reset when grading your project.
 */
public class Main {

	/**
	 * Main entry point for the application.
	 *
	 * IMPORTANT: You can change anything in this method to test your game,
	 * but your changes will be discarded when grading your project.
	 *
	 * @param args application arguments
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(() -> {
			try {
				// Create game
				// You can change the world width and height, size of each grid square in pixels or the game speed
				NatureSimulator game = new NatureSimulator(130,70, 10,1000);

				//Creates snakes, and snakes' bodies and add them
				Snake[] snake= new Snake[4];
				for(int i=0;i<4;i++) {
					snake[i]=new Snake(1+i,1);
				}
				for(int i=0;i<3;i++)
					snake[i+1].setPrev(snake[i]);
				for(int i =0;i<4;i++) {
					for(int j=0;j<4;j++)
						snake[i].snakeBody.add(snake[j]);
					game.addCreature(snake[i]);

				}
				//Adds food
				game.addFood();
			

				// Create application window that contains the game panel
				ApplicationWindow window = new ApplicationWindow(game.getGamePanel());
				window.getFrame().setVisible(true);

				// Start game
				game.start();

			} catch (Exception e) {
				e.printStackTrace();
			}
		});
	}

}
