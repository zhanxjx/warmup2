import unittest
import os
from testLib import RestTestCase

SUCCESS = 1
ERR_BAD_CREDENTIALS = -1
ERR_USER_EXISTS = -2
ERR_BAD_USERNAME = -3
ERR_BAD_PASSWORD = -4

class TestUnit(RestTestCase):

	def testUnit(self):
		respData = self.makeRequest("/TESTAPI/unitTests", method="POST")
		self.assertTrue('output' in respData)
		print ("Unit tests output:\n" + "\n***** ".join(respData['output'].split("\n")))
		self.assertTrue('totalTests' in respData)
		print "***** Reported " + str(respData['totalTests']) + " unit tests"
		minimumTests = 10
		self.assertTrue(respData['totalTests'] >= minimumTests, "at least "+str(minimumTests)+" unit tests. Found only " + str(respData['totalTests']) + ".")
		self.assertEquals(0, respData['nrFailed'])

class TestBackend(RestTestCase):
	def assertResponse(self, respData, count = None, errCode = SUCCESS):
		expected = {'errCode': errCode}
		if count is not None:
			expected['count'] = count
		self.assertDictEqual(expected, respData)
	
	def testAddSingleUser(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': 'password'})
		self.assertResponse(respData, count=1)
	
	def testAddSameUser(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': 'password'})
		self.assertResponse(respData, count=1)
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': 'password'})
		self.assertResponse(respData, errCode=ERR_USER_EXISTS)
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': 'password'})
		self.assertResponse(respData, errCode=ERR_USER_EXISTS)

	def testAddMultipleUser(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': 'password'})
		self.assertResponse(respData, count=1)
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user2', 'password': 'password'})
		self.assertResponse(respData, count=1)
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user3', 'password': 'password'})
		self.assertResponse(respData, count=1)
	
	def testAddUserWithEmptyUsername(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': '', 'password': 'password'})
		self.assertResponse(respData, errCode=ERR_BAD_USERNAME)

	def testAddUserWithEmptyPassword(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': ''})
		self.assertResponse(respData, count=1)
	
	def testAddUserWithLongUsername(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1'*128, 'password': 'password'})
		self.assertResponse(respData, errCode=ERR_BAD_USERNAME)
	
	def testAddUserWithLongPassword(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': 'password'*128})
		self.assertResponse(respData, errCode=ERR_BAD_PASSWORD)
	
	def testLoginSingleUserOneTime(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'})
		self.assertResponse(respData, count=2)

	def testLoginSingleUserMultipleTimes(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'})
		self.assertResponse(respData, count=8)
	
	def testLoginMultipleUsersOneTime(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': 'password'})
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user2', 'password': 'password'})
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user3', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'})
		self.assertResponse(respData, count=2)
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user2', 'password': 'password'})
		self.assertResponse(respData, count=2)
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user3', 'password': 'password'})
		self.assertResponse(respData, count=2)
		
	def testLoginMultipleUsersMultipleTimes(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': 'password'})
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user2', 'password': 'password'})
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user3', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'})
		self.assertResponse(respData, count=4)
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user2', 'password': 'password'})
		self.assertResponse(respData, count=2)
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user3', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user3', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user3', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user3', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user3', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user3', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user3', 'password': 'password'})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user3', 'password': 'password'})
		self.assertResponse(respData, count=9)
		
	def testLoginWithEmptyUsername(self):
		respData = self.makeRequest("/users/login", method="POST", data = {'user': '', 'password': 'password'})
		self.assertResponse(respData, errCode=ERR_BAD_CREDENTIALS)

	def testLoginWithEmptyPassword(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': ''})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': ''})
		self.assertResponse(respData, count=2)
	
	def testLoginWithLongUsername(self):
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1'*128, 'password': 'password'})
		self.assertResponse(respData, errCode=ERR_BAD_CREDENTIALS)
	
	def testLoginWithLongPassword(self):
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'*128})
		self.assertResponse(respData, errCode=ERR_BAD_CREDENTIALS)
		
	def testLoginWithWrongPassword(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': ''})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password1'})
		self.assertResponse(respData, errCode=ERR_BAD_CREDENTIALS)