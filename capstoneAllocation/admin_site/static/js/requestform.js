// There are many ways to pick a DOM node; here we get the form itself and the email
// input box, as well as the span element into which we will place the error message.

window.onload=function(){

//ensure the conditional fields are disabled by default, until the radio buttons are selected
document.getElementById('prototypeLength').disabled = true;document.getElementById('prototypeWidth').disabled = true;document.getElementById('prototypeHeight').disabled = true;
document.getElementById('showCaseLength').disabled = true;document.getElementById('showCaseWidth').disabled = true;document.getElementById('showCaseHeight').disabled = true;

const form  = document.getElementsByTagName('form')[0];

//Enter all the inputs you want to check for:

const submit = document.querySelectorAll("input[value='Submit Space Request']");

const email = document.getElementById('representativeEmail');
const projectName = document.getElementById('projectName');

const prototypeType1 = document.getElementById('prototypeType');
const prototypeType2 = document.getElementById('prototypeType2');
const prototypeType3 = document.getElementById('prototypeType3');
const prototypeType4 = document.getElementById('prototypeType4');
const prototypeType5 = document.getElementById('prototypeType5');
const prototypeCustom = document.getElementById('prototypeCustom');

const prototypeSize1 = document.getElementById('prototypeSize1');
const prototypeSize2 = document.getElementById('prototypeSize2');
const prototypeSize3 = document.getElementById('prototypeSize3');
const prototypeSize4 = document.getElementById('prototypeSize4');

const prototypeLength = document.getElementById('prototypeLength');
const prototypeWidth = document.getElementById('prototypeWidth');
const prototypeHeight = document.getElementById('prototypeHeight');

const showcaseSize1 = document.getElementById('showCaseSize1');
const showcaseSize2 = document.getElementById('showCaseSize2');
const showcaseSize3 = document.getElementById('showCaseSize3');
const showcaseSize4 = document.getElementById('showCaseSize4');

const showcaseLength = document.getElementById('showCaseLength');
const showcaseWidth = document.getElementById('showCaseWidth');
const showcaseHeight = document.getElementById('showCaseHeight');

const powerpoints = document.getElementById('powerpoints');
const bigPedestals = document.getElementById('bigPedestals');
const smallPedestals = document.getElementById('smallPedestals');
const pedestalDescription = document.getElementById('pedestalDescription');
const monitors = document.getElementById('monitors');
const TVs = document.getElementById('TVs');
const tables = document.getElementById('tables');
const chairs = document.getElementById('chairs');
const HDMIAdaptors = document.getElementById('HDMIAdaptors');
const others = document.getElementById('others');
const remarks = document.getElementById('remarks');



const emailError = document.querySelector('#representativeEmail + br + span.error');
const projectNameError = document.querySelector('#projectName + br + span.error');

const prototypeTypeError = document.querySelector('#prototypeType5 + br + span.error'); // for the type radio inputs
const prototypeCustomError = document.querySelector('#prototypeCustom + br + span.error'); // for the custom input

const prototypeSizeError = document.querySelector('#prototypeSize4 + span.error'); //for the size radio inputs
const prototypeLengthError = document.querySelector('#prototypeLength + br + span.error'); // for the custom input
const prototypeWidthError = document.querySelector('#prototypeWidth + br + span.error'); // for the custom input
const prototypeHeightError = document.querySelector('#prototypeHeight + br + span.error'); // for the custom input

const showcaseSizeError = document.querySelector('#showCaseSize4 + span.error'); //for the size radio input
const showcaseLengthError = document.querySelector('#showCaseLength + br + span.error'); // for the custom input
const showcaseWidthError = document.querySelector('#showCaseWidth + br + span.error'); // for the custom input
const showcaseHeightError = document.querySelector('#showCaseHeight + br + span.error'); // for the custom input

const powerpointsError = document.querySelector('#powerpoints + br + span.error');
const bigPedestalsError = document.querySelector('#bigPedestals + br + span.error');
const smallPedestalsError = document.querySelector('#smallPedestals + br + span.error');
const pedestalDescriptionError = document.querySelector('#pedestalDescription + br + span.error');
const monitorsError = document.querySelector('#monitors + br + span.error');
const TVsError = document.querySelector('#TVs + br + span.error');
const tablesError = document.querySelector('#tables + br + span.error');
const chairsError = document.querySelector('#chairs + br + span.error');
const HDMIAdaptorsError = document.querySelector('#HDMIAdaptors + br + span.error');
const othersError = document.querySelector('#others + br + span.error');
const remarksError = document.querySelector('#remarks + br + span.error');

//now use above functions to add the listeners to their corresponding objects

emailListener(email, emailError); stringListener(projectName, projectNameError); numberListener(prototypeLength, prototypeLengthError);
numberListener(prototypeWidth, prototypeWidthError); numberListener(prototypeHeight, prototypeHeightError); numberListener(showcaseLength, showcaseLengthError); numberListener(showcaseWidth, showcaseWidthError);
numberListener(showcaseHeight, showcaseHeightError); numberListener(powerpoints, powerpointsError); numberListener(bigPedestals, bigPedestalsError); numberListener(smallPedestals, smallPedestalsError);
stringListener(pedestalDescription, pedestalDescriptionError); numberListener(monitors, monitorsError); numberListener(TVs, TVsError); numberListener(tables, tablesError);
numberListener(chairs, chairsError); numberListener(HDMIAdaptors, HDMIAdaptorsError); stringListener(others, othersError); stringListener(remarks, remarksError);

stringListener(prototypeCustom, prototypeCustomError); 

form.addEventListener('submit', function (event) {
  // if the email field is valid, we let the form submit
  var flag = 0;
  //we need to handle the prototypeType, prototypeSize and showcaseSize separately
  if(!email.validity.valid) {showEmailError(email,emailError);flag = 1;} if(!projectName.validity.valid) {showStringError(projectName, projectNameError);flag = 1;} 
  if(!prototypeLength.validity.valid) {showNumberError(prototypeLength, prototypeLengthError);flag = 1;}
  if(!prototypeWidth.validity.valid) {showNumberError(prototypeWidth, prototypeWidthError);flag = 1;} if(!prototypeHeight.validity.valid) {showNumberError(prototypeHeight, prototypeHeightError);flag = 1;} 
  if(!showcaseLength.validity.valid) {showNumberError(showcaseLength, showcaseLengthError);flag = 1;} if(!showcaseWidth.validity.valid) {showNumberError(showcaseWidth, showcaseWidthError);flag = 1;}
  if(!showcaseHeight.validity.valid) {showNumberError(showcaseHeight, showcaseHeightError);flag = 1;} if(!powerpoints.validity.valid) {showNumberError(powerpoints, powerpointsError);flag = 1;} 
  if(!bigPedestals.validity.valid) {showNumberError(bigPedestals, bigPedestalsError);flag = 1;} if(!smallPedestals.validity.valid) {showNumberError(smallPedestals, smallPedestalsError);flag = 1;}
  if(!pedestalDescription.validity.valid) {showStringError(pedestalDescription, pedestalDescriptionError);flag = 1;} if(!monitors.validity.valid) {showNumberError(monitors, monitorsError);flag = 1;} 
  if(!TVs.validity.valid) {showNumberError(TVs, TVsError);flag = 1;} if(!tables.validity.valid) {showNumberError(tables, tablesError);flag = 1;}
  if(!chairs.validity.valid) {showNumberError(chairs, chairsError);flag = 1;} if(!HDMIAdaptors.validity.valid) {showNumberError(HDMIAdaptors, HDMIAdaptorsError);flag = 1;} 
  if(!others.validity.valid) {showStringError(others, othersError);flag = 1;} if(!remarks.validity.valid) {showStringError(remarks, remarksError);flag = 1;}
  //if(!prototypeType.validity.valid) {showStringError(prototypeType, prototypeTypeError);flag = 1;}
  // 
  // Then we prevent the form from being sent by canceling the event
  if(flag){
    event.preventDefault();
  }
});
}

