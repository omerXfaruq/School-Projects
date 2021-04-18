#ifndef SENSORDATA_H
#define SENSORDATA_H

#include "LPC407x_8x_177x_8x.h"

#define WINDOW_SIZE 3
#define PIN1 (*((volatile uint32_t *) 0x20098034))
#define DIR1 (*((volatile uint32_t *) 0x20098020))
	
typedef int32_t sensor_data_t;

const uint32_t dataSize = 20;
const sensor_data_t sensorData[] = {12,17,19,15,1,5,8,7,5,2,3,10,9,5,100,11,9,14,7,19 };
	
#endif
