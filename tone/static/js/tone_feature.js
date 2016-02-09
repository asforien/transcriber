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
			var result = $(this).data("value");
			
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

	$("#transcriptions").on("mouseenter mouseleave", ".transcription", function(e) {
		if (e.type == "mouseenter") {
			$(this).find(".transcription-menu").addClass("active")
		} else {
			$(this).find(".transcription-menu").removeClass("active")
			$(this).find(".feature-rising-menu, .feature-level-menu, .feature-falling-menu").hide()
			$(this).find(".feature-main-menu").show()
		}
	});

	$("#transcriptions").on("click", ".btn-rising-menu", function() {
		$menu = $(this).closest(".transcription-menu");
		$menu.find(".feature-rising-menu").show();
		$menu.find(".feature-main-menu").hide();
	});

	$("#transcriptions").on("click", ".btn-level-menu", function() {
		$menu = $(this).closest(".transcription-menu");
		$menu.find(".feature-level-menu").show();
		$menu.find(".feature-main-menu").hide();
	});

	$("#transcriptions").on("click", ".btn-falling-menu", function() {
		$menu = $(this).closest(".transcription-menu");
		$menu.find(".feature-falling-menu").show();
		$menu.find(".feature-main-menu").hide();
	});

	$("#transcriptions").on("click", ".tone-feature-btn", function() {
		var result = $(this).data("value")
		var container = $(this).closest(".transcription").find(".transcription-value");
		setTranscription(container, result);
		$menu = $(this).closest(".transcription-menu");
		$menu.find(".feature-rising-menu, .feature-level-menu, .feature-falling-menu").hide();
		$menu.find(".feature-main-menu").show();
		$menu.removeClass("active");
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

var repr = ["", "HL", "HR", "ML", "LF", "LR", "LL"]

function setTranscription($container, result) {
	result = result + "";
	var tone_feature = repr[result];
	$container.html(tone_feature)
		.data("value", result)
		.removeClass("tone-bg-hr tone-bg-lr tone-bg-hl tone-bg-ml tone-bg-ll tone-bg-lf incomplete")
		.addClass("tone-bg-" + tone_feature.toLowerCase());
}