//3 types of functions: email, string, number
function stringListener(string, ErrorObject){
    console.log("Now listening for string: ")
    console.log(string.id);
;

    string.addEventListener('input', function (event) {
        // Each time the user types something, we check if the
        // form fields are valid.
      
        if (string.validity.valid && (string.length!=0) && (string!='')) {
          // In case there is an error message visible, if the field
          // is valid, we remove the error message.
          ErrorObject.innerHTML = ''; // Reset the content of the message
          ErrorObject.className = 'error'; // Reset the visual state of the message
          submit.disabled = false;
        }
        else {
          // If there is still an error, show the correct error
          showStringError(string, ErrorObject);
          submit.disabled = true;
        }
      });
}

function numberListener(numerical, ErrorObject){
    console.log("Now listening for number: ")
    console.log(numerical.id);

    numerical.addEventListener('input', function (event) {
        // Each time the user types something, we check if the
        // form fields are valid.
        
      
        if (numerical.validity.valid && (numerical.value >= 0.0)) {
          // is valid, we remove the error message.
          ErrorObject.innerHTML = ''; // Reset the content of the message
          ErrorObject.className = 'error'; // Reset the visual state of the message
          submit.disabled = false;
        }
        else {
          // If there is still an error, show the correct error
          submit.disabled = true;
          showNumberError(numerical, ErrorObject);
        }
      });
}

