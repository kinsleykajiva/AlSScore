/**
 * This will contain all the javascript cutomem functions in addition to the other scripts that run by default
 * 
 */


//new BootstrapDialog().setTitle('Dialog instance 2').setMessage('Hi Orange!').setType(BootstrapDialog.TYPE_DANGER).open();



/***********************************************************************************************/


/***********************************************************************************************/

/*-------------------------------------------------------------------------------------------------------------------------*/



/*-------------------------------------------------------------------------------------------------------------------------*/
$("#submitResponse1").click(function(){

	let responseAnswer1TextArea = $("#responseAnswer1").val().trim();
	if(responseAnswer1TextArea == ''){
		BootstrapDialog.alert({
			title: 'Failed to submit ',
			message: 'No answers has been put !!',
			type: BootstrapDialog.TYPE_WARNING, 
			closable: true, 
			draggable: true, 
			buttonLabel: 'Ok'
		});

		return;
	}
	if( responseAnswer1TextArea.length > 0 && responseAnswer1TextArea.length < 3 ){
		BootstrapDialog.alert({
			title: 'Failed to submit ',
			message: 'Please put an anser that has greater than 3 characters in size',
			type: BootstrapDialog.TYPE_WARNING, 
			closable: true, 
			draggable: true, 
			buttonLabel: 'Ok'
		});

		return;
	}
	if( responseAnswer1TextArea.length > 4){
		showDialog();
		$.ajax({
					data: {
						posTResponse: responseAnswer1TextArea,
						posTQuestion_number: "2"
					},
					type: 'POST',
					url: '/getAnswer'
				}).done(function(response){
					hideDialog();
					
					if(response.response == "mark_score"){
								BootstrapDialog.alert({
									title: 'System Score ',
									message: 'You have scored ' + response.score + "\n Will be saved to the database later !!",
									type: BootstrapDialog.TYPE_WARNING, 
									closable: true, 
									draggable: true,
									buttonLabel: 'Close',
									callback: function(result) {
										// no call back yet kinsley !!!
										
									}
								});
							}
				});
	}

});
/*-------------------------------------------------------------------------------------------------------------------------*/

