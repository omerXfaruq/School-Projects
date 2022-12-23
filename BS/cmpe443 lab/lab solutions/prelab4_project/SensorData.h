#ifndef SENSORDATA_H
#define SENSORDATA_H
#include "LPC407x_8x_177x_8x.h"

typedef struct{   
volatile uint32_t DIR;            
uint32_t reserved[3];   
volatile uint32_t MASK;   
volatile uint32_t PIN;   
volatile uint32_t SET;   
volatile uint32_t CLR;}
GPIO_Type;

#define GPIO_base 0x20098000
#define GPIO0 ((GPIO_Type *)(GPIO_base)) //0x20098000
#define GPIO1 ((GPIO_Type *)(GPIO_base + 0x020)) //0x20098020

#define PCONP (*((volatile uint32_t *) 0x400FC0C4))

#define IOCON_P0_25 (*((volatile uint32_t *) 0x4002C064))
#define IOCON_P1_5 (*((volatile uint32_t *) 0x4002C094))
#define IOCON_P1_6 (*((volatile uint32_t *) 0x4002C098))
#define IOCON_P1_7 (*((volatile uint32_t *) 0x4002C09C))
#define IOCON_P1_11 (*((volatile uint32_t *) 0x4002C0AC))
#define IOCON_P1_3 (*((volatile uint32_t *) 0x4002C08C))
#define IOCON_P1_23 (*((volatile uint32_t *) 0x4002C0DC))
#define IOCON_P1_24 (*((volatile uint32_t *) 0x4002C0E0))

static const uint32_t seven_segment[10]= {0x1000000U, 0x10008e0U, 0x800080U, 0x800008U, 0x828U, 0x48U, 0x40U, 0x1800808U, 0x0U, 0x8U};
static const uint32_t ledKiller= 0x18008e8; //Kill all the leds

int flag=0;
int lastValue=0;
int value=0;
int numberOfSwitchChanges=0;
//#define PIN0 (*((volatile uint32_t *) 0x20098014))
//#define DIR0 (*((volatile uint32_t *) 0x20098000))

#endif
