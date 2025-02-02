#!/bin/bash

output=$(nvidia-smi)

# Now, use grep and awk to extract the memory usage values
memMin=$(echo "$output" | grep -oP '(?<=Memory-Usage\s\|\s)\d+MiB\s/\s\d+MiB' | awk '{print $1}')
memMax=$(echo "$output" | grep -oP '(?<=Memory-Usage\s\|\s)\d+MiB\s/\s\d+MiB' | awk '{print $3}')

# Output the values
echo "memMin: $memMin"
echo "memMax: $memMax"
