import subprocess
import os
import sys
import shutil

path = os.path.join(os.getcwd(), "media", "tests")

def create_tests():
    confirmation = input("WARNING: this script will remove ALL current files in the tests directory. \nAre you sure you wish to continue? [y/n]")
    if confirmation == 'y':
        shutil.rmtree(path)
        
        input1 = '1\n2\n3\n4\n5\n6\n7\n8'
        output1 = '1\n4\n9\n16\n25\n36\n49\n64'

        input2 = '1\n3\n5\n7'
        output2 = '1\n6\n120\n5040'

        inputs = [input1,input2]
        outputs = [output1, output2]

        for i in range(1,3):
            currtestdir_name = "test" + str(i)
            currtestdir = os.path.join(path, currtestdir_name)
            inputdir = os.path.join(path, currtestdir_name, "input", "in.txt")
            outputdir = os.path.join(path, currtestdir_name, "output", "in.txt") 
            
            subprocess.run(["mkdir", path], stderr=subprocess.PIPE)
            subprocess.run(["mkdir", currtestdir_name], cwd=path)
            subprocess.run(["mkdir", "input"], cwd=currtestdir)
            subprocess.run(["mkdir", "output"], cwd=currtestdir)
            
            with open(inputdir, "w+") as f:
                f.write(inputs[i-1])
            
            with open(outputdir, "w+") as f:
                f.write(outputs[i-1])



def remove_tests():
    confirmation = input("WARNING: this script will remove ALL current files in the tests directory. \nAre you sure you wish to continue? [y/n]")
    if confirmation == 'y':
        shutil.rmtree(path)
        subprocess.run(["mkdir", path], stderr=subprocess.PIPE)

if __name__ == '__main__':
    globals()[sys.argv[1]]()
