$(function () {
	$(".tone-container").click(function() {
		$(this).find("audio").get(0).play();
	});
});