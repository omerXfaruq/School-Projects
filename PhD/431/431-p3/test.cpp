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

#include "431project.h"
#include "YOURCODEHERE.h"

using namespace std;
std::map<std::string, unsigned int> GLOB_seen_configurations;
std::pair<double, double> GLOB_baseline_EP_pair;
std::map<std::string, std::map<std::string, double>*> GLOB_extracted_values;
std::map<std::string, std::pair<double, double> > GLOB_derived_values;

int main() {
	// Test validateConfiguration
	for (unsigned i0 = 0; i0 < 4; ++i0)
	for (unsigned i1 = 0; i1 < 4; ++i1)
	for (unsigned i2 = 0; i2 < 9; ++i2)
	for (unsigned i3 = 0; i3 < 3; ++i3)
	for (unsigned i4 = 0; i4 < 9; ++i4)
	for (unsigned i5 = 0; i5 < 3; ++i5)
	for (unsigned i6 = 0; i6 < 10; ++i6)
	for (unsigned i7 = 0; i7 < 4; ++i7)
	for (unsigned i8 = 0; i8 < 5; ++i8)
{
	std::stringstream ss;
	ss << i0 << " 0 " << i1 << " " << i2 << " " << i3 << " " << i4 << " " << i5 << " " << i6 << " " << i7 << " " << i8 << " 0 0 0 0 0 0 0 0";
	int res = validateConfiguration(ss.str());
	if (res) {
		std::cout << ss.str() << ": ";

		// For a valid param, generateCacheLatencyParams
		std::cout << generateCacheLatencyParams(ss.str()) << std::endl;
	}
}
	
	return 0;
}
