
//3 types of functions: email, string, number
function stringListener(string, test_type){
  
    if (string.validity.valid && (string.length!=0) && (string!='')) {
      // In case there is an error message visible, if the field
      // is valid, we remove the error message.
      return true;
    }
    else {
      // If there is still an error, show the correct error
      if(test_type == 0){
        return false;
      }
      else{
        return showStringError(string);
      }
    }
}

function numberListener(numerical, test_type){

    if (numerical.validity.valid && (numerical.value >= 0.0)) {
      // is valid, we remove the error message.
      return true;
    }
    else {
      // If there is still an error, show the correct error
      if(test_type == 0){
        return false;
      }
      else{
        return showNumberError(numerical);
      }
    }

}

function emailListener(email, test_type){

    if (email.validity.valid && /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email.value) && (email.length!=0)) {
        // In case there is an error message visible, if the field
        // is valid, we remove the error message.
        return true;
    }
    else {
        // If there is still an error, show the correct error
        if(test_type == 0){
          return false;
        }
        else{
          return showEmailError(email);
        }
    }
}

//redundant now
function showEmailError(email, ErrorObject) {
  if(email.validity.valueMissing) {
    // If the field is empty
    // display the following error message.
    return('You need to enter an e-mail address.');
  } else if(email.validity.typeMismatch) {
    // If the field doesn't contain an email address
    // display the following error message.
    return('Entered value needs to be an e-mail address.');
  } else if(email.validity.tooShort) {
    // If the data is too short
    // display the following error message.
    return('Too less characters.');
  }
  else{
    return('Generic Email Error');
  }

  // Set the styling appropriately
  ErrorObject.className = 'error active';
}

function showStringError(string){
    if(string.validity.valueMissing) {
        // If the field is empty
        // display the following error message.
        return('You need to enter a text.');
        } else if(string.validity.typeMismatch) {
        // If the field doesn't contain an email address
        // display the following error message.
        return('Entered value needs to be a valid text.');  
        }
        else{
          return('Generic String Error')
        }
}

function showNumberError(numerical){
    if(numerical.value<0){
        ErrorObject.textContent = 'You need to enter a non-negative number.';
    }
        else if(numerical.validity.valueMissing) {
        // If the field is empty
        // display the following error message.
        return('You need to enter a number.');
        } else if(numerical.validity.typeMismatch) {
        // If the field doesn't contain an email address
        // display the following error message.
        return('Entered value needs to be a valid number.');  
        }
        else{
        return('Generic Number Error');
        }
      }

//Functions to help us test the the above functions

function assertTestError(expectedValue, actualValue, i){
  pass = "Test " + String(i) + " passed!";
  fail = "Test " + String(i) + " failed!";
  if(expectedValue!=actualValue){
    console.log(fail);
  }
  else{
    console.log(pass);
  }
}

function multTests(inputObj, inputs, expected_outputs, test_type){
var integer = 0;
  for (integer = 0; integer<inputs.length; integer++){
    inputObj.value = inputs[integer];
    assertTestError(expected_outputs[integer], emailListener(inputObj, test_type), integer);
  }
}

/*
We will be performing black box and white box tests on 2 sets of functions:
a. The initial checking functions
b. The checking function + the error handling function

1. Black Box testing: 
We just know in general what the code is supposed to do.

a. First checking function: 
-email - Try inputting wrong email formats and see what is returned. Try blank inputs. Try emails with spaces in them
-string - try blank inputs
-numbers - try blank inputs, strings, alphanumeric, numbers with spaces in them, decimal numbers

b. Linked functions:
-email - check if correct mistake is identified
-string - check if correct mistake is identified
-number - check if correct mistake is identified

2. White Box Testing: See how the code works, bombard it with test cases that violate/conform to the specific conditions being checked for
a. First Checking fns:
email - input values that are correct, and then values that go against the regex format. Values that have 0 length, and ones that have. 
string - values that have 0 length, and ones that have. 
number - check if value is negative or not.

b. Linked functions - The coverage would be the same as above, so we will leave this out.
*/

var emailInput = document.createElement("INPUT");
emailInput.type = "email"

var stringInput = document.createElement("INPUT");
stringInput.type = "text"

var numberInput = document.createElement("INPUT");
numberInput.type = "number"

//test type 0 indicates initial checking function test. test type 1 indicates linked function test

console.log("Starting Black Box Testing!");

console.log("Testing intial checking functions!")

email_inputs_bb_0 = ["no mail", "haha@@@mail", "rahul@.com", "blah@gmail.com", "rahul@gmail.com", "student@sutd.outlook.com"]
email_expected_outputs_bb_0 = [false, false, false, true, true, true]

multTests(emailInput, email_inputs_bb_0, email_expected_outputs_bb_0, 0);

string_inputs_bb_0 = ["", "valid string 1", "what even", "valid string 2"]
string_expected_outputs_bb_0 = [false, true, true, true]

multTests(stringInput, string_inputs_bb_0, string_expected_outputs_bb_0, 0);

number_inputs_bb_0 = ["", "abc", "gdf", 12, 23, 24]
number_expected_outputs_bb_0 = [false, false, false, true, true, true]

multTests(numberInput, number_inputs_bb_0, number_expected_outputs_bb_0, 0);

console.log("Testing linked functions!")

email_inputs_bb_1 = ["", "aj@com", "2", 3, "rahulbhatta@gmail.com", "boya@outlook.com"]
email_expected_outputs_bb_1 = ['You need to enter an e-mail address.', 'Too less characters.', 'Entered value needs to be an e-mail address.', 'Entered value needs to be an e-mail address.', true, true]

multTests(emailInput, email_inputs_bb_1, email_expected_outputs_bb_1, 1);

string_inputs_bb_1 = ["", 2, null, "validtext", "haha"]
string_expected_outputs_bb_1 = ['You need to enter a text.','Entered value needs to be a valid text.','You need to enter a text.',true, true]

multTests(stringInput, string_inputs_bb_1, string_expected_outputs_bb_1, 1);

/*
number_inputs_bb_1 = []
number_expected_outputs_bb_1 = []

multTests(numberInput, number_inputs_bb_1, number_expected_outputs_bb_1, 1);

print("Starting White Box Testing!")

print("Testing intial checking functions!")

email_inputs_wb_0 = []
email_expected_outputs_wb_0 = []

multTests(emailInput, email_inputs_wb_0, email_expected_outputs_wb_0, 0);

string_inputs_wb_0 = []
string_expected_outputs_wb_0 = []

multTests(stringInput, string_inputs_wb_0, string_expected_outputs_wb_0, 0);

number_inputs_wb_0 = []
number_expected_outputs_wb_0 = []

multTests(numberInput, number_inputs_wb_0, number_expected_outputs_wb_0, 0);
*/