package project;

import java.awt.Color;
import game.Direction;
import naturesimulator.Action;
import naturesimulator.LocalInformation;
import naturesimulator.Action.Type;
import ui.GridPanel;


public class Plant extends Creature {

	/**Constructs a plant
	 * @param x
	 * @param y
	 */
	public Plant(int x, int y) {  
		super(x, y, 1);
	}

	/* Draw the Plant
	 * @param panel
	 */
	@Override
	public void draw(GridPanel panel) {   //Draw Plant according to health
		panel.drawSquare(x, y, Color.GREEN);
	} 

	/* Food doesn't choose action, return stay;
	 * @param information
	 * @return Action
	 */
	@Override		
	public Action chooseAction(LocalInformation information, int foodX, int foodY) {		//Chooses action according to rules
		return new Action(Type.STAY);
	}
	/* 
	 * Empty method, does not happen
	 */
	@Override
	public void stay() {    		
	}

	/* Empty method, does not happen
	 */
	@Override
	public void reproduce(){    
	}
	/* Empty method, does not happen
	 * @param target
	 */
	@Override
	public Creature attack(Creature target) {  //Will not ever work in plant
		return null;
	}
	/* Empty method, does not happen
	 * @param direction
	 */
	@Override
	public void move(Direction direction) {  //Will not ever work in plant

	}


}
