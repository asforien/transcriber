var wavesurfer = Object.create(WaveSurfer);
var regions = [];
var selectedRegion = null;

$(function () {
	var regionColor1 = "rgba(51, 102, 102, 0.4)";
	var regionColor2 = "rgba(68, 153, 204, 0.4)";

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
				color: index % 2 == 0 ? regionColor1 : regionColor2,
			});
			regions[index] = region;
		})

		$("region").each(function() {
        	$(".transcription").eq(0).clone()
        	.css('left', $(this).position().left + $(this).width() / 2 - 10)
        	.appendTo("#transcriptions");
		});
		$(".transcription").eq(0).remove();

		selectedRegion = regions[0];
	});

	var target = $("#transcriptions");
	$("#wave wave").scroll(function() {
		target.prop("scrollLeft", this.scrollLeft);
	});

	wavesurfer.on('region-click', function(region, e) {
		e.stopPropagation();
		if (selectedRegion != null) {
		}
		region.play();
		selectedRegion = region;
	})

	wavesurfer.load(audio_file_path);

	$("#btn-play").click(function() {
		wavesurfer.play();
	})
	$("#btn-pause-resume").click(function() {
		wavesurfer.playPause();
	})
	$("#btn-play-region").click(function() {
		selectedRegion.play();
	})

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
});