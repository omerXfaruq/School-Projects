make -j

OMP_PROGRAMS=(\
  "./solver_omp_tasks" \
)

DATASETS=(\
  "./data/dataset_hard.txt" \
  "./data/dataset_benchmark.txt" \
)

BINDS=(\
  "spread" \
)

NUM_THREADS=(\
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