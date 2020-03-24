from django.test import TestCase
from .models import Team, Request
from datetime import datetime
from pytz import timezone

# Create your tests here.

class TeamModelTests(TestCase):

	# Login Status Testing

	def test_pass_loginSuccessStatus(self):
		team = Team(teamID='test1', teamPW='password')
		team.validate('password')
		self.assertIs(team.isLoggedIn(), True)

	def test_pass_loginFailureStatus(self):
		team = Team(teamID='test2', teamPW='password')
		team.validate('wrongpw')
		self.assertIs(team.isLoggedIn(), False)

	def test_pass_multipleLoginStatus(self):
		team = Team(teamID='test3', teamPW='password', status=1)
		outcome=team.validate('password')
		self.assertIs((team.isLoggedIn()==True and outcome==2), True)

	def test_fail_loginSuccessStatus(self):
		team = Team(teamID='test1', teamPW='password')
		team.validate('password')
		self.assertIs(team.isLoggedIn(), False)

	def test_fail_loginFailureStatus(self):
		team = Team(teamID='test2', teamPW='password')
		team.validate('wrongpw')
		self.assertIs(team.isLoggedIn(), True)

	def test_fail_multipleLoginStatus(self):
		team = Team(teamID='test3', teamPW='password', status=1)
		outcome=team.validate('password')
		self.assertIs((team.isLoggedIn()==False and outcome==2), True)

	# Login Validation Testing
		
	def test_pass_wrongPasswordLogin(self):
		team = Team(teamID='test1', teamPW='password')
		self.assertIs(team.validate('wrongpw'), 0)

	def test_pass_emptyPasswordLogin(self):
		team = Team(teamID='test2', teamPW='password')
		self.assertIs(team.validate(''), 0)

	def test_pass_correctPasswordLogin(self):
		team = Team(teamID='test3', teamPW='password')
		self.assertIs(team.validate('password'), 1)

	def test_pass_multipleLogin(self):
		team = Team(teamID='test4', teamPW='password', status=1)
		self.assertIs(team.validate('password'), 2)

	def test_fail_wrongPasswordLogin(self):
		team = Team(teamID='test1', teamPW='password')
		self.assertIs(team.validate('wrongpw'), 1)

	def test_fail_emptyPasswordLogin(self):
		team = Team(teamID='test2', teamPW='password')
		self.assertIs(team.validate(''), 1)

	def test_fail_correctPasswordLogin1(self):
		team = Team(teamID='test3', teamPW='password')
		self.assertIs(team.validate('password'), 0)

	def test_fail_correctPasswordLogin2(self):
		team = Team(teamID='test4', teamPW='password')
		self.assertIs(team.validate('password'), 2)

	def test_fail_multipleLogin(self):
		team = Team(teamID='test5', teamPW='password', status=1)
		self.assertIs(team.validate('password'), 1)


class RequestModelTests(TestCase):

	def test_pass_projectName(self):
		dict = {'prototypeType': '1:1', 'prototypeLength': 1.5, 'prototypeWidth': 1.5, 'prototypeHeight': 1.5, 'showcaseLength': 1.5, 'showcaseWidth': 1.5, 'showcaseHeight': 1.5, 'representativeEmail': 'capstone1@capstone.com', 'projectName': 'capstone2020001', 'pedestalDescription': 'test', 'others': 'test', 'powerpoints': 0.0, 'bigPedestals': 0.0, 'smallPedestals': 1.0, 'monitors': 0.0, 'TVs': 0.0, 'tables': 1.0, 'chairs': 2.0, 'HDMIAdaptors': 1.0, 'reqDateTime': datetime.now(timezone('Asia/Singapore'))}
		req = Request(teamID='test1')
		req.inputDetails(dict)
		self.assertIs(req.projectName, dict['projectName'])

	def test_fail_projectName(self):
		dict = {'prototypeType': '1:1', 'prototypeLength': 1.5, 'prototypeWidth': 1.5, 'prototypeHeight': 1.5, 'showcaseLength': 1.5, 'showcaseWidth': 1.5, 'showcaseHeight': 1.5, 'representativeEmail': 'capstone1@capstone.com', 'projectName': 'capstone2020001', 'pedestalDescription': 'test', 'others': 'test', 'powerpoints': 0.0, 'bigPedestals': 0.0, 'smallPedestals': 1.0, 'monitors': 0.0, 'TVs': 0.0, 'tables': 1.0, 'chairs': 2.0, 'HDMIAdaptors': 1.0, 'reqDateTime': datetime.now(timezone('Asia/Singapore'))}
		req = Request(teamID='test1')
		req.inputDetails(dict)
		self.assertIs((req.projectName!=dict['projectName']), True)
