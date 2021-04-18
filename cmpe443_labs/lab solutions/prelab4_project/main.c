#include "LPC407x_8x_177x_8x.h"
#include "SensorData.h"
#include <stdio.h>

//2.18 LED 1  
//2.27 LED 2  turns on with 1, others turns with 0
//2.23 LED 3
//4.8 LED 3
/*
a, 		b,		c,		d,			e,		f,		g
P1.5, P1.6, P1.7, P1.11, P1.3, P1.23, P1.24
P0.25 -> push button

*/
//static const uint8_t seven_segment_array[10]= {0x3FU,0x06U,0x5BU,0x4FU,0x66U,0x6DU,0x7DU,0x07U,0x7FU,0x6FU}; //magic_number is ODD


void init() {
	GPIO0->DIR &= ~ (1 << 25);
	GPIO1->DIR |= (1 << 24 | 1 << 23 | 1 << 3 | 1 << 11 | 1 << 7 | 1 << 6 | 1 << 5);
	
	PCONP |= (1<<15);
	IOCON_P0_25 &= ~(1<<2|1<<1|1);
	IOCON_P1_5 &= ~(1<<2|1<<1|1);
	IOCON_P1_6 &= ~(1<<2|1<<1|1);
	IOCON_P1_7 &= ~(1<<2|1<<1|1);
	IOCON_P1_11 &= ~(1<<2|1<<1|1);
	IOCON_P1_3 &= ~(1<<2|1<<1|1);
	IOCON_P1_23 &= ~(1<<2|1<<1|1);
	IOCON_P1_24 &= ~(1<<2|1<<1|1);
}
void write_to_seven_segment(uint8_t number){    
	if(number <= 9)    
		{       
			GPIO1->PIN &= ~ledKiller; 	
			GPIO1->PIN |= seven_segment[number];
		}
}
	
int main() {
	int second=300000000;
	int f;
	int currentLed=0;
	init();
	
	
	while(1) {
		//Wait 1 sec
		for(f=0;f<second;f++)
		{
		} 
		
		value=(GPIO0->PIN & (1 << 25)) == (1<<25);
		if(lastValue==0 & value==1)
		{
			lastValue=1;
		}
		
		if(lastValue==1 & value==0)
		{
			flag = flag != 1; //Switch the flag
			lastValue=value;
		}
		
				
		if(flag)   // Old check (GPIO0->PIN & (1 << 25)) == (1<<25) )
			{
				write_to_seven_segment(currentLed);
				currentLed++;
				currentLed= currentLed % 10;
			}
		else
		{
				currentLed=0;
				write_to_seven_segment(currentLed);
		}
	}
}
