echo "N,T1,T8,T27,T64,S8,S27,S64" > $1

N=11
processorNo=1

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

processorNo=8

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

processorNo=27

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration27=$((($(date +%s%N) - $timestop)/1000000))

processorNo=64

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration64=$((($(date +%s%N) - $timestop)/1000000))

speedUp8=$(python3 divide.py $duration1 $duration8)
speedUp27=$(python3 divide.py $duration1 $duration27)
speedUp64=$(python3 divide.py $duration1 $duration64)

duration1=$(python3 divide.py $duration1 1000)
duration8=$(python3 divide.py $duration8 1000)
duration27=$(python3 divide.py $duration27 1000)
duration64=$(python3 divide.py $duration64 1000)

echo "$N,$duration1,$duration8,$duration27,$duration64,$speedUp8,$speedUp27,$speedUp64" >> $1


###
###
###

N=23
processorNo=1

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

processorNo=8

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

processorNo=27

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration27=$((($(date +%s%N) - $timestop)/1000000))

processorNo=64

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration64=$((($(date +%s%N) - $timestop)/1000000))

speedUp8=$(python3 divide.py $duration1 $duration8)
speedUp27=$(python3 divide.py $duration1 $duration27)
speedUp64=$(python3 divide.py $duration1 $duration64)

duration1=$(python3 divide.py $duration1 1000)
duration8=$(python3 divide.py $duration8 1000)
duration27=$(python3 divide.py $duration27 1000)
duration64=$(python3 divide.py $duration64 1000)

echo "$N,$duration1,$duration8,$duration27,$duration64,$speedUp8,$speedUp27,$speedUp64" >> $1

###
###
###

N=35
processorNo=1

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

processorNo=8

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

processorNo=27

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration27=$((($(date +%s%N) - $timestop)/1000000))

processorNo=64

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration64=$((($(date +%s%N) - $timestop)/1000000))

speedUp8=$(python3 divide.py $duration1 $duration8)
speedUp27=$(python3 divide.py $duration1 $duration27)
speedUp64=$(python3 divide.py $duration1 $duration64)

duration1=$(python3 divide.py $duration1 1000)
duration8=$(python3 divide.py $duration8 1000)
duration27=$(python3 divide.py $duration27 1000)
duration64=$(python3 divide.py $duration64 1000)

echo "$N,$duration1,$duration8,$duration27,$duration64,$speedUp8,$speedUp27,$speedUp64" >> $1

###
###
###

N=47
processorNo=1

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration1=$((($(date +%s%N) - $timestop)/1000000))

processorNo=8

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration8=$((($(date +%s%N) - $timestop)/1000000))

processorNo=27

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration27=$((($(date +%s%N) - $timestop)/1000000))

processorNo=64

timestop=$(date +%s%N)
mpiexec --oversubscribe -np $processorNo python3 try.py $N >>log.txt
duration64=$((($(date +%s%N) - $timestop)/1000000))

speedUp8=$(python3 divide.py $duration1 $duration8)
speedUp27=$(python3 divide.py $duration1 $duration27)
speedUp64=$(python3 divide.py $duration1 $duration64)

duration1=$(python3 divide.py $duration1 1000)
duration8=$(python3 divide.py $duration8 1000)
duration27=$(python3 divide.py $duration27 1000)
duration64=$(python3 divide.py $duration64 1000)

echo "$N,$duration1,$duration8,$duration27,$duration64,$speedUp8,$speedUp27,$speedUp64" >> $1
