#ifndef SENSORDATA_H
#define SENSORDATA_H

#include "LPC407x_8x_177x_8x.h"

#define WINDOW_SIZE 3

#define PIN0 (*((volatile uint32_t *) 0x20098014))
#define DIR0 (*((volatile uint32_t *) 0x20098000))

#define PIN1 (*((volatile uint32_t *) 0x20098034))
#define DIR1 (*((volatile uint32_t *) 0x20098020))

#define PIN2 (*((volatile uint32_t *) 0x20098054))
#define DIR2 (*((volatile uint32_t *) 0x20098040))

#define PIN4 (*((volatile uint32_t *) 0x20098094))
#define DIR4 (*((volatile uint32_t *) 0x20098080))

	
#endif
