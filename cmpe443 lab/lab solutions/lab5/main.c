#include "LPC407x_8x_177x_8x.h"
#include "SensorData.h"
#include <stdio.h>

//LED 1 & 2 are anot

//matcher pin P2.4
//Toggle
//T2_MAT1

//LED4 = P1.30
//Push Button = P2.8

void wait1Second();
void turn_on_led();

void init() {
	IOCON_P1_18 &= ~(1<<2|1<<1|1);
	IOCON_P0_13 &= ~(1<<2|1<<1|1);
	IOCON_P1_13 &= ~(1<<2|1<<1|1);
	IOCON_P1_30 &= ~(1<<2|1<<1|1);
	IOCON_P2_8 &= ~(1<<2|1<<1|1);

	
	LED1_PORT_PIN |= (1<< LED1_PIN_NO);  //Set as output
	LED2_PORT_PIN |= (1<< LED2_PIN_NO);  //Set as output
	LED3_PORT_PIN |= (1<< LED3_PIN_NO);  //Set as output
	LED4_PORT_PIN |= (1<< LED4_PIN_NO);  //Set as output
	Switch_PORT_DIR |= (1<< Switch_PIN_NO);  //Set as input
	
	//Initial state
	//Turn on LED1
	turn_on_led(1);
  
	//Use pconp to power up timer
	PCONP |= (1 << 22); //TIMER #2 
	
	
  TIMER_2->TCR = 2;		//Reset bit 1 enable bit 0
	TIMER_2->PR = 59;			//decrease it to 1MHz from 60MHz

	TIMER_2->MCR = (1 << 4);	//Reset feature for TC with MR1, 
	TIMER_2->EMR = (3 << 6);	//Toggle for MR1, 

	TIMER_2->TCR = 1;    //enable bit 1 reset bit 0 
	
}

void wait1Second(){
	TIMER_2->TC =0;
	TIMER_2->MR1= SECONDS;
	while(TIMER_2->TC < TIMER_2->MR1);
}

//anot
void openLed1()
{
	LED1_PORT_PIN &= ~(1<<LED1_PIN_NO);

}
void closeLed1()
{
	LED1_PORT_PIN |= (1<<LED1_PIN_NO);
}

//anot
void openLed2()
{
	LED2_PORT_PIN &= ~(1<<LED2_PIN_NO);

}
void closeLed2()
{
	LED2_PORT_PIN |= (1<<LED2_PIN_NO);
}

//katod
void openLed3()
{
	LED3_PORT_PIN |= (1<<LED3_PIN_NO);

}
void closeLed3()
{
	LED3_PORT_PIN &= ~(1<<LED3_PIN_NO);
}

//katod
void openLed4()
{
	LED4_PORT_PIN |= (1<<LED4_PIN_NO);

}
void closeLed4()
{
	LED4_PORT_PIN &= ~(1<<LED4_PIN_NO);
}

void turn_on_led(int ledNo){
	closeLed1();
	closeLed2();
	closeLed3();
	closeLed4();
	if (ledNo==1){
		openLed1();
	}
	else if (ledNo==2){
		openLed2();
	}
	else if (ledNo==3){
		openLed3();
	}
	else if (ledNo==4){
		openLed4();
	}
}

int main() {
	
	int numberOfSwitchChanges=0;
	int flag=0;
	int value=0;
	int lastValue=0;
	int f;
	int currentLed=0;
	init();
	
	
	while(1) {
		//Wait 1 sec
		wait1Second();
		
		
		//Checking button!!
		value=(Switch_PORT_PIN & (1 << Switch_PIN_NO )) == (1<<Switch_PIN_NO);
		if(lastValue==0 & value==1)
		{
			lastValue=1;
		}
		
		if(lastValue==1 & value==0)//Button is pressed
		{
			flag = flag != 1; //Switch the flag
			lastValue=value;
		}
		
				
		if(flag)// traverse LED1-LED2...
			{
				turn_on_led(currentLed+1);
				currentLed++;
				currentLed= currentLed % 4;
			}
		else//Stay at LED1
		{
				currentLed=0;
				turn_on_led(currentLed+1);
		}
	}
}
