DATASETS=(\
  " ./data/dataset_easy.txt " \
  " ./data/dataset_hard.txt " \
  " ./data/dataset_benchmark.txt " \
)
for D in "${DATASETS[@]}";
do
  echo $D
done