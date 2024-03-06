<h1>SETUP</h1>

RUN 'cd imager_for_linux' | Navigate to the folder
RUN 'sudo mv imager_for_linux /usr/local/bin' | Move the bash script to PATH environment
RUN 'sudo chmod +x /usr/local/bin/imager_for_linux' | Make the script executable
RUN 'cd ../..' | Go back to home directory
RUN 'sudo imager_for_linux' | Now you can run the script!
