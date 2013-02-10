"""
Each file that starts with test... in this directory is scanned for subclasses of unittest.TestCase or testLib.RestTestCase
"""

import unittest
import os
from testLib import RestTestCase

SUCCESS = 1
ERR_BAD_CREDENTIALS = -1
ERR_USER_EXISTS = -2
ERR_BAD_USERNAME = -3
ERR_BAD_PASSWORD = -4

class TestBackend(RestTestCase):
	def assertResponse(self, respData, count = None, errCode = SUCCESS):
		expected = {'errCode' : errCode}
		if count is not None:
			expected['count']  = count
		self.assertDictEqual(expected, respData)
	
	def testAddSingleUser(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': 'password'})
		self.assertResponse(respData, count=1)

	def testAddMultipleUser(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': 'password'})
		self.assertResponse(respData, count=1)
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user2', 'password': 'password'})
		self.assertResponse(respData, count=1)
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user3', 'password': 'password'})
		self.assertResponse(respData, count=1)
	
	def testAddUserWithEmptyUsername(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': '', 'password': 'password'})
		self.assertResponse(respData, errCode=-3)

	def testAddUserWithEmptyPassword(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': ''})
		self.assertResponse(respData, count=1)
	
	def testAddUserWithLongUsername(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1'*128, 'password': 'password'})
		self.assertResponse(respData, errCode=-3)
	
	def testAddUserWithLongPassword(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': 'password'*128})
		self.assertResponse(respData, errCode=-4)
	
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
		self.assertResponse(respData, errCode=-3)

	def testLoginWithEmptyPassword(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': ''})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': ''})
		self.assertResponse(respData, count=2)
	
	def testLoginWithLongUsername(self):
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1'*128, 'password': 'password'})
		self.assertResponse(respData, errCode=-3)
	
	def testLoginWithLongPassword(self):
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password'*128})
		self.assertResponse(respData, errCode=-4)
		
	def testLoginWithWrongPassword(self):
		respData = self.makeRequest("/users/add", method="POST", data = {'user': 'user1', 'password': ''})
		respData = self.makeRequest("/users/login", method="POST", data = {'user': 'user1', 'password': 'password1'})
		self.assertResponse(respData, errCode=-1)