function emailListener(email, ErrorObject){
    console.log("Now listening for email: ")

    email.addEventListener('input', function (event) {
    // Each time the user types something, we check if the
    // form fields are valid.

    if (email.validity.valid && /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email.value)) {
        // In case there is an error message visible, if the field
        // is valid, we remove the error message.
        ErrorObject.innerHTML = ''; // Reset the content of the message
        ErrorObject.className = 'error'; // Reset the visual state of the message
        submit.disabled = false;
    }
    else {
        // If there is still an error, show the correct error
        showEmailError(email, ErrorObject);
        submit.disabled = true;
    }
    });
}

//redundant now
function showEmailError(email, ErrorObject) {
  if(email.validity.valueMissing) {
    // If the field is empty
    // display the following error message.
    ErrorObject.textContent = 'You need to enter an e-mail address.';
  } else if(email.validity.typeMismatch) {
    // If the field doesn't contain an email address
    // display the following error message.
    ErrorObject.textContent = 'Entered value needs to be an e-mail address.';
  } else if(email.validity.tooShort) {
    // If the data is too short
    // display the following error message.
    ErrorObject.textContent = `Email should be at least ${ email.minLength } characters; you entered ${ email.value.length }.`;
  }

  // Set the styling appropriately
  ErrorObject.className = 'error active';
}

function showStringError(string, ErrorObject){
    if(string.validity.valueMissing) {
        // If the field is empty
        // display the following error message.
        ErrorObject.textContent = 'You need to enter a text.';
        } else if(string.validity.typeMismatch) {
        // If the field doesn't contain an email address
        // display the following error message.
        ErrorObject.textContent = 'Entered value needs to be a valid text.';  
        }
        // Set the styling appropriately
        ErrorObject.className = 'error active';
}

function showNumberError(numerical, ErrorObject){
    if(numerical.value<0){
        ErrorObject.textContent = 'You need to enter a non-negative number.';
    }
        else if(numerical.validity.valueMissing) {
        // If the field is empty
        // display the following error message.
        ErrorObject.textContent = 'You need to enter a number.';
        } else if(numerical.validity.typeMismatch) {
        // If the field doesn't contain an email address
        // display the following error message.
        ErrorObject.textContent = 'Entered value needs to be a valid number.';  
        }
        // Set the styling appropriately
        ErrorObject.className = 'error active';
}