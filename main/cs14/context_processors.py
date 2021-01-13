from cs14.models import Admin, Reviewer, Candidate

def isAdmin(request):
    auser = None
    try:
        if request.user.is_authenticated:
            auser = Admin.objects.get(user=request.user)
        else:
            auser = None
    except Admin.DoesNotExist:
        auser = None
    
    if auser == None:
        return {'isAdmin':False}
    else:
        return {'isAdmin': True}

def isReviewer(request):
    auser = None
    try:
        if request.user.is_authenticated:
            auser = Reviewer.objects.get(user=request.user)
    except Reviewer.DoesNotExist:
            auser = None
    
    if auser == None:
        return {'isReviewer': False}
    else:
        return {'isReviewer': True}

def isCandidate(request):
    auser = None
    try:
        if request.user.is_authenticated:
            auser = Candidate.objects.get(user=request.user)
    except Candidate.DoesNotExist:
        auser = None
    
    if auser == None:
        return {'isCandidate': False}
    else:
        return {'isCandidate': True}