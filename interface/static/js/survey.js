$("form").submit(function(event) {
	document.cookie= "subjectKey=" + $("#inputEmail").val() + "; path=/";
});

$.validator.setDefaults({
	highlight: function(element) {
		$(element).closest('.form-group').addClass('has-error');
	},
	unhighlight: function(element) {
		$(element).closest('.form-group').removeClass('has-error');
	},
	errorElement: 'span',
	errorClass: 'help-block',
	errorPlacement: function(error, element) {
		if(element.parent('.input-group').length) {
			error.insertAfter(element.parent());
		} else {
			error.insertAfter(element);
		}
	}
});

$("form").validate({
	rules: {
		inputName: {
			required: true,
			maxlength: 255
		},
		inputEmail: {
			required: true,
			maxlength: 255,
			email: true
		},
		nativeLanguages: {
			required: true,
			maxlength: 255
		},
		otherLanguages: {
			maxlength: 255
		},
		gender: {
			required: true
		},
		age: {
			required: true,
			digits: true,
			range: [18, 127]
		}
	},
	errorPlacement: function(error, element) {
		if (element.is(":radio")) {
			error.appendTo(element.parents('.radio-container'));
		}
		else { // This is the default behavior 
			error.insertAfter(element);
		}
	}
});