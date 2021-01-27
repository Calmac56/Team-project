import subprocess
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_DIR = os.path.join(BASE_DIR,'media')
USER_DIR = os.path.join(MEDIA_DIR, 'users')
TEST_DIR = os.path.join(MEDIA_DIR, 'tests')

def compileCode(filename, language):
    compile_command = ""
    if language == "java":
        compile_command = ("javac -d " + filename[:-5] + " " + filename + ".java").split()
        print(" ".join(compile_command))
    if language == "python":
        return ['worked']
    
    proc = subprocess.Popen(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate()
    
    if proc.returncode != 0:
        return ['error', error]
    else:
        return ['worked', output]
    
def run(filename, language, input_file):
    run_command = ""
    if language == "java":
        run_command = ("java -cp " + filename[:-5] + " main").split()
    if language == "python":
        run_command = ("python " + filename + ".py").split()
    input_data = ''
    with open(input_file, 'r') as f:
        input_data += f.read().strip()
        
    run_command.append(input_data)
    print(run_command)
    proc = subprocess.Popen(run_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate()
    if proc.returncode != 0:
        return ['error', error]
    else:
        return ['worked', output]
    



def add_language_extension(filename, language):
    language_mapping = {'java':'.java', 'python':'.py', 'c':'.c'}

    if language in language_mapping:
        return filename + language_mapping[language]
    else:
        raise Exception('language not supported')


def test(testname, username, language):
    filename = os.path.join(USER_DIR, username, testname, 'main')
    testfolder = os.path.join(TEST_DIR, testname)
    
    comp = compileCode(filename, language)
    
    if comp[0] != "worked":
        print("comp err")
        return [comp[1].strip()]
    
    
    
    test_cases = os.listdir(os.path.join(testfolder, 'input'))

    outputs = []
    
    #Results for run
    passes = 0
    fails = 0

    for i, test_case in enumerate(test_cases):
        out_str = "Test Case " + str(i+1) + ":\n" 
        output = run(filename, language, os.path.join(testfolder, 'input', test_case.strip()))
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
        if result:
            passes += 1
        else:
            fails +=1
    print ("passes: ", passes) 
    return outputs




