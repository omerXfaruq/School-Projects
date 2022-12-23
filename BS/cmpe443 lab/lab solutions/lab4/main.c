#include "LPC407x_8x_177x_8x.h"
#include "SensorData.h"
#include <stdio.h>

/*a = P2.21
b = P3.29
c = P2.8
d = P1.9
e = P3.4
f = P1.25
g = P0.19

Input = P1.3

0: 19
1: 9, 25
2: 8,21
3: 4, 29
*/

//static const uint8_t seven_segment_array[10]= {0x3FU,0x06U,0x5BU,0x4FU,0x66U,0x6DU,0x7DU,0x07U,0x7FU,0x6FU}; //magic_number is ODD


void init() {
	GPIO1->DIR &= ~ (1 << 3);
	
	GPIO0->DIR |= (1 << 19);
	GPIO1->DIR |= (1 << 9 | 1 << 25);
	GPIO2->DIR |= (1 << 21 | 1 << 8 );
	GPIO3->DIR |= (1 << 4 | 1 << 29);
	
	PCONP |= (1<<15);
	
	IOCON_P2_21 &= ~(1<<2|1<<1|1);
	IOCON_P3_29 &= ~(1<<2|1<<1|1);
	IOCON_P2_8 &= ~(1<<2|1<<1|1);
	IOCON_P1_9 &= ~(1<<2|1<<1|1);
	IOCON_P3_4 &= ~(1<<2|1<<1|1);
	IOCON_P1_25 &= ~(1<<2|1<<1|1);
	IOCON_P0_19 &= ~(1<<2|1<<1|1);
	IOCON_P1_3 &= ~(1<<2|1<<1|1);
	
}
void write_to_seven_segment(uint8_t number){    
	if(number <= 5)    
		{       
			GPIO0->PIN &= ~ledKiller[0]; 	
			GPIO0->PIN |= seven_segment0[number];
			
			GPIO1->PIN &= ~ledKiller[1]; 	
			GPIO1->PIN |= seven_segment1[number];
			
			GPIO2->PIN &= ~ledKiller[2]; 	
			GPIO2->PIN |= seven_segment2[number];
			
			GPIO3->PIN &= ~ledKiller[3]; 	
			GPIO3->PIN |= seven_segment3[number];
			
		}
}
	
int main() {
	int second=100000000;
	int f;
	int currentLed=0;
	init();
	
	
	while(1) {
		//Wait 1 sec
		for(f=0;f<second;f++)
		{
		} 
		
		value=(GPIO1->PIN & (1 << 3)) == (1<<3);
		// 0-1 transition
		if(lastValue==0 & value==1)
		{
			lastValue=1;
		}
		
		// 1-0 transition
		if(lastValue==1 & value==0)
		{
			flag = flag != 1; //Switch the flag
			lastValue=value;
		}
		
				
		if(flag)   // Old check (GPIO0->PIN & (1 << 25)) == (1<<25) )
			{
				write_to_seven_segment(currentLed);
				currentLed++;
				currentLed= currentLed % 6;
			}
		else
		{
				currentLed=0;
				write_to_seven_segment(currentLed);
		}
	}
}
