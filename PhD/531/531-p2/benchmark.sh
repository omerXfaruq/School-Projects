make -j
time mpirun -np 2 ./apsp ./dataset/2000-1200000.in  cur.out
diff ./dataset/2000-1200000.out cur.out