$("form").submit(function(event) {

	var cipherEmail = encryptedString(key, $("#inputEmail").val(),
		RSAAPP.NoPadding, RSAAPP.RawEncoding
	);
	$("#encryptedEmail").val(window.btoa(cipherEmail));
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
		inputEmail: {
			required: true,
			maxlength: 255,
			email: true
		},
	},
	submitHandler: function() { // do not submit sensitive fields
		$("#inputName").attr("name", "");
		$("#inputEmail").attr("name", "");
		form.submit();
	}
});

var key;
$(function() {
	setMaxDigits(1000);
	key = new RSAKeyPair(
		"10001","10001",
		"B926FC189CD3A0612019DFDBF7D065A366583C8224605824A406D5E12689E8791973D995DB1B9E89FB439D6542586164C690DF13C211841A96EC061FD84496895F193F992194780A2E00AD3F30D0D5D7258A3DC6EE1F9093E10139EC8A45048F68B467D998327C4AA659372E7FA7BE7A719F4F582BDEC96426B90CBA212211FE58D51C11A2FA1BD416349018FF1B9237E90F388A78BCEFE5727FD93A93E9988DFAB7F49ACF2BAF3AC553D7ED76D5521E88528734A96DBC8223BEB02067EB678776C8497AD8863165B6500EFF9DFD30047154E66535E58482AEB36D71A36CB56F051B9E66EBC1F99E374BD02357ABF3A67135827968B03C3B025BE9C3CFB3CB5B",
		2048
	);
});

