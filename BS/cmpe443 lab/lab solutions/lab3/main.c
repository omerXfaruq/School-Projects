#include "LPC407x_8x_177x_8x.h"
#include "SensorData.h"
#include <stdio.h>

//2.18 LED 1  
//2.27 LED 2  turns on with 1, others turns with 0
//2.23 LED 3
//4.8 LED 3

void init() {
	DIR2 |= (1<<18);  //Set as output
	DIR2 |= (1<<27);  //Set as output
	DIR2 |= (1<<23);  //Set as output
	DIR4 |= (1<<8);  //Set as output

	//Initial state
	//Turn off P_2.18, 
	//Turn on LED1
	PIN2 &= ~(1<<18); 
	
	//Turn off LED2, 
	PIN2 &= ~(1<<27);

	//Turn off LED3
	PIN2 |= (1<<23);
	//Turn off LED4
	PIN4 |= (1<<8);
}

void update() {
	int f;
	int second=300000000;
	
	//Turn on LED1
	PIN2 &= ~(1<<18); 
	//Wait 1 sec
	for(f=0;f<second;f++); 
  //Turn off LED1
	PIN2 |= (1<<18);
	
	//Turn on LED2	
	PIN2 |= (1<<27); 
	//Wait 1 sec
	for(f=0;f<second;f++);
	//Turn off LED2
	PIN2 &= ~(1<<27);
	
	//Turn on LED3	
	PIN2 &= ~(1<<23);
	//Wait 1 sec
	for(f=0;f<second;f++);
	//Turn off LED3
	PIN2 |= (1<<23);
	
	//Turn on LED4	
	PIN4 &= ~(1<<8);
	//Wait 1 sec
	for(f=0;f<second;f++);
	//Turn off LED4
	PIN4 |= (1<<8);

	
}

int main() {
	int f;
	init();

	while(1) {
		update();
	}
}
