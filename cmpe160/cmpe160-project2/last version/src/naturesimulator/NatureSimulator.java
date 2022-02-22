package naturesimulator;

import game.Direction;
import game.GridGame;
import project.Creature;
import project.Plant;
import project.Snake;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;


/**
 * Class that implements the game logic for Nature Simulator.
 *
 * IMPORTANT: Please do not modify this class in any way,
 * it will be reset when grading your project.
 */
/**
 * @author Lenovo
 *
 */
public class NatureSimulator extends GridGame {

	Creature newCreature;   //Creature added when food is eaten
	Plant food;		//Food in the game


	private List<Creature> creatures;
	private Creature[][] creaturesMap;

	/**
	 * Creates a new Nature Simulator game instance
	 * @param gridWidth number of grid squares along the width
	 * @param gridHeight number of grid squares along the height
	 * @param gridSquareSize size of a grid square in pixels
	 * @param frameRate frame rate (number of timer ticks per second)
	 */
	public NatureSimulator(int gridWidth, int gridHeight, int gridSquareSize, int frameRate) {
		super(gridWidth, gridHeight, gridSquareSize, frameRate);

		creatures = new ArrayList<>();
		creaturesMap = new Creature[gridWidth][gridHeight];
	}

	/**Creates a food at a random position
	 * 
	 */
	public void addFood() {

		int x=(int)(Math.random()*(getGridWidth()));
		int y=(int)(Math.random()*(getGridHeight()));

		food=new Plant(x,y);
		if(isPositionFree(x, y))
			addCreature(food);
		else
			addFood();
	}

	@Override
	protected void timerTick() {
		//Ýf there is no food add food
		if(food.getHealth()<=0)
			addFood();
		// Determine and execute actions for all creatures
		ArrayList<Creature> creaturesCopy = new ArrayList<>(creatures);


		for (Creature creature : creaturesCopy) {
			if(creature.getPrev()!=null) {	//Ýf creature is not head dont make any action, move has already been made by head.
				continue;
			}
			
			// Choose action
			Action action = creature.chooseAction(createLocalInformationForCreature(creature), food.getX(), food.getY());

			// Execute action
			if (action != null) {
				if (action.getType() == Action.Type.STAY) {
					// STAY
					creature.stay();
				} else if (action.getType() == Action.Type.MOVE) {
					// MOVE
					if (isDirectionFree(creature.getX(), creature.getY(), action.getDirection())) {
						creature.move(action.getDirection());
						update(creature.snakeBody);
					}

				} else if (action.getType() == Action.Type.ATTACK) {
					// ATTACK
					Creature attackedCreature = getCreatureAtDirection(creature.getX(), creature.getY(), action.getDirection());
					if (attackedCreature != null) {
						newCreature=(creature.attack(attackedCreature));	//Will add a new snake to tail
						if (attackedCreature.getHealth() <= 0.0) {
							food.setX(-1);		//Ýf food is eaten other snakes wont move that round
							food.setY(-1);
							removeCreature(attackedCreature);
						}
						// Remove attacked creature if its health is zero
					}
					updateAfterAttack(creature.snakeBody);	//Updates snakes' locations except last added
					addCreature(newCreature);				//Adds added snake to map
					if(creature.snakeBody.size()==8)		//Divides snake into two
						creature.reproduce();
				}
			}		
		}
	}