$("#BtnCreatAccount").click(function() {

	let password = $("#emailReg");
	let username = $("#emailReg");
	let userTyperegister = $("#userTyperegister").val();
	if (userTyperegister == "null") {
		BootstrapDialog.alert({
			title: 'Failed to submit ',
			message: 'Please choose to Register as Student or Teacher !',
			type: BootstrapDialog.TYPE_WARNING, 
			closable: true, 
			draggable: true, 
			buttonLabel: 'Ok'
		});

		return;
	}
	if (username.val().trim().length == '' && password.val().trim().length == '') {
		BootstrapDialog.alert({
			title: 'Failed to submit ',
			message: 'Please put your username and password !',
			type: BootstrapDialog.TYPE_WARNING,
			closable: true, 
			draggable: true,
			buttonLabel: 'Ok',
			callback: function(result) {

			}
		});
	} else {
		if (safe_tags_replace(username.val().trim()).length == '' && safe_tags_replace(password.val().trim()).length == '') {
			BootstrapDialog.alert({
				title: 'Failed to submit ',
				message: 'Please put a valid  username and password !',
				type: BootstrapDialog.TYPE_WARNING,
				closable: true, 
				draggable: true, 
				buttonLabel: 'Ok', 
				callback: function(result) {


				}
			});
		} else {
			if (!ValidateEmail(password.val().trim())) {
				BootstrapDialog.alert({
					title: 'Failed to submit ',
					message: 'Please put a valid email address !',
					type: BootstrapDialog.TYPE_DANGER, 
					closable: true, 
					draggable: true, 
					buttonLabel: 'Ok',
					callback: function(result) {
						$("#statusProcessing").val("<span style='color:red;'> Please put a valid email address  </span>");
					}
				});
			} else {
				showDialog();
				/*now sending the data to flask script*/
				
				$.ajax({
					data: {
						posTUsername: username.val().trim(),
						posTPassword: password.val().trim(),
						posTuserType: userTyperegister
					},
					type: 'POST',
					url: '/registerAjax'
				}).done(function(response) {
					
						hideDialog();					

						if (response.response == 'error') {

							BootstrapDialog.alert({
								title: 'Failed to submit ',
								message: 'An new Error',
								type: BootstrapDialog.TYPE_WARNING, 
								closable: true,
								draggable: true, 
								buttonLabel: 'Close',
								callback: function(result) {
									
								}
							});

						} else {
							if(response.response == "taken"){
								BootstrapDialog.alert({
									title: 'User Exists ',
									message: 'That user name already exists, Please chose another name',
									type: BootstrapDialog.TYPE_WARNING, 
									closable: true, 
									draggable: true,
									buttonLabel: 'Close',
									callback: function(result) {
										
										
									}
								});
							}
							if(response.response == "done"){

								
								if (response.user == 'Teacher'){
									window.location.href = "/teacher/";
								
								} else {
									window.location.href = "/student/";
								}
							}

					}
					//alert(response.response);
				});
		}

	}
}

});
/*-------------------------------------------------------------------------------------------------------------------------*/
$("#BtnLogin").click(function() {
	let username = $("#username");
	let password = $("#password");
	let userTypelogin = $("#userTypelogin").val();

	if (userTypelogin == "null") {
		BootstrapDialog.alert({
			title: 'Failed to submit ',
			message: 'Please choose to log in as Student or Teacher !',
			type: BootstrapDialog.TYPE_WARNING, 
			closable: true, 
			draggable: true, 
			buttonLabel: 'Ok'
		});

		return;
	}


	if (username.val().trim().length == '' && password.val().trim().length == '') {
		BootstrapDialog.alert({
			title: 'Failed to submit ',
			message: 'Please put your username and password !',
			type: BootstrapDialog.TYPE_WARNING, 
			closable: true, 
			draggable: true,
			buttonLabel: 'Ok',
			callback: function(result) {
				$("#statusProcessing").html("<span style='color:red;'>Please put your username and password </span>");
			}
		});

	} else {
		if (safe_tags_replace(username.val().trim()).length == '' && safe_tags_replace(password.val().trim()).length == '') {
			BootstrapDialog.alert({
				title: 'Failed to submit ',
				message: 'Please put a valid  username and password !',
				type: BootstrapDialog.TYPE_WARNING, 
				closable: true, 
				draggable: true,
				buttonLabel: 'Ok',
				callback: function(result) {
					$("#statusProcessing").val("<span style='color:red;'> Please put a valid  username and password </span>");

				}
			});
		} else {
			if (!ValidateEmail(username.val().trim())) {				
				BootstrapDialog.alert({
					title: 'Failed to submit ',
					message: 'Please put a valid email address !',
					type: BootstrapDialog.TYPE_DANGER, 
					closable: true, 
					draggable: true, 
					buttonLabel: 'Ok',
					callback: function(result) {
						$("#statusProcessing").val("<span style='color:red;'> Please put a valid email address  </span>");
					}
				});
			} else {
				showDialog();
				/*now sending the data to flask script*/
				$.ajax({
					data: {
						posTUsername: username.val().trim(),
						posTPassword: password.val().trim(),
						posTuserType: userTypelogin
					},
					type: 'POST',
					url: '/loginAjax'
				}).done(function(response) {
					hideDialog();
					if (response.response == 'error') {
						BootstrapDialog.alert({
							title: 'Failed to login ',
							message: 'An error occured please try again',
							type: BootstrapDialog.TYPE_DANGER, 
							closable: true, 
							draggable: true, 
							buttonLabel: 'Ok ', 
							callback: function(result) {
								// result will be true if button was click, while it will be false if users close the dialog directly.
								// alert('Result is: ' + result);
							}
						});
					} else {
						if (response.response == "exist") {
							if (response.user == 'Teacher') {
								window.location.href = "/teacher/";
							} else {
								window.location.href = "/student/";
							}
						}
						if (response.response == "new") {
							BootstrapDialog.alert({
								title: 'User not found ',
								message: 'Please register to log in',
								type: BootstrapDialog.TYPE_DANGER, 
								closable: true, 
								draggable: true, 
								buttonLabel: 'Ok , Retry',
								callback: function(result) {


								}
							});
						}
						if(response.response == "password_error"){
							BootstrapDialog.alert({
								title: 'Password Error ',
								message: 'Please use the correct password',
								type: BootstrapDialog.TYPE_DANGER, 
								closable: true, 
								draggable: true, 
								buttonLabel: 'Close',
								callback: function(result) {

									password.val(""); // clear the password section

								}
							});
						}
					}
					//alert(response.response);
				});
			}
		}
	}

});

/*-------------------------------------------------------------------------------------------------------------------------*/


/****************************************************************************/


function showDialog() {
	$.LoadingOverlay("show");
}


/***************************************************/

function hideDialog() {
	$.LoadingOverlay("hide");
}

/***********************************************************************************************/

/**This will validate email and retunr a boolena value*/
function ValidateEmail(inputText) {
	let mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
	if (inputText.match(mailformat)) {
		return true;
	} else {
		return false;
	}
}

/**to escape html elements to avoid injections*/
let tagsToReplace = {
	'&': '&amp;',
	'<': '&lt;',
	'>': '&gt;'
};
/***********************************************************************************************/
function __replaceTag(tag) {
	return tagsToReplace[tag] || tag;
}
/***********************************************************************************************/
function safe_tags_replace(str) {
	return str.replace(/[&<>]/g, __replaceTag);
}



console.log("This system was designed and developed by Kinsley Kajiva +263 737 531 075");