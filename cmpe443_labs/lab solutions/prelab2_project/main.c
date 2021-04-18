#include "LPC407x_8x_177x_8x.h"
#include "SensorData.h"
#include <stdio.h>

sensor_data_t filteredSensorData[dataSize];
//Note that after doing the lates build these are the code sizes:
//O0:1476
//O1:1192
//O2:972
//O3:972

int TruthValue=-1;
//void * PORT1= 0x4002C0F8;
//void * PORT1= 0x4002C0F8;
void swap(int *p,int *q) {
   int t;
   
   t=*p; 
   *p=*q; 
   *q=t;
}

void sort(int a[],int n) { 
   int i,j,temp;

   for(i = 0;i < n-1;i++) {
      for(j = 0;j < n-i-1;j++) {
         if(a[j] > a[j+1])
            swap(&a[j],&a[j+1]);
      }
   }
}

int findAverage(int a[],int n){
	int i,j;
	int sum;
  for(i = 0;i < n;i++) {
		sum+=a[i];
	 }
	sum = sum/n;
	 return sum;
}


//int WINDOW_SIZE=5;
int temporaryArray[WINDOW_SIZE];
int temporaryArrayForAverage[WINDOW_SIZE];

void medianFilter(const sensor_data_t* data, sensor_data_t* result, uint32_t size) {
	int i,j,f,average;
	for(i=0;i<WINDOW_SIZE-1;i++)
	{
		result[i]=data[i];
	}
	
	for(i=WINDOW_SIZE-1;i<size;i++)
	{
		int currentIndex=0;
		for(j=i-WINDOW_SIZE+1;j<i+1;j++)
		{
			//Take last WINDOW_SIZE elements into temporary arrays
			temporaryArray[currentIndex]=data[j];
			temporaryArrayForAverage[currentIndex]=data[j];
			currentIndex++;
		}
		//Sort
		sort(temporaryArray,WINDOW_SIZE);
		//Calculate median
		if(WINDOW_SIZE % 2)
		{//Odd SET
			result[i]=temporaryArray[WINDOW_SIZE/2];
		}
		else
		{//Even set
			result[i]=1/2*(temporaryArray[WINDOW_SIZE/2] + temporaryArray[WINDOW_SIZE/2 -1]);
		}
		
		average=findAverage(temporaryArrayForAverage,WINDOW_SIZE);
		if( average >= 150/100*result[i]){ 
			//Turn on the LED
			PIN1 |= (1<<30);
			TruthValue=1;
		}
		else{
			//Turn off the Led
			PIN1 &= ~(1<<30);
			TruthValue=0;
		}
		for(f=0;f<1000*2;f++); //Wait 2 sec

	}
	//Wait in for loop
	for(f=0;f<1000*2;f--); //Wait infinitely
}


void init() {
	DIR1 |= (1<<30);  //Set as output
}

void update() {
	medianFilter(sensorData, filteredSensorData, dataSize);
}

int main() {
	int f;
	init();

	while(1) {
		for(f=0;f<1000*2;f++); //Wait 2 sec
		update();
	}
}
