g++ -o ./static.out -fopenmp openmp_prime_finding_static.cpp 
g++ -o ./dynamic.out -fopenmp openmp_prime_finding_dynamic.cpp
g++ -o ./guided.out -fopenmp openmp_prime_finding_dynamic.cpp

echo "M,OpenMp Loop Scheduling Method,Chunk Size,T1,T2,T3,T4,T8,S2,S4,S8" > test.csv



###############''#################


###############''#################

scheduling="static"

export OMP_NUM_THREADS=1

inputSize=1000000
chunkSize=10

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv



######

scheduling="dynamic"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


######

scheduling="guided"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


################################################################################################################################################################



scheduling="static"

export OMP_NUM_THREADS=1


chunkSize=100

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv



######

scheduling="dynamic"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


######

scheduling="guided"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


################################################################################################################################################################



################################################################################################################################################################



scheduling="static"

export OMP_NUM_THREADS=1


chunkSize=1000

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv



######

scheduling="dynamic"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


######

scheduling="guided"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


################################################################################################################################################################



###############''#################


###############''#################

scheduling="static"

export OMP_NUM_THREADS=1

inputSize=10000000
chunkSize=10

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv



######

scheduling="dynamic"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


######

scheduling="guided"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


################################################################################################################################################################



scheduling="static"

export OMP_NUM_THREADS=1


chunkSize=100

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv



######

scheduling="dynamic"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


######

scheduling="guided"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


################################################################################################################################################################



################################################################################################################################################################



scheduling="static"

export OMP_NUM_THREADS=1


chunkSize=1000

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv



######

scheduling="dynamic"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


######

scheduling="guided"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


################################################################################################################################################################






###############''#################


###############''#################

scheduling="static"

export OMP_NUM_THREADS=1

inputSize=100000000
chunkSize=10

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv



######

scheduling="dynamic"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


######

scheduling="guided"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


################################################################################################################################################################



scheduling="static"

export OMP_NUM_THREADS=1


chunkSize=100

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv



######

scheduling="dynamic"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


######

scheduling="guided"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


################################################################################################################################################################



################################################################################################################################################################



scheduling="static"

export OMP_NUM_THREADS=1


chunkSize=1000

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv



######

scheduling="dynamic"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


######

scheduling="guided"

export OMP_NUM_THREADS=1

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=2

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration2=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=4

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration4=$((($(date +%s%N) - $timestop)/1000000))

export OMP_NUM_THREADS=8

timestop=$(date +%s%N)
./$scheduling.out $inputSize $chunkSize > $inputSize.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

speedUp2=$((duration1/duration2))
speedUp4=$((duration1/duration4))
speedUp8=$((duration1/duration8))

echo "$inputSize,$scheduling,$chunkSize,$duration1,$duration2,$duration4,$duration8,$speedUp2,$speedUp4,$speedUp8" >> test.csv


################################################################################################################################################################



