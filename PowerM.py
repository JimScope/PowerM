#! /usr/bin/python3

from time import sleep
import traceback


import config
import emailer
import utilities
# Importing Modules
from modules.test import multiply
from modules.test import slow


def on_startup():
    print("PowerMail")
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
        print("Empty")
    else:
        for x in messages:
            if x[1].startswith("$multiply "):
                keywords = x[1].lstrip("$multiply ")
                thread_multiply = multiply.MyThread(x[0],keywords)
                thread_multiply.start()

            elif x[1].startswith("$slow "):
                keywords = x[1].lstrip("$slow ")
                thread_slow = slow.MyThread(x[0],keywords)
                thread_slow.start()
    #|

def main():
    on_startup()

    # Delays measured in seconds.
    loop_delay = 15
    iteration = 0

    # Continuously monitor email for new commands, pausing every 42 seconds
    try:
        while True:
            # Check for commands in emails every loop
            print("Working...")
            read_commands()
            sleep(loop_delay)
            iteration += 1
    except:
        # In case of an uncaught exception, get stacktrace for diag and exit.
        trace_string = traceback.format_exc()

        # log it locally in case internet is down
        utilities.log("Something happened, I have crashed:\n" + trace_string)

        # Build and send an email
        sub = "PowerMail crashed"
        msg = "Something went wrong with PowerMail, here is the stack trace:\n\n" + trace_string
        emailer.send(sub, msg)

        # Exit the program with error code 1
        exit(1)

main()
