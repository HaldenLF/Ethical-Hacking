# module for time
import time
# module for monitoring system info
import psutil

# variables for storing previous bytes
last_received = psutil.net_io_counters().bytes_recv
last_sent = psutil.net_io_counters().bytes_sent
last_total = last_received + last_sent

while True:
    # variables that get and store current bytes
    bytes_received = psutil.net_io_counters().bytes_recv
    bytes_sent = psutil.net_io_counters().bytes_sent
    bytes_total = bytes_received + bytes_sent

    # varaiables that store new bytes by subtracting from last
    new_received = bytes_received - last_received
    new_sent = bytes_sent - last_sent
    new_total = bytes_total - last_total

    # values are converted into MB
    mb_new_received = new_received / 1024 / 1024
    mb_new_sent = new_sent / 1024 / 1024
    mb_new_total = new_total / 1024 / 1024

    # prints MB values to terminal
    print(f"{mb_new_received: .2f} Mb received, {mb_new_sent: .2f} MB sent, {mb_new_total: .2f} MB total.")

    # updates last variables for next iteration
    last_received = bytes_received
    last_sent = bytes_sent
    last_total = bytes_total

    # prints message every second
    time.sleep(1)