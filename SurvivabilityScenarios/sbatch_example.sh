#!/bin/bash

#SBATCH --job-name=exemple
#SBATCH --nodes=1
#SBATCH --constraint=amd
#SBATCH --cpus-per-gpu=16
#SBATCH --mem=512G
#SBATCH --gpus=a100_3g.40gb:1
#SBATCH --time=5
#SBATCH --mail-type=ALL
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

# Your computation here
ampl test-loop.run
