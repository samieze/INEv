import subprocess

def execute_scripts(script_list):
    for script in script_list:
        try:
            subprocess.run(['python', script], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing {script}: {e}")
            break

if __name__ == "__main__":
    script_list = ['allPairs.py', 'write_config_single.py', 'determine_all_single_selectivities.py','generate_projections.py','combigen.py','computePlanCosts_aug.py','generateEvaluationPlan.py']  # Replace with the actual script filenames
    execute_scripts(script_list)