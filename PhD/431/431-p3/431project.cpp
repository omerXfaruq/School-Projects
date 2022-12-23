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
#include <limits>

#include "431project.h"

// Data structures to hold simulation result summaries.
std::pair<double, double> GLOB_baseline_EP_pair;
std::map<std::string, std::map<std::string, double>*> GLOB_extracted_values;
std::map<std::string, std::pair<double, double> > GLOB_derived_values;
std::map<std::string, unsigned int> GLOB_seen_configurations;

void printUsage() {
	fprintf(stderr,
			"Wrong number of arguments! Run as './DSE energy' or"
					" './DSE performance' for energy or performance run, respectively\n");
}

int main(int argc, char** argv) {

	std::ofstream logfile;
	std::ofstream bestfile;

	int optimizeforEDP = 0;
	int optimizeforEXEC = 0;

	srand(0); // for stability during testing

	if (2 != argc) {
		printUsage();
		return -1;
	} else {
		int isEarg = ('e' == argv[1][0]);
		int isParg = ('p' == argv[1][0]);
		if (!(isEarg || isParg)) {
			printUsage();
			return -1;
		} else {
			system("mkdir -p logs");
			system("mkdir -p summaryfiles");
			system("mkdir -p rawProjectOutputData");
			if (isParg) { // do performance exploration
				optimizeforEXEC = 1;
				logfile.open("logs/ExecutionTime.log");
				bestfile.open("logs/ExecutionTime.best");
			} else { // do energy-efficiency exploration
				optimizeforEDP = 1;
				logfile.open("logs/EnergyEfficiency.log");
				bestfile.open("logs/EnergyEfficiency.best");
			}
		}
	}

	std::cout << "Testing baseline: ";
	runexperiments(GLOB_baseline, 0); // generate baseline values
	populate(GLOB_baseline); // read raw values from files
	// Save baseline information
	GLOB_baseline_EP_pair.first = calculategeomeanEDP(GLOB_baseline);
	GLOB_baseline_EP_pair.second = calculategeomeanExecutionTime(GLOB_baseline);

	logfile << calculategeomeanEDP(GLOB_baseline) / GLOB_baseline_EP_pair.first
			<< ","
			<< calculategeomeanExecutionTime(GLOB_baseline)
					/ GLOB_baseline_EP_pair.second << ","
			<< calculategeomeanEDP(GLOB_baseline) << ","
			<< calculategeomeanExecutionTime(GLOB_baseline) << std::endl;
	std::cout << std::endl;

	// Prepare for main loop.
	std::cout << "Starting DSE" << std::endl << std::endl;
	double bestEDP = GLOB_baseline_EP_pair.first;
	double bestTime = GLOB_baseline_EP_pair.second;

	std::string bestTimeconfig = GLOB_baseline;
	std::string bestEDPconfig = GLOB_baseline;
	std::string currentConfiguration = GLOB_baseline;

	//for (unsigned int iter = 0; iter < 10; ++iter) {
	for (unsigned int iter = 0; iter < 1000; ++iter) {

		std::string nextconf = generateNextConfigurationProposal(
				currentConfiguration, bestTimeconfig, bestEDPconfig,
				optimizeforEXEC, optimizeforEDP);

		if(currentConfiguration == nextconf) {
			std::cerr << "returned the same configuration\n"
					"FINISH\n";
			break;
		}

		runexperiments(nextconf, iter);
		populate(nextconf);

		if (0
				== (*(GLOB_extracted_values[nextconf]))[GLOB_prefixes[0]
						+ GLOB_fields[0]]) { // quick and dirty sanity check
			// run failed, try another, don't count this one
			std::cout << " [failed] " << std::endl;
			--iter;
			continue;
		}

		double proposedGeoEDP = calculategeomeanEDP(nextconf);
		double proposedGeoTime = calculategeomeanExecutionTime(nextconf);
		double geomeanEDPNorm = proposedGeoEDP / GLOB_baseline_EP_pair.first;
		double geomeanExecTimeNorm = proposedGeoTime
				/ GLOB_baseline_EP_pair.second;

		logfile << geomeanEDPNorm << "," << geomeanExecTimeNorm << ","
				<< proposedGeoEDP << "," << proposedGeoTime << std::endl;

		if (proposedGeoTime < bestTime) {
			bestTimeconfig = nextconf;
			bestTime = proposedGeoTime;
		}

		if (proposedGeoEDP < bestEDP) {
			bestEDPconfig = nextconf;
			bestEDP = proposedGeoEDP;
		}

		std::cout << std::endl << "             " << "proposedGeoEDP="
				<< proposedGeoEDP << ", bestEDP=" << bestEDP
				<< ", proposedGeoTime=" << proposedGeoTime << ", bestTime="
				<< bestTime;

		// Get ready for next iteration.
		std::cout << std::endl << std::endl;
		currentConfiguration = nextconf;
	}

	// Dump best configurations stats and associated data to bestfile.

	// Dump best EDP config geomean and all 5 individual benchmark stats.
	bestfile << bestEDPconfig << ","
			<< calculategeomeanEDP(bestEDPconfig) / GLOB_baseline_EP_pair.first
			<< ","
			<< calculategeomeanExecutionTime(bestEDPconfig)
					/ GLOB_baseline_EP_pair.second << ","
			<< calculategeomeanEDP(bestEDPconfig) << ","
			<< calculategeomeanExecutionTime(bestEDPconfig) << ",";
	for (int i = 0; i < 5; ++i) {
		bestfile << calculateEDP(bestEDPconfig, GLOB_prefixes[i]) << ","
				<< calculateEDP(bestEDPconfig, GLOB_prefixes[i])
						/ calculateEDP(GLOB_baseline, GLOB_prefixes[i]) << ",";
	}
	bestfile << std::endl;

	// Dump best Execution Time config geomean and all 5 individual benchmark stats.
	bestfile << bestTimeconfig << ","
			<< calculategeomeanEDP(bestTimeconfig) / GLOB_baseline_EP_pair.first
			<< ","
			<< calculategeomeanExecutionTime(bestTimeconfig)
					/ GLOB_baseline_EP_pair.second << ","
			<< calculategeomeanEDP(bestTimeconfig) << ","
			<< calculategeomeanExecutionTime(bestTimeconfig) << ",";
	for (int i = 0; i < 5; ++i) {
		bestfile << calculateExecutionTime(bestTimeconfig, GLOB_prefixes[i])
				<< ","
				<< calculateExecutionTime(bestTimeconfig, GLOB_prefixes[i])
						/ calculateExecutionTime(GLOB_baseline,
								GLOB_prefixes[i]) << ",";
	}
	bestfile << std::endl;

	logfile.close();
	bestfile.close();
}
