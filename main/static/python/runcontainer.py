import subprocess
import os
#Currently only supports compiling one file at a time

#directory for file to be run or compiled
path = os.path.join(os.getcwd(), "testing")
file = os.listdir(path)[0]

#---COMPILATION
if file[-4:] == "java":
    proc = subprocess.run(["javac", os.path.join(path, file)])
    #remove .java file to get compiled one
    subprocess.run(["rm", os.path.join(path, file)])
    file = os.listdir(path)[0]

#---FILE BEING RUN
input_data = ''
input_path = os.path.join(os.getcwd(), "input")
input_file = os.path.join(input_path, os.listdir(input_path)[0])
with open (input_file, 'r') as f:
    input_data += f.read().strip()
subprocess.run(["rm", os.path.join(input_path, input_file)])

#filetype checking
if file[-2:] == "py":
    #python
    proc = subprocess.run(["python3", os.path.join(path, file), input_data])
elif file[-5:] == "class":
    #java
    classname = file[:-6]
    proc = subprocess.run(["java", "-cp", path, classname, input_data])

subprocess.run(["rm", os.path.join(path, file)])
