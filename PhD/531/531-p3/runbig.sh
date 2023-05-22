time ./seq ./dataset/2000-1200000.in cur.out 

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

for block in "${BLOCKSIZES[@]}"
do
    printf "\n apsp on 2000-1200000 B: $block \n"
    time ./apsp ./dataset/2000-1200000.in cur.out $block
done
