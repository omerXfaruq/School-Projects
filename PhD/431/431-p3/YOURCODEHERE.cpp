#include <iostream>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <sys/stat.h>
#include <unistd.h>
#include <algorithm>
#include <fstream>
#include <map>
#include <math.h>
#include <fcntl.h>
#include <vector>
#include <iterator>
#include <cmath>
#include "431project.h"

using namespace std;

/*
 * Enter your PSU IDs here to select the appropriate scanning order.
 */
#define PSU_ID_SUM (929765036)

/*
 * Some global variables to track heuristic progress.
 * 
 * Feel free to create more global variables to track progress of your
 * heuristic.
 */

//FPU BP Core Cache
int DIMENSION_EXPLORATION_ORDER[] = {11, 12, 13, 14, 0, 1, 2, 8, 3, 5, 7, 4, 6, 9};
unsigned int CURRENT_EXPLORATION_DIMENSION_INDEX = 0;
unsigned int CURRENT_EXPLORATION_DIMENSION = DIMENSION_EXPLORATION_ORDER[CURRENT_EXPLORATION_DIMENSION_INDEX];
bool currentDimDone = false;
bool isDSEComplete = false;
int visit2 = 0;
std::string prevConfig;

int width[] = {1, 2, 4, 8};
int l1block[] = {8, 16, 32, 64};
int dl1sets[] = {32, 64, 128, 256, 512, 1024, 2048, 4096, 8192};
int dl1assoc[] = {1, 2, 4};
int il1sets[] = {32, 64, 128, 256, 512, 1024, 2048, 4096, 8192};
int il1assoc[] = {1, 2, 4};
int ul2sets[] = {256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072};
int ul2block[] ={16, 32, 64, 128};
int ul2assoc[]={1, 2, 4, 8, 16};

/*
 * Given a half-baked configuration containing cache properties, generate
 * latency parameters in configuration string. You will need information about
 * how different cache paramters affect access latency.
 * 
 * Returns a string similar to "1 1 1"
 */ 
std::string generateCacheLatencyParams(string halfBackedConfig) {
	string latencySettings;

	string delimiter = " ";
	size_t pos = 0;
	int tokens[NUM_DIMS];
    
	int il1_size = getil1size(halfBackedConfig);
	int il1_latency = log2(il1_size/(1<<10)) + extractConfigParam(halfBackedConfig, 6) - 1;
	
	int dl1_size = getdl1size(halfBackedConfig);
	int dl1_latency = log2(dl1_size/(1<<10)) + extractConfigParam(halfBackedConfig, 4) - 1;
	
	int ul2_size = getl2size(halfBackedConfig);;
	int ul2_latency = log2(ul2_size/(1<<10))+ extractConfigParam(halfBackedConfig, 9) - 5;
	latencySettings = std::to_string(dl1_latency) + delimiter +  std::to_string(il1_latency) + delimiter +  std::to_string(ul2_latency);
	return latencySettings;
}

/*
 * Returns 1 if configuration is valid, else 0
 */
int validateConfiguration(std::string configuration) {
	
	int ifq_size = 1<<(3+extractConfigParam(configuration, 0));
	if(ifq_size > l1block[extractConfigParam(configuration, 2)]){
		return 0;
	}
	if(ul2block[extractConfigParam(configuration, 8)] < 2*l1block[extractConfigParam(configuration,2)]){
		return 0;
	};
	if(ul2block[extractConfigParam(configuration, 8)] > 128){
		return 0;
	};

	int il1_size = getil1size(configuration);
	int dl1_size = getdl1size(configuration);
	int ul2_size = getl2size(configuration);

	if(! (il1_size >= 1<<11 && il1_size <= 1<<16)){
		return 0;
	} 
	if(! (dl1_size >= 1<<11 && dl1_size <= 1<<16)){
		return 0;
	} 
	if(! (ul2_size >= 1<<15 && ul2_size <= 1<<20)){
		return 0;
	} 
	if(! (ul2_size >= 1<<15 && ul2_size <= 1<<20)){
		return 0;
	} 
	if(! (ul2_size >= 2*(il1_size+dl1_size))){
		return 0;
	} 

	return isNumDimConfiguration(configuration);
}

/*
 * Given the current best known configuration, the current configuration,
 * and the globally visible map of all previously investigated configurations,
 * suggest a previously unexplored design point. You will only be allowed to
 * investigate 1000 design points in a particular run, so choose wisely.
 *
 * In the current implementation, we start from the leftmost dimension and
 * explore all possible options for this dimension and then go to the next
 * dimension until the rightmost dimension.
 */
std::string generateNextConfigurationProposal(std::string currentconfiguration,
		std::string bestEXECconfiguration, std::string bestEDPconfiguration,
		int optimizeforEXEC, int optimizeforEDP) {

	//
	// Some interesting variables in 431project.h include:
	//
	// 1. GLOB_dimensioncardinality
	// 2. GLOB_baseline
	// 3. NUM_DIMS
	// 4. NUM_DIMS_DEPENDENT
	// 5. GLOB_seen_configurations
	std::string nextconfiguration = currentconfiguration;
	int current_dim_starting_value;
	// Continue if proposed configuration is invalid or has been seen/checked before.
	while (!validateConfiguration(nextconfiguration) ||
		GLOB_seen_configurations[nextconfiguration]) {

		// Check if DSE has been completed before and return current
		// configuration.
		if(isDSEComplete) {
			return currentconfiguration;
		}

		std::stringstream ss;

		string bestConfig;
		if (optimizeforEXEC == 1)
			bestConfig = bestEXECconfiguration;

		if (optimizeforEDP == 1)
			bestConfig = bestEDPconfiguration;

		// Fill in other dimensions with the saved value.
		for (int dim = 0; dim < CURRENT_EXPLORATION_DIMENSION; dim++) {
			ss << extractConfigParam(bestConfig, dim) << " ";
		}
	
		int nextValue = (extractConfigParam(1, CURRENT_EXPLORATION_DIMENSION) + 1) % GLOB_dimensioncardinality[CURRENT_EXPLORATION_DIMENSION];
		
		ss << nextValue << " ";
		
		// Fill in other dimensions with the saved value.
		for (int dim = CURRENT_EXPLORATION_DIMENSION + 1;
				dim < (NUM_DIMS - NUM_DIMS_DEPENDENT); dim++) {
			ss << extractConfigParam(bestConfig, dim) << " ";

		}

		//
		// Last NUM_DIMS_DEPENDENT3 configuration parameters are not independent.
		// They depend on one or more parameters already set. Determine the
		// remaining parameters based on already decided independent ones.
		//
		string configSoFar = ss.str();

		// Populate this object using corresponding parameters from config.
		ss << generateCacheLatencyParams(configSoFar);

		// Configuration is ready now.
		nextconfiguration = ss.str();
		
		// Make sure we start exploring next dimension in next iteration.
		if (nextValue == (current_dim_starting_value - 1) % GLOB_dimensioncardinality[CURRENT_EXPLORATION_DIMENSION]) {
			CURRENT_EXPLORATION_DIMENSION_INDEX++;
			CURRENT_EXPLORATION_DIMENSION = DIMENSION_EXPLORATION_ORDER[CURRENT_EXPLORATION_DIMENSION_INDEX];
			current_dim_starting_value = extractConfigParam(nextconfiguration, CURRENT_EXPLORATION_DIMENSION);
		}
		
		// Signal that DSE is complete after this configuration.
		if (CURRENT_EXPLORATION_DIMENSION_INDEX == (NUM_DIMS - NUM_DIMS_DEPENDENT))
			isDSEComplete = true;
	}
	return nextconfiguration;
}

