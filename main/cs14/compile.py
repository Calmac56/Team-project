import subprocess

def compileCode(filename, language):
    compile_command = ""
    if language == "java":
        compile_command = ("javac " + filename).split()
    if language == "python":
        return
    
    subprocess.call(compile_command)
    
def run(filename, language, args=""):
    run_command = ""
    if language == "java":
        run_command = ("java " + filename + " " + args).split()
    if language == "python":
        run_command = ("python " + filename + " " + args).split()
    run_command.append("> temp.txt")
    print(run_command)
    out = subprocess.check_output(run_command)
    with open("temp.txt", 'wb') as f:
        f.write(out)

def test(filename, testFile):
    with open(filename, "r") as f:
        with open(testFile, "r") as g:
            a = f.readline()
            b = g.readline()
            print(a, b)
            if (a != b):
                return False
    return True
