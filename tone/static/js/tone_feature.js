var wavesurfer = Object.create(WaveSurfer);
var regions = [];

var startTime = 0;

$(function () {
	startTime = new Date().getTime();

	wavesurfer.init({
		container: document.querySelector('#wave'),
		waveColor: '#888',
		progressColor: '#437',
	});

	wavesurfer.on('ready', function () {
		$.each(alignments, function(index, segment) {
			var region = wavesurfer.addRegion({
				start: segment[0],
				end: segment[0] + segment[1],
				drag: false,
				resize: false,
				color: getRegionColor(index),
			});
			regions[index] = region;
			region.index = index;
		});

		$("region").each(function() {
			$(".transcription").eq(0).clone()
			.css('left', $(this).position().left + $(this).width() / 2)
			.appendTo("#transcriptions");
		});
		$(".transcription").eq(0).remove();

		if (typeof previous_answers !== 'undefined') {
			$(".transcription-value").each(function(index, element) {
				setTranscription($(this), previous_answers.charAt(index))
			});
		}
	});

	var target = $("#transcriptions");
	$("#wave wave").scroll(function() {
		target.prop("scrollLeft", this.scrollLeft);
	});

	wavesurfer.on('region-click', function(region, e) {
		e.stopPropagation();
		region.play();
	});

	wavesurfer.load(audio_file_path);

	$("#btn-play").click(function() {
		wavesurfer.play(0);
	});
	$("#btn-pause-resume").click(function() {
		wavesurfer.playPause();
	});

	$("form").submit(function(event) {
		var timeTaken = (new Date().getTime() - startTime);
		console.log("Time taken: " + timeTaken + " milliseconds");
		$("#timeTaken").val(Math.floor(timeTaken/1000));

		var results = [];
		var complete = true;

		$(".transcription-value").each(function(i) {
			var result = $(this).html().trim();
			
			if (result == "?") {
				complete = false;
				$(this).addClass("incomplete");
			}
			results.push(result);
		});
		console.log(results.join(""));
		$("#result").val(results.join(""));

		if (!complete) {
			alert("There are incomplete segments");
			event.preventDefault();
		}
	});

	$("#transcriptions").on("click", ".transcription-menu button", function() {
		var result = $(this).data("value")
		var container = $(this).closest(".transcription-box").find(".transcription-value");
		setTranscription(container, result);
	});

	// prevent space from re-opening modal
	$(document).on('hidden.bs.modal', function() {
    	document.activeElement.blur();
	});
});

function getRegionColor(index) {
	var regionColor1 = "rgba(128, 128, 128, 0.4)";
	var regionColor2 = "rgba(64, 64, 64, 0.4)";
	return index % 2 == 0 ? regionColor1 : regionColor2;
}

function setTranscription($container, result) {
	result = result + "";
	$container.html(result).removeClass()
	.addClass("transcription-value tone-bg-" + result.toLowerCase());
}