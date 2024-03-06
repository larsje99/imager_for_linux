#############################################################################################
# IMPORTING PACKAGES

import os
import sys
import subprocess
import datetime
import time
import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import re
from make_image import MakeImage
from multiprocessing import Process

#############################################################################################
# START MAIN SCRIPT

#############################################################################################
# CREATING FUNCTIONS

try:
    def close_window():
        # Close the main window when the pop-up is closed
        root.destroy()

    current_datetime = datetime.datetime.today()
    current_datetime_format = current_datetime.strftime('%Y%m%d')

    def CheckSinFormat(inputNumber):
        sinRegex = r'^[a-z]{4}[-_]?\d{4}(?:_[1-9]\d?)?$'
        return re.fullmatch(sinRegex, inputNumber)

    def CheckFileAvailability(inputNumber):
        if os.path.exists(inputNumber + '.E01'):
            return False
        else:
            return True

    def make_image_process(inputNumber, log_file_path):
        MakeImage(inputNumber, log_file_path)

    def MakeDailyLogFile():
        try:
            # Set up logging to a file
            logging.basicConfig(filename=str(current_datetime_format) + ".log", level=logging.DEBUG)
        except:
            pass

#############################################################################################
# CREATING DAILY LOG FILE

    MakeDailyLogFile()

#############################################################################################
# LOGGER CREATION

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    logger.info("PROCESS STARTED BY USER AT " + str(current_datetime))

#############################################################################################
# CAPTURE IMPORTANT FLASH DRIVE PATHS AND ID'S

    original_connected_devices = subprocess.getoutput("lsusb | cut -d \' \' -f7-")
    listOriginalConnected = original_connected_devices.split("\n")

    original_connected_devices_id = subprocess.getoutput("lsusb | cut -d \' \' -f6")
    listOriginalConnected_ID = original_connected_devices_id.split("\n")

    deviceNumber = subprocess.getoutput("lsusb | cut -d \' \' -f4")
    deviceNumberList = deviceNumber.split("\n")

    connectedCount = len(listOriginalConnected)

#############################################################################################
# INITIALIZE MAIN SCRIPT

    while True:
        current_datetime = datetime.datetime.today()
        current_datetime_format = current_datetime.strftime('%Y%m%d')

        liveCounter = len(listOriginalConnected) - connectedCount

        original_connected_devices_id = subprocess.getoutput("lsusb | cut -d \' \' -f6")
        deviceNumber = subprocess.getoutput("lsusb | cut -d \' \' -f4")

        connectedCount = len(listOriginalConnected)

        if liveCounter == -1:
            logger.info("DEVICE DISCONNECTED AT " + str(current_datetime))
        else:
            logger.info(str(liveCounter) + " NEW DEVICE(S) CONNECTED AT " + str(current_datetime))

        if liveCounter == 1:
            informationDrive = subprocess.getoutput("lsusb -v")
            listInformation = informationDrive.split("\nBus")
            newConnected_ID = original_connected_devices_id.split("\n")
            newDeviceNumber = deviceNumber.split("\n")

            for iD, number in zip(newConnected_ID, newDeviceNumber):
                if iD not in listOriginalConnected_ID or number not in deviceNumberList:
                    listOriginalConnected_ID.append(iD)
                    deviceNumberList.append(number)
                    break

            root = tk.Tk()
            root.withdraw()

            user_input = simpledialog.askstring("Input", "Please enter a valid SIN number:")
            if user_input is None:
                logger.info("USER CANCELED IMAGE PROCESS")
                root.after(1, close_window)
                root.mainloop()

            else:
                while True:  # Loop until a valid SIN is entered
                    if CheckSinFormat(user_input) is not None:
                        if CheckFileAvailability(user_input) is False:
                            messagebox.showinfo("Title", "File already exists!")
                            user_input = simpledialog.askstring("Input", "Enter your name:")
                        logger.info("Image creation started with SIN: " + str(user_input))
                        break  # Exit the loop if a valid SIN is entered
                    elif CheckSinFormat(user_input) is None:
                        messagebox.showinfo("Title", "Please input a valid SIN number!")
                        user_input = simpledialog.askstring("Input", "Enter your name:")

                root.after(1, close_window)

                root.mainloop()

                if CheckFileAvailability(user_input) is True:
                    image_process = Process(target=make_image_process, args=(user_input, current_datetime_format + "_image_process.log"))
                    image_process.start()

                for info in listInformation:
                    if listOriginalConnected_ID[-1] and deviceNumberList[-1] in info:
                        logger.info("\n" + info + "\n")

        original_connected_devices = subprocess.getoutput("lsusb | cut -d \' \' -f7-")
        listOriginalConnected = original_connected_devices.split("\n")

        time.sleep(1)
except:
    logger.info("PROCESS KILLED BY USER AT " + str(current_datetime))