	/**
	 * Adds a new creature to the game
	 * @param creature creature to be added
	 * @return boolean indicating the success of addition
	 */
	public boolean addCreature(Creature creature) {
		if (creature != null) {
			if (isPositionInsideGrid(creature.getX(), creature.getY())) {
				if (creaturesMap[creature.getX()][creature.getY()] == null) {
					creatures.add(creature);
					addDrawable(creature);
					creaturesMap[creature.getX()][creature.getY()] = creature;
					return true;
				} else {
					return false;
				}
			} else {
				return false;
			}
		}
		return false;
	}	
	/**
	 *Updates snake's whole body
	 *@param List<Snake> snakeBody
	 * 
	 */
	private void update(List<Snake> list) {
		for(int i =0; i<list.size();i++) {
			Creature mem=list.get(i);
			updateCreaturesMap(mem.getOldX(), mem.getOldY(), null);
			updateCreaturesMap(mem.getX(), mem.getY(), mem);
		}

	}
	/**
	 *Updates snake's whole body except last added, last added will be added with addCreature method
	 *@param List<Snake> snakeBody
	 * 
	 */
	private void updateAfterAttack(List<Snake> list) {
		for(int i =0; i<list.size()-1;i++) {
			Creature mem=list.get(i);
			updateCreaturesMap(mem.getOldX(), mem.getOldY(), null);
			updateCreaturesMap(mem.getX(), mem.getY(), mem);
		}

	}


	private void removeCreature(Creature creature) {
		if (creature != null) {
			creatures.remove(creature);
			removeDrawable(creature);
			if (isPositionInsideGrid(creature.getX(), creature.getY())) {
				creaturesMap[creature.getX()][creature.getY()] = null;
			}
		}
	}

	private LocalInformation createLocalInformationForCreature(Creature creature) {
		int x = creature.getX();
		int y = creature.getY();

		HashMap<Direction, Creature> creatures = new HashMap<>();
		creatures.put(Direction.UP, getCreatureAtPosition(x, y - 1));
		creatures.put(Direction.DOWN, getCreatureAtPosition(x, y + 1));
		creatures.put(Direction.LEFT, getCreatureAtPosition(x - 1, y));
		creatures.put(Direction.RIGHT, getCreatureAtPosition(x + 1, y));

		ArrayList<Direction> freeDirections = new ArrayList<>();
		if (creatures.get(Direction.UP) == null && isPositionInsideGrid(x, y - 1)) {
			freeDirections.add(Direction.UP);
		}
		if (creatures.get(Direction.DOWN) == null && isPositionInsideGrid(x, y + 1)) {
			freeDirections.add(Direction.DOWN);
		}
		if (creatures.get(Direction.LEFT) == null && isPositionInsideGrid(x - 1, y)) {
			freeDirections.add(Direction.LEFT);
		}
		if (creatures.get(Direction.RIGHT) == null && isPositionInsideGrid(x + 1, y)) {
			freeDirections.add(Direction.RIGHT);
		}

		return new LocalInformation(getGridWidth(), getGridHeight(), creatures, freeDirections);
	}

	private boolean isPositionInsideGrid(int x, int y) {
		return (x >= 0 && x < getGridWidth()) && (y >= 0 && y < getGridHeight());
	}

	private void updateCreaturesMap(int x, int y, Creature creature) {
		if (isPositionInsideGrid(x, y)) {
			creaturesMap[x][y] = creature;
		}
	}

	private Creature getCreatureAtPosition(int x, int y) {
		if (!isPositionInsideGrid(x, y)) {
			return null;
		}
		return creaturesMap[x][y];
	}

	private Creature getCreatureAtDirection(int x, int y, Direction direction) {
		if (direction == null) {
			return null;
		}
		int xTarget = x;
		int yTarget = y;
		if (direction == Direction.UP) {
			yTarget--;
		} else if (direction == Direction.DOWN) {
			yTarget++;
		} else if (direction == Direction.LEFT) {
			xTarget--;
		} else if (direction == Direction.RIGHT) {
			xTarget++;
		}
		return getCreatureAtPosition(xTarget, yTarget);
	}

	private boolean isPositionFree(int x, int y) {
		return isPositionInsideGrid(x, y) && getCreatureAtPosition(x, y) == null;
	}

	private boolean isDirectionFree(int x, int y, Direction direction) {
		if (direction == null) {
			return false;
		}
		int xTarget = x;
		int yTarget = y;
		if (direction == Direction.UP) {
			yTarget--;
		} else if (direction == Direction.DOWN) {
			yTarget++;
		} else if (direction == Direction.LEFT) {
			xTarget--;
		} else if (direction == Direction.RIGHT) {
			xTarget++;
		}
		return isPositionFree(xTarget, yTarget);
	}

}
