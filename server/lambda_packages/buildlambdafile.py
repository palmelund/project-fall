# Arguments: foldername filename
import os
import sys
import zipfile
from shutil import copyfile, copytree, make_archive, rmtree


foldername = input("foldername")
filename = input("filename")

if os.path.exists(foldername):
    rmtree(foldername)

os.makedirs(foldername)


copyfile("../" + filename, foldername + "/" + "lambda_function.py")

copyfile("lambda_package_resources/connect_str.py", foldername + "/" + "connect_str.py")
copyfile("lambda_package_resources/respond.py", foldername + "/" + "respond.py")
copytree("lambda_package_resources/psycopg2", foldername + "/" + "psycopg2")

make_archive(foldername, "zip", foldername)
