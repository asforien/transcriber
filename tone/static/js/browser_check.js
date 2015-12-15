$(function () {
	if (!(window.AudioContext || window.webkitAudioContext)) {
		$(".browser-unsupported").show();
	} else {
		$(".browser-supported").show();
	}
});