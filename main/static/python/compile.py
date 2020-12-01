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
        return
    try:
        subprocess.call(compile_command)
        print('Compiled')
    except:
        print('could not compile code')
    
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
    out = subprocess.check_output(run_command)
    return out


def add_language_extension(filename, language):
    language_mapping = {'java':'.java', 'python':'.py', 'c':'.c'}

    if language in language_mapping:
        return filename + language_mapping[language]
    else:
        raise Exception('language not supported')


def test(testname, username, language):
    filename = os.path.join(USER_DIR, username, testname, 'main')
    testfolder = os.path.join(TEST_DIR, testname)
    try:
        compileCode(filename, language)
    except:
        raise Exception('Compilation Error')
    
    test_cases = os.listdir(os.path.join(testfolder, 'input'))

    outputs = []

    for i, test_case in enumerate(test_cases):
        print(test_case)
        output = run(filename, language, os.path.join(testfolder, 'input', test_case.strip())).decode('ascii')
        with open(os.path.join(testfolder, 'output', test_case.strip()), 'r') as f:
            data = f.read()
            outputs.append(data.strip() == output.strip())
    return outputs




