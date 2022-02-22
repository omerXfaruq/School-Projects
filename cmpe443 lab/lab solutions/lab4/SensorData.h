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

/*a = P2.21
b = P3.29
c = P2.8
d = P1.9
e = P3.4
f = P1.25
g = P0.19

Input = P1.3

*/
#define GPIO_base 0x20098000
#define GPIO0 ((GPIO_Type *)(GPIO_base)) //0x20098000
#define GPIO1 ((GPIO_Type *)(GPIO_base + 0x020)) //0x20098020
#define GPIO2 ((GPIO_Type *)(GPIO_base + 0x040)) //0x20098020
#define GPIO3 ((GPIO_Type *)(GPIO_base + 0x060)) //0x20098020

#define PCONP (*((volatile uint32_t *) 0x400FC0C4))

#define IOCON_P2_21 (*((volatile uint32_t *) 0x4002C154))
#define IOCON_P3_29 (*((volatile uint32_t *) 0x4002C1F4))
#define IOCON_P2_8 (*((volatile uint32_t *) 0x4002C120))
#define IOCON_P1_9 (*((volatile uint32_t *) 0x4002C0A4))
#define IOCON_P3_4 (*((volatile uint32_t *) 0x4002C190))
#define IOCON_P1_25 (*((volatile uint32_t *) 0x4002C0E4))
#define IOCON_P0_19 (*((volatile uint32_t *) 0x4002C04C))
#define IOCON_P1_3 (*((volatile uint32_t *) 0x4002C08C))

static const uint32_t seven_segment0[6]= {0x80000U, 0x80000U, 0x0U, 						0x0U, 0x80000U, 0x80000U};
static const uint32_t seven_segment1[6]= {0x2000000U, 0x2000200U, 0x2000200U, 0x2000200U, 0x2000200U, 0x2000000U};
static const uint32_t seven_segment2[6]= {0x200100U, 0x200100U, 0x200000U, 0x200100U, 0x200000U, 0x200000U};
static const uint32_t seven_segment3[6]= {0x20000010U, 0x20000010U, 0x10U, 0x20000010U, 0x10U, 0x10U};

static const uint32_t ledKiller[4]= {0x80000U,0x2000200U,0x200100U,0x20000010U}; //Kill all the leds

int flag=0;
int lastValue=0;
int value=0;
int numberOfSwitchChanges=0;
//#define PIN0 (*((volatile uint32_t *) 0x20098014))
//#define DIR0 (*((volatile uint32_t *) 0x20098000))

#endif
