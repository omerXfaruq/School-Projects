package project;

import java.awt.Color;
import java.util.*;
import game.Direction;
import naturesimulator.Action;
import naturesimulator.LocalInformation;
import naturesimulator.Action.Type;
import ui.GridPanel;

public class Snake extends Creature {
	private Snake previous=null;

	private static final Color DARK_RED = new Color(204, 0, 0);            //New colors for snake's body
	private static final Color VERY_DARK_RED = new Color(153, 0, 0);
	private static final Color VERY_LIGHT_RED = new Color(255, 102, 102);
	private static final Color LIGHT_RED=new Color(255,51,51);
	private static final Color VERY_VERY_LIGHT_RED=new Color(255,153,153);
	private static final Color VERY_VERY_VERY_LIGHT_RED=new Color(255,204,204);

	/**Sets snake's previous
	 * @param snake
	 */
	public void setPrev(Snake snake) {
		previous=snake;
	}

	public Snake getPrev() {
		return previous;
	}

	/**Constructor
	 * @param x
	 * @param y
	 */
	public Snake(int x, int y) {		    
		super(x, y, 1);
		oldX=x;
		oldY=y;
	}


	/*Draws Snake's parts according to position 
	 *@param panel			

	 */
	@Override
	public void draw(GridPanel panel) {  	 
		if(previous==null)	//Head
			panel.drawSquare(x, y, Color.BLUE);
		else if(previous.previous==null)
			panel.drawSquare(x, y, VERY_DARK_RED);
		else if(previous.previous.previous==null)
			panel.drawSquare(x, y, DARK_RED);
		else if(previous.previous.previous.previous==null)
			panel.drawSquare(x, y, Color.RED);
		else if(previous.previous.previous.previous.previous==null)
			panel.drawSquare(x, y, LIGHT_RED);
		else if(previous.previous.previous.previous.previous.previous==null)
			panel.drawSquare(x, y, VERY_LIGHT_RED);
		else if(previous.previous.previous.previous.previous.previous.previous==null)
			panel.drawSquare(x, y, VERY_VERY_LIGHT_RED);
		else
			panel.drawSquare(x, y, VERY_VERY_VERY_LIGHT_RED);

	}

	/* Action picker, brain of the creature
	 * Move to to food
	 * if not possible move randomly
	 * if not possible stay 
	 *
	 * @param information
	 * @return action
	 */
	@Override
	public Action chooseAction(LocalInformation information, int foodX, int foodY) {  	//Chooses action according to the rules
		if(previous!=null)   //Ýf it is not head don't choose any action.
			return null;
		else if(foodX==-1 || foodY==-1) {  //Stay if food is eaten that round
			return new Action(Type.STAY); }
		else if(information.getCreatureDown() instanceof Plant || information.getCreatureUp() instanceof Plant ||  //Check if there is a food nearby
				information.getCreatureLeft() instanceof Plant || information.getCreatureRight() instanceof Plant) {
			return new Action(Type.ATTACK, randomPlantDirection(information));}  //Eat the food
		else if(! directionsToFood(information,foodX,foodY).isEmpty()) {		//Check if it can go in the food way
			return new Action(Type.MOVE,LocalInformation.getRandomDirection(directionsToFood(information,foodX,foodY)));}  //Random move to food
		else if(! information.getFreeDirections().isEmpty()) {		//Random move is available
			return new Action(Type.MOVE , LocalInformation.getRandomDirection(information.getFreeDirections()));} //Random move
		else {
			return new Action(Type.STAY);}		//Stay

	}
	/**@param information
	 * @param x
	 * @param y
	 * @return List<Direction> available directions to food
	 */
	private List<Direction> directionsToFood(LocalInformation information, int x, int y) {
		List<Direction> directions=new ArrayList<Direction>();
		if(this.x<x && information.getFreeDirections().contains(Direction.RIGHT))
			directions.add(Direction.RIGHT);
		if(this.x>x && information.getFreeDirections().contains(Direction.LEFT))
			directions.add(Direction.LEFT);
		if(this.y<y && information.getFreeDirections().contains(Direction.DOWN))
			directions.add(Direction.DOWN);
		if(this.y>y && information.getFreeDirections().contains(Direction.UP))
			directions.add(Direction.UP);
		return directions;
	}
	/**
	 * @param information
	 * @return a random plant direction
	 */
	private Direction randomPlantDirection(LocalInformation information){		
		List<Direction> directions=new ArrayList<Direction>();
		if(information.getCreatureDown() instanceof Plant) {
			directions.add(Direction.DOWN);
		}
		if(information.getCreatureUp() instanceof Plant) {
			directions.add(Direction.UP);
		}
		if(information.getCreatureLeft() instanceof Plant) {
			directions.add(Direction.LEFT);
		}
		if(information.getCreatureRight() instanceof Plant) {
			directions.add(Direction.RIGHT);
		}
		return LocalInformation.getRandomDirection(directions);

	}
	/* Stays, does nothing
	 * 
	 */
	@Override
	public void stay() {
	}
	/* Reproduces, divides into two.
	 */
	@Override
	public void reproduce() {  
		Snake []temp= new Snake[9];
		temp[8]=null;
		for(int i=0;i<8;i++) 
			temp[i]=snakeBody.get(i);

		for(int i=0;i<8;i++)
			temp[i].snakeBody=new LinkedList<Snake>();

		for(int i=0;i<4;i++) {
			for(int j=0;j<4;j++)
				temp[i].snakeBody.add(temp[j]);
		}
		for(int i=4;i<8;i++) {
			temp[i].previous=temp[i+1];
			for(int j=7;j>3;j--)
				temp[i].snakeBody.add(temp[j]);
		}

	}
	/* Attacks to food and eat it,
	 * add a new pixel to tail
	 * Make food's health 0
	 * 
	 * @param target Attack target
	 * @return Creature Snake added to tail
	 */
	@Override
	public Creature attack(Creature target) {

		Snake snake= new Snake(snakeBody.get(snakeBody.size()-1).x ,snakeBody.get(snakeBody.size()-1).y);  //Create a new snake point for tail
		updateTillTail();
		oldX=x;
		oldY=y;
		x=target.x;
		y=target.y;
		snakeBody.add(snake);
		snake.snakeBody.add(this);
		for(int i=1;i<snakeBody.size()-1;i++) {
			snakeBody.get(i).snakeBody.add(snake);
			snake.snakeBody.add(snakeBody.get(i));
		}
		snake.snakeBody.add(snake);
		snake.previous=snakeBody.get(snakeBody.size()-2);

		target.health=0;

		return snake;

	}

	/* Move every snake point to previous snake point, 
	 *  and move head according to the direction
	 * @param direction
	 */
	@Override
	public void move(Direction direction) {     
		updateTillTail();
		oldX=x;
		oldY=y;
		if (direction == Direction.UP)
			y = y - 1;
		if (direction == Direction.DOWN)
			y = y + 1;
		if (direction == Direction.LEFT)
			x = x - 1;
		if (direction == Direction.RIGHT)
			x = x + 1;

	}
	/* Tail follows the head
	 */
	private void updateTillTail() {
		for(int i=snakeBody.size()-1;i>0;i--) {
			snakeBody.get(i).oldX=(snakeBody.get(i).x);
			snakeBody.get(i).x=(snakeBody.get(i).previous.x);

			snakeBody.get(i).oldY=(snakeBody.get(i).y);
			snakeBody.get(i).y=(snakeBody.get(i).previous.y);			
		}
	}
}

