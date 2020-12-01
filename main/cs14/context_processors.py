from cs14.models import Admin

def isAdmin(request):

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