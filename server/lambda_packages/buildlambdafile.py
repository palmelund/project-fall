from os import path, makedirs
from shutil import copyfile, copytree, make_archive, rmtree

# When more lambda functions are made, append them below.
# We do it this way just to make everything easier.
# When requiring more than one file not part of the standard packed library, include them in the list.
# The name of the output directory and zip file should be the last element in the list.
# The first file in each list must be the main file
file_folder_lists = [
    #["activate_alarm.py", "activate_alarm"],
    #["put_alarm.py", "update_alarm"],
    ["login.py", "login"],
    ["create_user.py", "create_user"],
    #["control_panel_add_citizen.py", "control_panel_add_citizen"],
    #["control_panel_add_contact.py", "control_panel_add_contact"],
    #["control_panel_get_citizen.py", "control_panel_get_citizen"],
    #["control_panel_get_citizens.py", "control_panel_get_citizens"],
    #["control_panel_get_contact.py", "control_panel_get_contact"],
    #["control_panel_get_contacts.py", "control_panel_get_contacts"],
    #["control_panel_search_contact.py", "control_panel_search_contacts"],

    ["alarm_activate.py", "alarm_activate"],
    ["alarm_create.py", "alarm_create"],
    ["alarm_respond.py", "alarm_respond"],
    ["alarm_destroy.py", "alarm_destroy"]
]

for file_folder_list in file_folder_lists:
    # We create a folder, in which we put everything to upload with the lambda
    # Remember that the folder name is the last name in the list
    folder_name = file_folder_list[-1]
    print("Current lambda folder: " + folder_name)

    # If folder already exist, remove them
    if path.exists(folder_name):
        rmtree(folder_name)

    # Recreate folder
    makedirs(folder_name)

    # copy the main file over, and rename it
    copyfile("../" + file_folder_list[0], folder_name + "/" + "lambda_function.py")

    # Copy other specified files to the output directory
    for file_name in file_folder_list[:-1]:
        copyfile("../" + file_name, folder_name + "/" + file_name)

    # connect_str is a private file containing connectivity info for the database
    # This file should only be present locally on the computer packing the files
    copyfile("../database/connect_str.py", folder_name + "/" + "connect_str.py")

    # database
    copytree("../database", folder_name + "/" + "database")

    # Copy the respond method. This is used to properly construct the response messages
    copyfile("../respond.py", folder_name + "/" + "respond.py")

    # Since AWS doesn't provide a library for interacting with PostgreSQL, we have to provide it ourselves
    copytree("psycopg2", folder_name + "/" + "psycopg2")

    # Since some lambdas depend on the models, we also pack that library
    copytree("../../model", folder_name + "/" + "model")

    # Some lambdas require SNS support, so we also copy that
    copytree("../sns", folder_name + "/" + "sns")

    # Proper serialization
    copyfile("../json_serializer.py", folder_name + "/" + "json_serializer.py")

    # Include ARN endpoints
    copyfile("../endpoints.py", folder_name + "/" + "endpoints.py")

    # Finally zip the output folder. The zip file can then be uploaded to the lambda function
    make_archive(folder_name, "zip", folder_name)

    # Cleanup
    rmtree(folder_name)

