DATASETS=(\
  "./dataset/50-1225.in" \
  "./dataset/100-4000.in" \
  "./dataset/500-40000.in" \
  "./dataset/1000-400000.in" \
  "./dataset/2000-1200000.in" \
)

PROGRAMS=(\
  "./seq"
  "mpirun -np 1 -hostfile hostfile ./apsp"
  "mpirun -np 2 -hostfile hostfile ./apsp"
  "mpirun -np 3 -hostfile hostfile ./apsp"
  "mpirun -np 4 -hostfile hostfile ./apsp"
)
for data in "${DATASETS[@]}"
do
  for program in "${PROGRAMS[@]}"
  do  
    printf "\n $program on $data:\n"
    time env OMP_PROC_BIND="close" $program $data cur.out
  done
done
