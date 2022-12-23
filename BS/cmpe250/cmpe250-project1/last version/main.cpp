#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include "SurveyClass.h"
using namespace std;

template <class Container>
void split1(const string& str, Container& cont)
{
    istringstream iss(str);
    copy(istream_iterator<string>(iss),
              istream_iterator<string>(),
              back_inserter(cont));
}

float findAmount(const vector<string> words)
{
    float return_value = 0;
    for(int i=0; i<words.size(); i++){
        if (words[i][0] == '$') {
            const char *cstr = (words[i].substr(1)).c_str();
            return_value = strtof(cstr, NULL);
            cout << "return_value: " << return_value << endl;
            break;
        }
    }
    return return_value;
}

int main(int argc, char* argv[]) {
    // below reads the input file
    // in your next projects, you will implement that part as well
    if (argc != 3) {
        cout << "Run the code with the following command: ./project1 [input_file] [output_file]" << endl;
        return 1;
    }

    cout << "input file: " << argv[1] << endl;
    cout << "output file: " << argv[2] << endl;


    /*
    // here, perform the input operation. in other words,
    // read the file named <argv[1]>
    ifstream infile(argv[1]);
    string line;
    vector<string> input;
    // process first line
    getline(infile, line);
    int N = stoi(line);
    cout << "number of input lines: " << N << endl;

    SurveyClass mySurveyClass;
    for (int i=0; i<N; i++) {
        getline(infile, line);
        cout << "line: " << line << endl;

        vector<string> words;
        split1(line,words);
        string curr_name = words[0];
        float curr_amount = findAmount(words);

        mySurveyClass.handleNewRecord(curr_name, curr_amount);
    }

    cout << "input file has been read" << endl;

    float minExp = mySurveyClass.calculateMinimumExpense();
    float maxExp = mySurveyClass.calculateMaximumExpense();
    float avgExp = mySurveyClass.calculateAverageExpense();

    // here, perform the output operation. in other words,
    // print your results into the file named <argv[2]>
    ofstream myfile;
    myfile.open (argv[2]);
    myfile << minExp << " " << maxExp << " " << avgExp << endl;
    myfile.close();

    cout << "minExp " << minExp << endl;
    cout << "maxExp " << maxExp << endl;
    cout << "avgExp " << avgExp << endl;
    */


    return 0;
}
