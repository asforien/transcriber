var wavesurfer = Object.create(WaveSurfer);
var regions = [];
var selectedRegion = -1;

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

		setSelectedRegion(0);

		$(".transcription-answer").each(function(index, element) {
			setTranscription($(this), answers.charAt(index));
		});
	});

	var target = $("#transcriptions");
	$("#wave wave").scroll(function() {
		target.prop("scrollLeft", this.scrollLeft);
	});

	wavesurfer.on('region-click', function(region, e) {
		e.stopPropagation();
		region.play();
		setSelectedRegion(region.index);
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
		var result = $(this).html()
		var container = $(this).closest(".transcription").find(".transcription-value");
		setTranscription(container, result);
	});

	// Keyboard controls

	var isShiftDown = false;
	$(document).keydown(function(event) {
		switch(event.which) {
			case 16: // shift
				isShiftDown = true;
			break;

			case 32: // space
				regions[selectedRegion].play();
			break;

			case 37: // left
				if (selectedRegion > 0) {
					setSelectedRegion(selectedRegion - 1);
				}
			break;

			case 39: // right
				if (selectedRegion < regions.length - 1) {
					setSelectedRegion(selectedRegion + 1);
				}
			break;

			case 49: case 50: case 51: case 52: case 53: case 54: // 1-6
				if (!isShiftDown) {
					var choiceNum = event.which - 49;
					if (choiceNum < choices.length) {
						var result = choices[choiceNum];
						var container = $(".transcription-value.selected")
						setTranscription(container, result)
						container.addClass("selected")
					}
				} else {
					$("audio").get(event.which - 49).play();
				}
			break;
		}
	});

	$(document).keyup(function(event) {
		if (event.which == 16) { // shift
			isShiftDown = false;
		}
	});

	// prevent space from re-opening modal
	$(document).on('hidden.bs.modal', function() {
    	document.activeElement.blur();
	});

	$("#show-answers").click(function() {
		$(".transcription-answer").show();
		$(".transcription-menu").remove();
	});
});

function getRegionColor(index) {
	var regionColor1 = "rgba(128, 128, 128, 0.4)";
	var regionColor2 = "rgba(64, 64, 64, 0.4)";
	return index % 2 == 0 ? regionColor1 : regionColor2;
}

function setTranscription($container, result) {
	result = result + "";
	$container.html(result).removeClass("tone-bg-1 tone-bg-2 tone-bg-3 tone-bg-4 tone-bg-5 tone-bg-6")
	.addClass("tone-bg-" + result.toLowerCase());
}

function setSelectedRegion(index) {
	if (selectedRegion != -1) {
		regions[selectedRegion].update({color: getRegionColor(selectedRegion)});
		$(".transcription-value").eq(selectedRegion).removeClass("selected");
	}

	selectedRegion = index;
	var highlightColor = "rgba(153, 102, 153, 0.4)";
	regions[selectedRegion].update({color: highlightColor});
	$(".transcription-value").eq(selectedRegion).addClass("selected");
}