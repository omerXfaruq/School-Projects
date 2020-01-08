package project;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import game.Direction;
import game.Drawable;
import naturesimulator.Action;
import naturesimulator.LocalInformation;
import ui.GridPanel;

public abstract class Creature implements Drawable {
	public List<Snake> snakeBody = new ArrayList<Snake>(); // SnakeBody
	protected double health;
	protected int x, y, oldX, oldY; // oldX, oldY is used for updating positions

	/**Constructor
	 * @param x
	 * @param y
	 * @param health
	 */
	public Creature(int x, int y, double health) { 
		this.x = x;
		this.y = y;
		this.health = health;
	}

	/**Returns the previous snake in the snakeBody
	 * @return Snake previous
	 */
	public Snake getPrev() { // Getter for previous, checks if creature is head or not
		return null; // Overwritten in snake subclass
	}				//Plant class always returns null

	/**
	 * Getter for health
	 * 
	 * @return health
	 */
	public double getHealth() { // Health getter
		return health;
	}

	/**
	 * Getter for x
	 * 
	 * @return x position
	 */
	public int getX() { // x getter
		return x;
	}

	/**
	 * @return oldX
	 */
	public int getOldX() {
		return oldX;
	}

	/**
	 * @return oldY
	 */
	public int getOldY() {
		return oldY;
	}

	/**
	 * Getter for y
	 * 
	 * @return y position
	 */
	public int getY() { // y getter
		return y;
	}

	/**Setter for x
	 * @param x
	 */
	public void setX(int x) {
		this.x = x;
	}

	/**Setter for y
	 * @param y
	 */
	public void setY(int y) {
		this.y = y;
	}

	/**
	 * Stays
	 * 
	 */
	public abstract void stay(); // Overwritten in subclasses

	/**
	 * Reproduces, divides snake into two
	 * @param direction
	 */
	public abstract void reproduce(); // Overwritten in subclasses

	/**
	 * Attacks to the target
	 * 
	 * @param target
	 */
	public abstract Creature attack(Creature target); // Overwritten in subclasses

	/**Moves to the direction
	 * @param direction
	 */
	public abstract void move(Direction direction); // Overwritten in subclasses

	/**
	 * Chooses action
	 * 
	 * @param information,
	 *            food x position, food y position
	 * @return action
	 */
	public abstract Action chooseAction(LocalInformation information, int foodX, int foodY); // Overwritten in
																								// subclasses

	/*
	 * (non-Javadoc)
	 * 
	 * @see game.Drawable#draw(ui.GridPanel)
	 */
	public abstract void draw(GridPanel panel); // Overwritten in subclasses

}
