from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from cs14.compile import *

def index(request):
    return render(request, 'cs14/index.html')

def codingPage(request):
    
    return render(request, 'cs14/codingPage.html')

def sendCode(request):
    if(request.method == 'POST'):

        temp = request.POST.get('codeArea')
        file = open("temp.py", "w")
        file.write(temp)
        file.close()
        
        #run the code and do the tests
        compileCode("temp.py", "python")
        run("temp.py", "python")
        results = test("temp.txt", "testFile1.txt")

    return render(request, 'cs14/codingPage.html', {'results':[str(results)], 'code':temp})