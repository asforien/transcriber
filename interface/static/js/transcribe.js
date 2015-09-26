var wavesurfer = Object.create(WaveSurfer);
var regions = [];
var selectedRegion = -1;

$(function () {
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
			.css('left', $(this).position().left + $(this).width() / 2 - 10)
			.appendTo("#transcriptions");
		});
		$(".transcription").eq(0).remove();

		setSelectedRegion(0);
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
		$(this).closest(".transcription").find(".transcription-value").html(result).removeClass("incomplete");
	});

	$("#subjectKey").val(getCookie("subjectKey"));

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
					$(".transcription-value.selected").html(event.which - 48);
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
});

function getCookie(cname) {
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i=0; i<ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1);
		if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
	}
	return "";
}

function getRegionColor(index) {
	var regionColor1 = "rgba(51, 102, 102, 0.4)";
	var regionColor2 = "rgba(68, 153, 204, 0.4)";
	return index % 2 == 0 ? regionColor1 : regionColor2;
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