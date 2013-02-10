from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from models import User
import json

SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

def client(request):
	return render_to_response('client.html')

@csrf_exempt
def userLogin(request):
	data = json.loads(request.raw_post_data)
	u = data['user']
	p = data['password']
	if request.path == '/users/login':
		rtn = login(u, p)
	else:
		rtn = add(u, p)
	if rtn < 0:
		resp = {"errCode": rtn}
	else:
		resp = {"errCode": SUCCESS, "count": rtn}
	return HttpResponse(json.dumps(resp))
	
@csrf_exempt
def testAPI(request):
	if request.path == '/TESTAPI/resetFixture':
		rtn = TESTAPI_resetFixture()
	resp = {"errCode": rtn}
	return HttpResponse(json.dumps(resp))

def login(u, p):
	if len(u) > 128 or not u:
		return ERR_BAD_USERNAME
	
	try:
		result = User.objects.get(name=u)
	except User.DoesNotExist:
		return ERR_BAD_CREDENTIALS
	
	if result.password == p:
		result.count += 1
		result.save()
		return result.count
	else:
		return ERR_BAD_CREDENTIALS

def add(u, p):
	if len(u) > 128 or not u:
		return ERR_BAD_USERNAME
		
	if len(p) > 128:
		return ERR_BAD_PASSWORD
	
	try:
		result = User.objects.get(name=u)
	except User.DoesNotExist:
		User(name=u, password=p, count=1).save()
		return SUCCESS
	else:
		return ERR_USER_EXISTS

def TESTAPI_resetFixture():
	User.objects.all().delete()
	return 1