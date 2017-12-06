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
    #["login.py", "login"],
    #["create_user.py", "create_user"],
    #["control_panel_add_citizen.py", "control_panel_add_citizen"],
    #["control_panel_add_contact.py", "control_panel_add_contact"],
    #["control_panel_get_citizen.py", "control_panel_get_citizen"],
    #["control_panel_get_citizens.py", "control_panel_get_citizens"],
    #["control_panel_get_contact.py", "control_panel_get_contact"],
    #["control_panel_get_contacts.py", "control_panel_get_contacts"],
    #["control_panel_search_contact.py", "control_panel_search_contacts"],

    #["alarm_activate.py", "alarm_activate"],
    #["alarm_create.py", "alarm_create"],
    #["alarm_respond.py", "alarm_respond"],
    #["alarm_destroy.py", "alarm_destroy"],

    ["notification_endpoint_create.py", "notification_endpoint_create"],
    ["notification_endpoint_store.py", "notification_endpoint_store"],
    ["notification_endpoint_update.py", "notification_endpoint_update"],

    ["alexa_help.py", "lib:requests", "alexa_help"],

    ["device_get_user.py", "device_user"],

    ["user_get.py", "user_get"],
    ["citizen_get.py", "citizen_get"],
    ["contact_get.py", "contact_get"],
    ["alarm_get.py", "alarm_get"],


    ["populate_server.py", "populate_server"]
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
    copyfile("../" + file_folder_list[0], folder_name + "/lambda_function.py")

    # Copy other specified files to the output directory
    # for file_name in file_folder_list[:-1]:
    #    copyfile("../" + file_name, folder_name + "/" + file_name)

    # database
    copytree("../database", folder_name + "/server/database")

    # Some lambdas require SNS support, so we also need to provide that
    copytree("../sns", folder_name + "/server/sns")

    # Copy the respond method. This is used to properly construct the response messages
    copyfile("../respond.py", folder_name + "/server/respond.py")

    # Since some lambdas depend on the models, we also pack that library
    copytree("../../model", folder_name + "/model")

    # Include ARN endpoints
    copyfile("../endpoints.py", folder_name + "/server/endpoints.py")

    # Include marshmallow for proper json support
    copytree("../../marshmallow", folder_name + "/marshmallow")

    # Since AWS doesn't provide a library for interacting with PostgreSQL, we have to provide it ourselves
    copytree("../../psycopg2", folder_name + "/psycopg2")

    if "lib:requests" in file_folder_list:

        # Copy files related to requests library
        copytree("../../certifi", folder_name + "/" + "certifi")
        copytree("../../chardet", folder_name + "/" + "chardet")
        copytree("../../idna", folder_name + "/" + "idna")
        copytree("../../requests", folder_name + "/" + "requests")
        copytree("../../urllib3", folder_name + "/" + "urllib3")

    # Finally zip the output folder. The zip file can then be uploaded to the lambda function
    make_archive(folder_name, "zip", folder_name)

    # Cleanup
    rmtree(folder_name)

