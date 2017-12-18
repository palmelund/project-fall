from os import path, makedirs
import os, sys
from shutil import copyfile, copytree, make_archive, rmtree
import boto3
from server.sns.sns_credentials import region_name, aws_access_key_id, aws_secret_access_key
from pprint import pprint


# When more lambda functions are made, append them below.
# We do it this way just to make everything easier.
# When requiring more than one file not part of the standard packed library, include them in the list.
# The name of the output directory and zip file should be the last element in the list.
# The first file in each list must be the main file
file_folder_lists = [
    ["alexa_help.py", "lib:requests", "alexa_help"],

    ["device_get_user.py", "device_user"],

    ["device_put_helper.py", "device_put_helper"],

    ["alarm_post_helper.py", "alarm_post_helper"],
    ["alarm_put_helper.py", "alarm_put_helper"],

    ["user_get.py", "authenticate", "user_get"],
    ["citizen_get.py", "citizen_get"],
    ["contact_get.py", "contact_get"],
    ["alarm_get.py", "alarm_get"],

    ["user_post.py", "authenticate", "user_post"],
    ["alarm_post.py", "alarm_post"],
    ["device_post.py", "device_post"],

    ["user_put.py", "user_put"],
    ["alarm_put.py", "alarm_put"],
    ["device_put.py", "device_put"],

    ["user_delete.py", "user_delete"],
    ["alarm_delete.py", "alarm_delete"],
    ["device_delete.py", "device_delete"],

    ["citizen_get_all.py", "citizen_get_all"],
    ["contact_get_all.py", "contact_get_all"],

    ["populate_server.py", "populate_server"],

    ["authenticator.py", "authenticate", "authenticator"],
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

    # Get user token lib
    if "authenticate" in file_folder_list:
        copytree("../../jwt", folder_name + "/jwt")

    # Include marshmallow for proper json support
    copytree("../../marshmallow", folder_name + "/marshmallow")

    # Since AWS doesn't provide a library for interacting with PostgreSQL, we have to provide it ourselves
    copytree("../../psycopg2", folder_name + "/psycopg2")

    # If we need to make requests
    if "lib:requests" in file_folder_list:
        copytree("../../certifi", folder_name + "/" + "certifi")
        copytree("../../chardet", folder_name + "/" + "chardet")
        copytree("../../idna", folder_name + "/" + "idna")
        copytree("../../requests", folder_name + "/" + "requests")
        copytree("../../urllib3", folder_name + "/" + "urllib3")

    # Finally zip the output folder. The zip file can then be uploaded to the lambda function
    make_archive(folder_name, "zip", folder_name)

    # Cleanup
    rmtree(folder_name)


# Upload zip files to lambdas

arn_map = [
    # ["alexa_help.zip", "AlexaHelp"],
    #
    # ["device_user.zip", "ProjectFallDeviceUser"],
    #
    # ["alarm_post_helper.zip", "ProjectFallAlarmCreate"],
    # ["alarm_put_helper.zip", "ProjectFallAlarmPutHelper"],

    #["device_put_helper.zip", "ProjectFallDevicePutHelper"],

    # ["user_get.zip", "ProjectFallUserGet"],
    # ["citizen_get.zip", "ProjectFallCitizenGet"],
    # ["contact_get.zip", "ProjectFallContactGet"],
    # ["alarm_get.zip", "ProjectFallAlarmGet"],
    #
    # ["user_post.zip", "ProjectFallUserPost"],
    # ["alarm_post.zip", "ProjectFallAlarmPost"],
    # ["device_post.zip", "ProjectFallDevicePost"],
    #
    # ["user_put.zip", "ProjectFallUserPut"],
    # ["alarm_put.zip", "ProjectFallAlarmPut"],
    # ["device_put.zip", "ProjectFallDevicePut"],

    # ["user_delete.zip", "ProjectFallUserDelete"],
    # ["alarm_delete.zip", "ProjectFallAlarmDelete"],
    # ["device_delete.zip", "ProjectFallDeviceDelete"],
    #
    # ["populate_server.zip", "ProjectFallPopulateServer"],

    ["citizen_get_all.zip", "ProjectFallCitizenGetAll"],
    # ["contact_get_all.zip", "ProjectFallContactGetAll"],

    # ["authenticator.zip", "ProjectFallAuthenticator"],
]

aws_client = boto3.client(
    "lambda",
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

for m in arn_map:
    file_name = m[0]
    function_name = m[-1]

    res = aws_client.update_function_code(
        FunctionName=function_name,
        ZipFile=open(file_name, "rb").read()
    )

    pprint(res)

dirs = os.listdir(".")

for f in dirs:
    if f.endswith(".zip"):
        os.remove(os.path.join(".", f))
    elif os.path.isdir(f):
        rmtree(f)
