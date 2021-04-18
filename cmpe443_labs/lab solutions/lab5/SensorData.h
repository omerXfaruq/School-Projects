#ifndef SENSORDATA_H
#define SENSORDATA_H

#include "LPC407x_8x_177x_8x.h"

#define WINDOW_SIZE 3


/*
Led1 -> 1.18 anot
led2 -> 0.13 anot
led3 -> 1.13 katod
led4 -> 1.30 katod
switch-> 2.8 
*/
#define LED1_PORT_PIN PIN1
#define LED2_PORT_PIN PIN0
#define LED3_PORT_PIN PIN1
#define LED4_PORT_PIN PIN1		
#define Switch_PORT_PIN PIN2		

#define LED1_PORT_DIR DIR1
#define LED2_PORT_DIR DIR0
#define LED3_PORT_DIR DIR1
#define LED4_PORT_DIR DIR1		
#define Switch_PORT_DIR DIR2		

#define LED1_PIN_NO 18
#define LED2_PIN_NO 13
#define LED3_PIN_NO 13
#define LED4_PIN_NO 30		
#define Switch_PIN_NO 8		


#define PIN0 (*((volatile uint32_t *) 0x20098014))
#define DIR0 (*((volatile uint32_t *) 0x20098000))

#define PIN1 (*((volatile uint32_t *) 0x20098034))
#define DIR1 (*((volatile uint32_t *) 0x20098020))

#define PIN2 (*((volatile uint32_t *) 0x20098054))
#define DIR2 (*((volatile uint32_t *) 0x20098040))

#define PIN3 (*((volatile uint32_t *) 0x20098074))
#define DIR3 (*((volatile uint32_t *) 0x20098060))

#define PIN4 (*((volatile uint32_t *) 0x20098094))
#define DIR4 (*((volatile uint32_t *) 0x20098080))

#define PCONP (*((volatile uint32_t*) 0x400FC0C4))
#define SECONDS (1000 * 1000)
	
#define IOCON_P1_18 (*((volatile uint32_t *) 0x4002C0C8))
#define IOCON_P0_13 (*((volatile uint32_t *) 0x4002C034))
#define IOCON_P1_13 (*((volatile uint32_t *) 0x4002C0B4))
#define IOCON_P1_30 (*((volatile uint32_t *) 0x4002C0F8))
#define IOCON_P2_8 (*((volatile uint32_t *) 0x4002C120))


typedef struct {
    volatile uint32_t IR;
    volatile uint32_t TCR;
    volatile uint32_t TC;
    volatile uint32_t PR;
    volatile uint32_t PC;
    volatile uint32_t MCR;
    volatile uint32_t MR0;
    volatile uint32_t MR1;
    volatile uint32_t MR2;
    volatile uint32_t MR3;
    volatile uint32_t CCR;
    volatile uint32_t CR0;
    volatile uint32_t CR1;
    volatile uint32_t reserved1[2];
    volatile uint32_t EMR;
    volatile uint32_t reserved2[12]; 
    volatile uint32_t CTCR;
} TIMER_Typedef;

#define TIMER_0 ((TIMER_Typedef *)(0x40004000)) 
#define TIMER_1 ((TIMER_Typedef *)(0x40008000)) 
#define TIMER_2 ((TIMER_Typedef *)(0x40090000)) 
#define TIMER_3 ((TIMER_Typedef *)(0x40094000)) 
	
#endif
