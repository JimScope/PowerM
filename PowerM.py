#! /usr/bin/python3

from time import sleep
import traceback

# Local Modules
import config
import emailer
import utilities
# Importing PowerM Modules
from modules.test import multiply
from modules.test import slow
from modules.admin import logs


def on_startup():
    utilities.log("Starting up.")
    # Ensure the user has setup the script
    if config.email_user_name == "" or config.white_list == [] or config.email_password == "":
        utilities.log("Email variables are not setup. Exiting.")
        exit(1)
    utilities.log("Waiting for startup delay.")


def read_commands():
    messages = emailer.read()

    #|
    if messages is None:
        # print("Empty")
        pass
    else:
        for x in messages:
            if x[1].startswith("$logs"):
                thread_logs = logs.MyThread(x[0])
                thread_logs.start()

            if x[1].startswith("$multiply"):
                keywords = x[1].lstrip("$multiply ")
                thread_multiply = multiply.MyThread(x[0],keywords)
                thread_multiply.start()

            elif x[1].startswith("$slow"):
                keywords = x[1].lstrip("$slow ")
                thread_slow = slow.MyThread(x[0],keywords)
                thread_slow.start()
    #|

def main():
    on_startup()
    try:
        print("Welcome to PowerM\nCtrl-C to exit")
        print("Waiting for startup delay.")
        while True:
            sleep(15)
            read_commands()

    except Exception:
        # In case of an uncaught exception, get stacktrace for diag and exit.
        trace_string = traceback.format_exc()

        # log it locally in case internet is down
        utilities.log("Something happened, I have crashed:\n" + trace_string)

        # Build and send an email
        sub = "PowerMail crashed"
        msg = "Something went wrong with PowerMail, here is the stack trace:\n\n" + trace_string
        emailer.send(config.support, sub, msg)

        # Exit the program with error code 1
        exit(1)

main()
