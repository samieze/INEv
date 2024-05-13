#!/bin/bash

while IFS= read -r directory_name; do
    if [ -d "$directory_name" ]; then
	echo "Starting Experiments in '$directory_name'"
        cd "$directory_name"/scripts || exit 1
	./combined.sh > out
        # Return to the original directory 
        cd - || exit 1
    else
        echo "Directory '$directory_name' does not exist."
    fi
done < "failed_experiments.txt"
