#!/bin/bash

#SBATCH --job-name=cpu_job
#SBATCH --nodes=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=2:00:00
#SBATCH --output=cpu_job-%j.out
#SBATCH --error=cpu_job-%j.err

# Your computation here
for ((i=6; i<=30; i+=6)); do
  # Launch a batch of 10 instances in parallel
  for ((j=6; j<=15; j+=1)); do
    # Uncomment the line below for your specific use case
    # python3 runHeuristicIns.py $j & # Example with a Python script
    python3 SMART_SINC_SINC+_loop.py $i $j  10 & # Running Python script with two arguments
    # cust_func $j & # Example with a custom function
  done
  # Wait for all background processes started in the loop to complete before continuing
  wait
done

## Put all cust_func in the background and bash
## would wait until those are completed
## before displaying all done message
wait
echo "All done for all cases of sinc algorithm"
