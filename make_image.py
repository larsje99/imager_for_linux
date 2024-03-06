import subprocess

def MakeImage(inputNumber, log_file_path):
    drivePath = subprocess.getoutput('lsscsi | rev | cut -d \' \' -f2 | rev')
    command = 'ewfacquire -w -m removable -l image_process_log -c fast -f ftk -t ' + str(inputNumber) + ' ' + drivePath

    # Open log file in append mode
    with open(log_file_path, "a") as log_file:
        # Run the command using subprocess.Popen() to capture output
        process = subprocess.Popen('sudo -S gnome-terminal -- bash -c "' + command + '; read -p \'Press Enter to exit...\'"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        # Read and log output line by line
        for line in process.stdout:
            log_file.write(line)
            print(line, end='')  # Print output to console for real-time progress

        for line in process.stderr:
            log_file.write(line)
            print(line, end='')  # Print error output to console

        # Wait for the process to finish
        process.wait()

    if process.returncode == 0:
        print("Command executed successfully.")
    else:
        print("Error executing command:", process.returncode)