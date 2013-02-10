import unittest
import sys

from views import *

SUCCESS  = 1
ERR_BAD_CREDENTIALS = -1
ERR_USER_EXISTS = -2
ERR_BAD_USERNAME = -3
ERR_BAD_PASSWORD = -4

class UnitTests(unittest.TestCase):

	def setUp(self):
		reset()

	def testAddSingleUser(self):
		self.assertEquals(SUCCESS, add("user1", "password"))
	
	def testAddSameUser(self):
		self.assertEquals(SUCCESS, add("user1", "password"))
		self.assertEquals(ERR_USER_EXISTS, add("user1", "password"))
		self.assertEquals(ERR_USER_EXISTS, add("user1", "password"))

	def testAddMultipleUser(self):
		self.assertEquals(SUCCESS, add("user1", "password"))
		self.assertEquals(SUCCESS, add("user2", "password"))
		self.assertEquals(SUCCESS, add("user3", "password"))
	
	def testAddUserWithEmptyUsername(self):
		self.assertEquals(ERR_BAD_USERNAME, add("", "password"))

	def testAddUserWithEmptyPassword(self):
		self.assertEquals(SUCCESS, add("user1", ""))
	
	def testAddUserWithLongUsername(self):
		self.assertEquals(ERR_BAD_USERNAME, add("user1"*128, "password"))
	
	def testAddUserWithLongPassword(self):
		self.assertEquals(ERR_BAD_PASSWORD, add("user1", "password"*128))
	
	def testLoginSingleUserOneTime(self):
		add("user1", "password")
		self.assertEquals(2, login("user1", "password"))

	def testLoginSingleUserMultipleTimes(self):
		add("user1", "password")
		login("user1", "password")
		login("user1", "password")
		login("user1", "password")
		login("user1", "password")
		login("user1", "password")
		login("user1", "password")
		self.assertEquals(8, login("user1", "password"))
	
	def testLoginMultipleUsersOneTime(self):
		add("user1", "password")
		add("user2", "password")
		add("user3", "password")
		self.assertEquals(2, login("user1", "password"))
		self.assertEquals(2, login("user2", "password"))
		self.assertEquals(2, login("user3", "password"))
		
	def testLoginMultipleUsersMultipleTimes(self):
		add("user1", "password")
		add("user2", "password")
		add("user3", "password")
		login("user1", "password")
		login("user1", "password")
		self.assertEquals(4, login("user1", "password"))
		self.assertEquals(2, login("user2", "password"))
		login("user3", "password")
		login("user3", "password")
		login("user3", "password")
		login("user3", "password")
		login("user3", "password")
		login("user3", "password")
		login("user3", "password")
		self.assertEquals(9, login("user3", "password"))
		
	def testLoginWithEmptyUsername(self):
		self.assertEquals(ERR_BAD_USERNAME, login("", "password"))

	def testLoginWithEmptyPassword(self):
		add("user1", "")
		self.assertEquals(2, login("user1", ""))
	
	def testLoginWithLongUsername(self):
		self.assertEquals(ERR_BAD_USERNAME, login("user1"*128, "password"))
	
	def testLoginWithLongPassword(self):
		self.assertEquals(ERR_BAD_PASSWORD, login("user1", "password"*128))
		
	def testLoginWithWrongPassword(self):
		add("user1", "password")
		self.assertEquals(ERR_BAD_CREDENTIALS, login("user1", "password1"))

if __name__ == "__main__":
	unittest.main()