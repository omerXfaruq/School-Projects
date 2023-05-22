BLOCKSIZES=(\
  "2" \
  "3" \
  "4" \
  "5" \
  "6" \
  "7" \
  "8" \
  "16" \
  "32" \
  "64" \
  "128" \
)

DATASETS=(\
  "./dataset/50-1225.in" \
  "./dataset/100-4000.in" \
  "./dataset/500-40000.in" \
  "./dataset/1000-400000.in" \
  "./dataset/2000-1200000.in" \
)

for data in "${DATASETS[@]}"
do  
    printf "\n seq on $data:\n"
    time ./seq $data cur.out 
done

for data in "${DATASETS[@]}"
do
    printf "\n apsp on $data B: 5\n"
    time ./apsp $data cur.out 5
done

for block in "${BLOCKSIZES[@]}"
do
    printf "\n apsp on 2000-1200000 B: $block \n"
    time ./apsp ./dataset/2000-1200000.in cur.out $block
done