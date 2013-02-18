from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from models import User
import json
import os
import cgi
import tempfile
import traceback
import re

SUCCESS  = 1
ERR_BAD_CREDENTIALS = -1
ERR_USER_EXISTS = -2
ERR_BAD_USERNAME = -3
ERR_BAD_PASSWORD = -4

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
	return HttpResponse(content=json.dumps(resp), content_type='application/json')
	
@csrf_exempt
def testAPI(request):
	if request.path == '/TESTAPI/resetFixture':
		rtn = reset()
		resp = {"errCode": rtn}
	if request.path == "/TESTAPI/unitTests":
		resp = unitTests()
	return HttpResponse(content=json.dumps(resp), content_type='application/json')

def login(u, p):
	if len(u) > 128 or not u or len(p) > 128:
		return ERR_BAD_CREDENTIALS
	
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

def reset():
	User.objects.all().delete()
	return 1

def unitTests():
	(ofile, ofileName) = tempfile.mkstemp(prefix="userCounter")
	try:
		errMsg = ""
		output = ""
		totalTests = 0
		nrFailed   = 0
		while True:
			thisDir = os.path.dirname(os.path.abspath(__file__))
			cmd = "make -C "+thisDir+"/.. unit_tests >"+ofileName+" 2>&1"
			print "Executing "+cmd
			code = os.system(cmd)
			if code != 0:
				errMsg = "Error running command (code="+str(code)+"): "+cmd+"\n"
			try:
				ofileFile = open(ofileName, "r")
				output = ofileFile.read()
				ofileFile.close ()
			except:
				errMsg += "Error reading the output "+traceback.format_exc()
				break
			print "Got "+output
			m = re.search(r'Ran (\d+) tests', output)
			if not m:
				errMsg += "Cannot extract the number of tests\n"
				break
			totalTests = int(m.group(1))
			m = re.search('rFAILED.*\(failures=(\d+)\)', output)
			if m:
				nrFailures = int(m.group(1))
			break
		return {'output': errMsg + output, 'totalTests': totalTests, 'nrFailed': nrFailed}
	finally:
		os.unlink(ofileName)