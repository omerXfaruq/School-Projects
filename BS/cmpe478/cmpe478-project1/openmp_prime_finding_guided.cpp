#include <iostream>
#include <vector>
#include <sstream>
#include <math.h>
#include <omp.h>
#include <bits/stdc++.h> 
using namespace std;

//TODO: -How to schedulize and use chunk size together?
//      -Automize running and outputing as csv.

//Returns closest smaller odd number
int oddConversion(int number){
    if (number%2==0){
        return number-1;
    }
    return number;
}

bool isItPrime(vector<int> primes,int number){
    bool itIsPrime=true;
    for(int i=0;i<primes.size();i++){
        if (number < primes[i]*primes[i]){
            break;
        }
        if (number%primes[i]==0){
            itIsPrime=false;
        }
    }
    return itIsPrime;
}

int main(int argc, char *argv[]) {
    // below reads the input file
    // in your next projects, you will implement that part as well
    if (argc != 3) {
        cout << "Run like this: ./a.out [M] [ChunkSize]" << endl;
        return 1;
    }

    istringstream ss(argv[1]);
    int N;
    if (!(ss >> chunkSize)) {
        std::cerr << "Invalid number: " << argv[1] << '\n';
    } else if (!ss.eof()) {
        std::cerr << "Trailing characters after number: " << argv[1] << '\n';
    }

    istringstream ss2(argv[2]);
    int chunkSize;
    if (!(ss2 >> N)) {
        std::cerr << "Invalid number: " << argv[2] << '\n';
    } else if (!ss2.eof()) {
        std::cerr << "Trailing characters after number: " << argv[2] << '\n';
    }

    //Generate primes until sqrt(N)
    cout << N << endl;
    int M=(int)sqrt(N);
    cout << M << endl;
    vector<int> primes;
    int j;
    int k;
    int n;
    int quo, rem;
    bool loop1 = 1;
    bool loop2 = 1;

    //P1
    primes.push_back(2);
    n = 3;
    j = 0;

    while (loop1) {
        //P2
        loop2 = true;
        j += 1;
        primes.push_back(n);
        //P3
        while (loop2) {


            //P4
            n += 2;
            if(n>M){    //Goto P9
                loop1=false;    
                break;
            }
            k = 1;

            while (1) {
                //P6

                quo = n / primes[k];
                rem = n % primes[k];
                if (rem == 0) {//Goto P4
                    break;
                }
                //P7
                if (quo <= primes[k]) {//Goto p2
                    loop2 = false;
                    break;
                }
                //P8
                k += 1;
            }
        }
    }


    int i=0;
    int nthreads;
    #pragma omp parallel
  {
    #pragma omp single
    nthreads=omp_get_num_threads();
  }


    cout << "No of nthreads:" << nthreads << endl;
    int tid;
    vector<int> primeVectors[nthreads];

    #pragma omp parallel private(i,tid)
    {
        tid = omp_get_thread_num();

      #pragma omp for schedule(guided,chunkSize)
        for(i =oddConversion(M+1) ; i < N ; i+=2 ) {
            if(isItPrime(primes,i)){
                primeVectors[tid].push_back(i);
            }
    }

}
    
    //Combining different threads' vectors

    for (j = 1; j < nthreads; j++) {
        primeVectors[0].insert( primeVectors[0].end(),primeVectors[j].begin(),primeVectors[j].end() );

}
    sort(primeVectors[0].begin(),primeVectors[0].end());
    primes.insert(primes.end(),primeVectors[0].begin(),primeVectors[0].end());
    


    cout << "Finished all of them" << endl;
    
    for (j = 0; j < primes.size(); j++) {
        printf("%d\n", primes[j]);
    }
}