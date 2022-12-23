#!/bin/bash
benchpairs=( \
"/home/software/simplesim/ss-benchmark/bzip2/bzip2_base.i386-m32-gcc42-nn /home/software/simplesim/ss-benchmark/bzip2/dryer.jpg" \
"/home/software/simplesim/ss-benchmark/mcf/mcf_base.i386-m32-gcc42-nn /home/software/simplesim/ss-benchmark/mcf/inp.in" \
"/home/software/simplesim/ss-benchmark/hmmer/hmmer_base.i386-m32-gcc42-nn /home/software/simplesim/ss-benchmark/hmmer/bombesin.hmm" \
"/home/software/simplesim/ss-benchmark/sjeng/sjeng_base.i386-m32-gcc42-nn /home/software/simplesim/ss-benchmark/sjeng/test.txt" \
"/home/software/simplesim/ss-benchmark/equake/equake_base.pisa_little < /home/software/simplesim/ss-benchmark/equake/inp.in")

#
# List of Design Space parameters and their possible values
#

# Number of instruction pipelines in processor (= # of ALU, FPU etc.)
width=( "1" "2" "4" "8" )

# In-order core of Out-of-Order core
scheduling=( "-issue:inorder true -issue:wrongpath false" "-issue:inorder false -issue:wrongpath true" )

#
# ## Cache related params

# Block size in bytes of L1 $ (= L1 Data $ block size = L1 Instruction $ block size)
l1block=( "8" "16" "32" "64" )

# Number of sets in L1 Data $
dl1sets=( "32" "64" "128" "256" "512" "1024" "2048" "4096" "8192" )

# Associativity of L1 Data $
dl1assoc=( "1" "2" "4" )

# Number of sets in L1 Instruction $
il1sets=( "32" "64" "128" "256" "512" "1024" "2048" "4096" "8192" )

# Associativity of L1 Instruction $
il1assoc=( "1" "2" "4" )

# Number of sets in Unified L2 $ 
ul2sets=( "256" "512" "1024" "2048" "4096" "8192" "16384" "32768" "65536" "131072" )

# Block size in bytes of Unified L2 $
ul2block=( "16" "32" "64" "128" )

# Associativity of unified L2 $
ul2assoc=( "1" "2" "4" "8" "16" )

# Caches and TLBs replacement policy
# l = LRU
# f = FIFO
# r = random
replacepolicy=("l" "f" "r")

#
# ## Other processor params

# Floating point unit width
fpwidth=( "1" "2" "4" "8" )

# Choice of branch predictor
branchsettings=("-bpred nottaken" \
                "-bpred bimod -bpred:bimod 2048" \
                "-bpred 2lev -bpred:2lev 1 1024 8 0" \
                "-bpred 2lev -bpred:2lev 4 256 8 0" \
                "-bpred comb -bpred:comb 1024")

# Return Address Stack (RAS) size (# of entries)
ras=("1" "2" "4" "8")

# Branch Target Buffer <number of sets> <associativity>
btb=("128 16" "256 8" "512 4" "1024 2" "2048 1")

#
# ### Latency params. These are dependant on cache parameters.

# L1 D$ Latency
dl1lat=( "1" "2" "3" "4" "5" "6"  "7"  "8"  "9"  "10")

# L1 I$ Latency
il1lat=( "1" "2" "3" "4" "5" "6"  "7"  "8"  "9"  "10")

# Unified L2 Latency
ul2lat=( "5" "6" "7" "8" "9" "10" "11" "12" "13" "14")
###################################


#
# Set index for arrays of parameters listed above using arguments passed to this script.
#
width_index=${1}
scheduling_index=${2}
l1block_index=${3}
dl1sets_index=${4}
dl1assoc_index=${5}
il1sets_index=${6}
il1assoc_index=${7}
ul2sets_index=${8}
ul2block_index=${9}
ul2assoc_index=${10}
replacepolicy_index=${11}
fpwidth_index=${12}
branchsettings_index=${13}
ras_index=${14}
btb_index=${15}
dl1lat_index=${16}
il1lat_index=${17}
ul2lat_index=${18}

echo ${1} ${width[$width_index]}
echo ${2} ${scheduling[$scheduling_index]}
echo ${3} ${l1block[$l1block_index]}
echo ${4} ${dl1sets[$dl1sets_index]}
#
# Execute SimpleScalar simulator for each benchmark using the system defined by paramaters passed to this script.
#

for benchnum in $(seq 0 $((${#benchpairs[*]} - 1))) ; do
    eval /home/software/simplescalar/x86_64/bin/sim-outorder -fastfwd 10000000 -max:inst 1000000 \
        -fetch:ifqsize ${width[$width_index]} \
        -fetch:speed 1 -fetch:mplat 3 \
        -decode:width ${width[$width_index]} \
        -issue:width ${width[$width_index]} \
        ${scheduling[$scheduling_index]} \
        -ruu:size 32 -lsq:size 16 \
        -res:ialu ${width[$width_index]} \
        -res:imult ${width[$width_index]} \
        -res:memport 1 \
        -res:fpalu ${fpwidth[$fpwidth_index]} \
        -res:fpmult ${fpwidth[$fpwidth_index]} \
        -cache:dl1 dl1:${dl1sets[$dl1sets_index]}:${l1block[$l1block_index]}:${dl1assoc[$dl1assoc_index]}:${replacepolicy[$replacepolicy_index]} \
        -cache:il1 il1:${il1sets[$il1sets_index]}:${l1block[$l1block_index]}:${il1assoc[${il1assoc_index}]}:${replacepolicy[$replacepolicy_index]} \
        -cache:il2 dl2 \
        -cache:dl2 ul2:${ul2sets[$ul2sets_index]}:${ul2block[$ul2block_index]}:${ul2assoc[$ul2assoc_index]}:${replacepolicy[$replacepolicy_index]} \
        -cache:dl1lat ${dl1lat[$dl1lat_index]} \
        -cache:il1lat ${il1lat[$il1lat_index]} \
        -cache:dl2lat ${ul2lat[$ul2lat_index]} \
        -mem:lat 51 7 -mem:width 8 -tlb:lat 30 \
        ${branchsettings[${branchsettings_index}]} \
        -bpred:ras ${ras[$ras_index]} \
        -bpred:btb ${btb[$btb_index]} \
        -redir:sim rawProjectOutputData/"$benchnum"."${1}"."${2}"."${3}"."${4}"."${5}"."${6}"."${7}"."${8}"."${9}"."${10}"."${11}"."${12}"."${13}"."${14}"."${15}"."${16}"."${17}"."${18}".simout \
        ${benchpairs[$benchnum]}
done

#
# Make note in a file that this configuration has been simulated.
# 
touch rawProjectOutputData/DONE."${1}"."${2}"."${3}"."${4}"."${5}"."${6}"."${7}"."${8}"."${9}"."${10}"."${11}"."${12}"."${13}"."${14}"."${15}"."${16}"."${17}"."${18}".DONE
