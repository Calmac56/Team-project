import subprocess
from pathlib import Path
import os
from cs14.models import Candidate



BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_DIR = os.path.join(BASE_DIR,'media')
USER_DIR = os.path.join(MEDIA_DIR, 'users')
TEST_DIR = os.path.join(MEDIA_DIR, 'tests')


def create_container():
    #DOCKER IMAGE BEING USED
    dimage = "coding-image" 
    #create a container from the specified image
    proc = subprocess.Popen(["docker","create", dimage], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    encoded_containerID, error = proc.communicate()
    if proc.returncode != 0:
        return ['Error creating container', error]
    else:
        containerID = encoded_containerID.decode("utf-8")[:12]
        return containerID

def remove_container(containerID):
    #remove given container
    stopCont, error = subprocess.Popen(["docker", "container", "stop", containerID, ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if len(error) != 0:
        return ["Failed to stop container.", error]

    rmCont, error = subprocess.Popen(["docker", "container", "rm", containerID, ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if len(error) != 0:
        return ["Failed to remove container.", error]


def run_container(containerID, filename, input_file):
    #RUNS AND COMPILES FILE IN CONTAINER

    #copy user code and input files to container
    subprocess.run([ "docker", "cp", filename, containerID + ":" + "/testing"])
    subprocess.run(["docker", "cp", input_file, containerID + ":" + "/input"])
    #run the container
    runCont = subprocess.Popen(["docker", "container", "start", "-a", containerID, ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #get outputs or errors
    output, error = runCont.communicate()
    exitstatus = subprocess.Popen(["docker", "inspect", containerID, "--format='{{.State.ExitCode}}'"], stdout=subprocess.PIPE)
    exitcode = exitstatus.communicate()[0]

    #Returns to the user that the container was timed out or that output was too long. Both security measures to prevent malicious code from crashing the server.
    if exitcode.decode().strip() == "'124'":
        output = "Time limit exceeded".encode()

    if len(output) > 2000:
        output = "Output exceeds size limit".encode()

    
    
    if len(error) != 0:
        return['error', error]
    else:
        return['worked', output]


def add_language_extension(filename, language):
    language_mapping = {'java':'.java', 'python':'.py', 'c':'.c'}

    if language in language_mapping:
        return filename + language_mapping[language]
    else:
        raise Exception('language not supported')


def test(candidate, testname, username, language, input=None):
    #if there is no container assigned, set up new one
    containerID = getattr(candidate, "containerID")
    if len(containerID) == 0:
        containerID = create_container()
        if len(containerID) != 0:
            Candidate.objects.filter(user=candidate.user).update(containerID=containerID)
        else:
            return ["Error creating container.", 0,0]
    else:
        containerID = getattr(candidate, "containerID")

    filename = os.path.join(USER_DIR, username, testname, add_language_extension('main', language))

    testfolder = os.path.join(TEST_DIR, testname)
    
    test_cases = os.listdir(os.path.join(testfolder, 'input'))

    outputs = []
    
    if input==None:
        testingInput = 'noncustom'
    else:
        testingInput = input


    #Results for run
    passes = 0
    fails = 0
    result = 0
    if testingInput == 'noncustom':
        for i, test_case in enumerate(test_cases):
            out_str = "Test Case " + str(i+1) + ":\n"
            testingInput = os.path.join(testfolder, 'input', test_case.strip())

            output = run_container(containerID, filename, testingInput)
            
            if output[0] == 'error':
                out_str+=output[1].decode('ascii')
            else:
                with open(os.path.join(testfolder, 'output', test_case.strip()), 'r') as f:
                    data = f.read()
                    #test case result
                    result = data.strip() == output[1].strip().decode("ASCII")
                    out_str += str(result) +"\n"
                    out_str += output[1].strip().decode("ASCII") + "\n"
            outputs.append(out_str + "\n")
        
            if result != 0:
                passes += 1
            else:
                fails +=1
        return outputs, passes, fails
    else:
        output = run_container(containerID, filename, testingInput)
        #add error handling
        return ["Custom testing", output[1]]

"""  
Function to test the code run on the code review page

Takes in the name of the test, username of code being tested, testing language and input for use if custom input is selected

Returns test output, test passes and fails

If custom input is selected returns just the output


"""
def reviewtest(testname, candusername, language,username , input=None):

    containerID = create_container()

    filename = os.path.join(USER_DIR, candusername, testname,username, 'temp',  add_language_extension('main', language))
  
    testfolder = os.path.join(TEST_DIR, testname)
    passes = 0
    fails = 0
    result = 0
    
    test_cases = os.listdir(os.path.join(testfolder, 'input'))

    outputs = []
    if input==None:
        testingInput = 'noncustom'
    else:
        testingInput = input

    if testingInput == 'noncustom':

        for i, test_case in enumerate(test_cases):
            out_str = "Test Case " + str(i+1) + ":\n"
            output = run_container(containerID, filename, os.path.join(testfolder, 'input', test_case.strip()))
            if output[0] == 'error':
                out_str+=output[1].decode('ascii')
                
            else:
                with open(os.path.join(testfolder, 'output', test_case.strip()), 'r') as f:
                    data = f.read()
                    result = data.strip() == output[1].strip().decode("ASCII")
                    out_str += str(data.strip() == output[1].strip().decode("ASCII")) +"\n"
                    out_str += output[1].strip().decode("ASCII") + "\n"
        
            outputs.append(out_str + "\n")
            if result != 0:
                passes += 1
            else:
                fails +=1
        return outputs, passes, fails

    else:
        output = run_container(containerID, filename, testingInput)
        #add error handling
        return ["Custom testing", output[1]]
    
    remove_container(containerID)

   




