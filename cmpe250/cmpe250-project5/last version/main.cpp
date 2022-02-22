#include <iostream>
#include <fstream>
#include <queue>
#include <unordered_set>
#include <cmath>
#include <list>

using namespace std;

unsigned long long int modulo(unsigned long long int n) {
    return n % 1000000007;
}

unsigned long long int hashing(string &s) {
    int size = s.size();

    if (size == 1)
        return (int) s[0] - 97;

    unsigned long long int hash = 0;

    for (int i = 0; i < size; i++) {

        hash = modulo(hash * 26 + s[i] - 97);

    }
    return hash;
}


bool scanTheWordsHashes(int hash, unordered_set<unsigned long long int> &set) {
    unordered_set<unsigned long long int>::iterator it = set.begin();

    unordered_set<unsigned long long int>::iterator end = set.end();

    while (it != end) {
        if (hash == *it)
            return true;
        it++;
    }


    return false;

}

long long int
recursionFunction(string s, int size, int loc1, unordered_set<unsigned long long int> (&wordList)[1001][26],
                  int (&possibleSentences)[1001][1001]) {


    //   if (loc1 > loc2)
    //     return 0;
    //   if (loc2 > size || loc1 > size)
    //       return 0;
    if (loc1 == size)
        return 1;

    /*
    if (size < loc)
        return 0;
    if (loc == size) {
        if (scanTheWordsHashes(hash, dictionary[loc]) > 0)
            return 1;
        else
            return 0;
    }
*/

    if (possibleSentences[0][loc1] == -1) {


        int firstChar = s[loc1] - 97;
        unsigned long long int hash = firstChar;


        int nextLoc = loc1 + 1;
        unsigned long long int returns = 0;

        while (!(nextLoc > size)) {     // Putting space at each word location

            bool check = scanTheWordsHashes(hash, wordList[nextLoc-loc1 ][firstChar]);

            if (check) {
                bool bool1 = (possibleSentences[0][nextLoc] == -1);

                if (bool1) {
                    possibleSentences[0][nextLoc] = recursionFunction(s, size, nextLoc, wordList, possibleSentences);

                }

                returns = modulo(returns + possibleSentences[0][nextLoc]);

            }

            hash = modulo(hash * 26 + s[nextLoc] - 97);
            nextLoc++;

        }

        possibleSentences[0][loc1] = returns;

    }

    return possibleSentences[0][loc1];


}

int main(int argc, char *argv[]) {
    ios_base::sync_with_stdio(false);
    clock_t start;
    start = clock();

    unsigned long long int lon = modulo(pow(2, 50));
    unsigned long long int num = 1;

    for (int i = 0; i < 19; i++) {
        num = modulo(num * lon);
    }
    num = modulo(num * lon);

    cout << "num: " << num << endl;
    if (argc != 3) {
        cout << "Run the code with the following command: ./project1 [input_file] [output_file]" << endl;
        return 1;
    }

    cout << "input file: " << argv[1] << endl;
    cout << "output file: " << argv[2] << endl;

    string input = argv[1];
    string output = argv[2];


    ifstream infile(input);

    // process first line

    string sentence;

    string word;

    int dictionarySize;

    infile >> sentence;
    infile >> dictionarySize;


    unordered_set<unsigned long long int> wordsWithRespectToSize[1001][26];         //Put words into Buckets with respect to sizes


    for (int i = 0; i < dictionarySize; i++) {
        infile >> word;
        wordsWithRespectToSize[word.size()][word[0]-97].insert(hashing(word));

    }

    cout << (clock() - start) / (double) CLOCKS_PER_SEC << ": finished reading input" << endl;


    cout << (clock() - start) / (double) CLOCKS_PER_SEC << ": finished finding words inside it" << endl;


    int possibleSentences[1001][1001];
    for (int i = 0; i < 1001; i++) {
        for (int j = 0; j < 1001; j++) {
            possibleSentences[i][j] = -1;
        }
    }
    int size = sentence.size();


    long long int answer = recursionFunction(sentence, size, 0, wordsWithRespectToSize, possibleSentences);


    cout << "finished" << endl;
    cout << answer << endl;


    infile.close();

    cout << (clock() - start) / (double) CLOCKS_PER_SEC << ": finished finding output" << endl;


    ofstream out(output);

    out << answer;

    return 0;
}
