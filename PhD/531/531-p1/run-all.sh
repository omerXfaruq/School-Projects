printf "New benchmark:\n"

make clean
make -j


DATASETS=(\
  "./data/dataset_easy.txt" \
  "./data/dataset_hard.txt" \
  "./data/dataset_benchmark.txt" \
)

export PROGRAM=./solver_seq

for DATASET in "${DATASETS[@]}"
do
  printf "$PROGRAM on $DATASET:\n"
  $PROGRAM $DATASET
done


OMP_PROGRAMS=(\
  "./solver_omp" \
  "./solver_omp_prealloc" \
  "./solver_omp_tasks" \
)

BINDS=(\
  "close" \
  "spread" \
)

NUM_THREADS=(\
  "1" \
  "2" \
  "4" \
  "8" \
  "16" \
  "24" \
)


for PROGRAM in "${OMP_PROGRAMS[@]}"
do
  for DATASET in "${DATASETS[@]}"
  do
    for BIND in "${BINDS[@]}"
    do
      export OMP_PROC_BIND=$BIND
      for NUM in "${NUM_THREADS[@]}"
      do
        export OMP_NUM_THREADS=$NUM
        printf "$PROGRAM on $DATASET, $BIND, $NUM:\n"
        $PROGRAM $DATASET
      done
    done
  done
done