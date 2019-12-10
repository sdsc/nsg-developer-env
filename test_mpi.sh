NUM_CORES=`grep -c ^processor /proc/cpuinfo`

git clone https://github.com/wesleykendall/mpitutorial.git
cd mpitutorial/tutorials/mpi-hello-world/code/
make
echo "Running test with $NUM_CORES cores: mpirun -n $NUM_CORES mpi_hello_world"
mpirun -n $NUM_CORES mpi_hello_world
