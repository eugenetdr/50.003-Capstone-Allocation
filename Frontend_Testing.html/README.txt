Three python files to run for all the System level tests:

1. website_selenium.py: this will run 20/custom specified number of tests as specified in constants.py, for the student side input.
2. student_route_testing.py: recursively tests the student side page flow, along with the fuzzed inputs for the form inputs.

NOTE: This will submit the form even though the inputs are bad, but in real life it wont, since the form button is disabled while
any input is incorrect. Selenium is able to click on the button even if its disabled, real people cannot.

3. admin_route_testing.py: recursively tests the admin side page flow, along with the random edits to the edit floorplan page.