from datetime import datetime
import tarfile
import config


# Write a new line to the log file
def log(entry, log_file=config.log_file_path):
    with open(log_file, "a") as log_file:
        time_stamp = datetime.now().strftime("%c")
        log_file.write(time_stamp + " - " + entry + "\n")
    # Log File is closed


def compress(name):
    with tarfile.open("data/"+name+".tar.bz2", 'w:bz2') as tar:
        tar.add(name)
    return 0
