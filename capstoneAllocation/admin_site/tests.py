from django.test import TestCase
from .models import Admin

# Create your tests here.

class AdminModelTests(TestCase):

	# Login Status Testing

	def test_pass_loginSuccessStatus(self):
		admin = Admin(adminID='test1', adminPW='password')
		admin.validate('password')
		self.assertIs(admin.isLoggedIn(), True)

	def test_pass_loginFailureStatus(self):
		admin = Admin(adminID='test2', adminPW='password')
		admin.validate('wrongpw')
		self.assertIs(admin.isLoggedIn(), False)

	def test_pass_multipleLoginStatus(self):
		admin = Admin(adminID='test3', adminPW='password', status=1)
		outcome=admin.validate('password')
		self.assertIs((admin.isLoggedIn()==True and outcome==2), True)

	def test_fail_loginSuccessStatus(self):
		admin = Admin(adminID='test1', adminPW='password')
		admin.validate('password')
		self.assertIs(admin.isLoggedIn(), False)

	def test_fail_loginFailureStatus(self):
		admin = Admin(adminID='test2', adminPW='password')
		admin.validate('wrongpw')
		self.assertIs(admin.isLoggedIn(), True)

	def test_pass_multipleLoginStatus(self):
		admin = Admin(adminID='test3', adminPW='password', status=1)
		outcome=admin.validate('password')
		self.assertIs((admin.isLoggedIn()==False and outcome==2), True)

	# Login Validation Testing
		
	def test_pass_wrongPasswordLogin(self):
		admin = Admin(adminID='test1', adminPW='password')
		self.assertIs(admin.validate('wrongpw'), 0)

	def test_pass_emptyPasswordLogin(self):
		admin = Admin(adminID='test2', adminPW='password')
		self.assertIs(admin.validate(''), 0)

	def test_pass_correctPasswordLogin(self):
		admin = Admin(adminID='test3', adminPW='password')
		self.assertIs(admin.validate('password'), 1)

	def test_pass_multipleLogin(self):
		admin = Admin(adminID='test4', adminPW='password', status=1)
		self.assertIs(admin.validate('password'), 2)

	def test_fail_wrongPasswordLogin(self):
		admin = Admin(adminID='test1', adminPW='password')
		self.assertIs(admin.validate('wrongpw'), 1)

	def test_fail_emptyPasswordLogin(self):
		admin = Admin(adminID='test2', adminPW='password')
		self.assertIs(admin.validate(''), 1)

	def test_fail_correctPasswordLogin1(self):
		admin = Admin(adminID='test3', adminPW='password')
		self.assertIs(admin.validate('password'), 0)

	def test_fail_correctPasswordLogin2(self):
		admin = Admin(adminID='test4', adminPW='password')
		self.assertIs(admin.validate('password'), 2)

	def test_fail_multipleLogin(self):
		admin = Admin(adminID='test5', adminPW='password', status=1)
		self.assertIs(admin.validate('password'), 1)