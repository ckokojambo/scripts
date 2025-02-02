#!/bin/bash

# Check if both input and output directory paths are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <input_directory> <output_directory>"
    exit 1
fi

# Store the input and output directory paths
input_directory="$1"
output_directory="$2"

# Check if the input directory is valid
if [ ! -d "$input_directory" ]; then
    echo "Error: Input directory '$input_directory' is not valid."
    exit 1
fi

# Check if the output directory exists; if not, create it
if [ ! -d "$output_directory" ]; then
    echo "Output directory '$output_directory' does not exist. Creating it..."
    mkdir -p "$output_directory"
fi

# Loop through all .fit files in the input directory
for fitfile in "$input_directory"/*.fit; do
    # Extract the base filename without the .fit extension
    basefilename=$(basename "$fitfile" .fit)
    
    # Convert the .fit file to unicsv and save it in the output directory
    gpsbabel -i garmin_fit -f "$fitfile" -o unicsv,fields="date+time+lat+lon+alt+ele+caden+speed+temp" -F "$output_directory/${basefilename}.csv"
done

echo "Conversion complete! CSV files saved in '$output_directory'."
