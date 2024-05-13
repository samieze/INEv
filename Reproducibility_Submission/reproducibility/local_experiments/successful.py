import os
import shutil

# Get the current working directory
current_directory = os.getcwd()

# Create a text file to record empty directories
with open("failed_experiments.txt", "w") as empty_file:
    # Iterate over subdirectories
    for subdir in os.listdir(current_directory):
        if subdir.startswith("REPRO_") and os.path.isdir(subdir):
            figs_directory = os.path.join(subdir, "res/figs")
            data_directory = os.path.join(subdir, "res")

            # Check if the 'res/figs' directory is empty or 'res/' has no .csv files
            if not os.listdir(figs_directory) or not any(file.endswith(".csv") for file in os.listdir(data_directory)):
                empty_file.write(subdir + "\n")
            else:
                # Create the 'Figures' directory if it doesn't exist
                figures_directory = os.path.join(current_directory, "Figures")
                os.makedirs(figures_directory, exist_ok=True)

                # Copy files from 'res/figs' to 'Figures'
                for file_name in os.listdir(figs_directory):
                    src = os.path.join(figs_directory, file_name)
                    dest = os.path.join(figures_directory, file_name)
                    shutil.copy(src, dest)
