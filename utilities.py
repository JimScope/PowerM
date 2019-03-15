from datetime import datetime
import config


# Write a new line to the log file
def log(entry, log_file=config.log_file_path):
    with open(log_file, "a") as log_file:
        time_stamp = datetime.now().strftime("%c")
        log_file.write(time_stamp + " - " + entry + "\n")
    # Log File is closed
