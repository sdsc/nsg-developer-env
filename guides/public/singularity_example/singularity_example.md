# Singularity Example
This is an example of running an MPI job using a singularity container. More
example definition files can be found [here](https://github.com/mkandes/naked-singularity).

## Building a Container from a Definition File
1. Grab the definition file from [this link](https://raw.githubusercontent.com/mkandes/ubuntu-openmpi/master/Singularity). You can either
copy and paste from the link, or run this command:
``` bash
wget -O mpi-example.def https://raw.githubusercontent.com/mkandes/ubuntu-openmpi/master/Singularity
```
This matches the OpenMPI v3.1.6 on Expanse at this writing:
https://raw.githubusercontent.com/mkandes/ubuntu-openmpi/master/Singularity.ubuntu-18.04-openmpi-3.1.6

2. Build the container with the following command:
``` bash
sudo /opt/singularity-3.1.0/bin/singularity build mpi-container mpi-example.def
```

## Compile Test MPI Code

1. Save the following as hello_world.c:
``` c
// Author: Wes Kendall
// Copyright 2011 www.mpitutorial.com
// This code is provided freely with the tutorials on mpitutorial.com. Feel
// free to modify it for your own use. Any distribution of the code must
// either provide a link to www.mpitutorial.com or keep this header intact.
//
// An intro MPI hello world program that uses MPI_Init, MPI_Comm_size,
// MPI_Comm_rank, MPI_Finalize, and MPI_Get_processor_name.
//
#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
  MPI_Init(NULL, NULL);

  int world_size;
  MPI_Comm_size(MPI_COMM_WORLD, &world_size);

  int world_rank;
  MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

  char processor_name[MPI_MAX_PROCESSOR_NAME];
  int name_len;
  MPI_Get_processor_name(processor_name, &name_len);

  printf("Hello world from processor %s, rank %d out of %d processors\n",
         processor_name, world_rank, world_size);

  MPI_Finalize();
}
```

2. Compile the code with the following command:
``` bash
mpicc helllo_world.c -o mpi-code
```

## Running the Container
1. Run the container with the following command:
``` bash
singularity exec -B . mpi-container ./mpi-code
```

You should see some output like the following:
```
Hello world from processor test-instance, rank 0 out of 1 processors
```
