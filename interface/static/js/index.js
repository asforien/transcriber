var wavesurfer = Object.create(WaveSurfer);
var regions = [];
var selectedRegion = null;

document.addEventListener('DOMContentLoaded', function () {
	var regionColor1 = "rgba(0, 0, 0, 0.2)";
	var regionColor2 = "rgba(0, 0, 0, 0.3)";

	wavesurfer.init({
	    container: document.querySelector('#wave'),
	    waveColor: 'blue',
	    progressColor: 'purple'
	});

	wavesurfer.on('ready', function () {
		$.each(alignments, function(index, segment) {
			var region = wavesurfer.addRegion({
				start: segment[0],
				end: segment[0] + segment[1],
				drag: false,
				resize: false,
				color: index % 2 ? regionColor1 : regionColor2,
			});
			regions[index] = region;
		})

		$("region").each(function() {
        	$(".transcription").eq(0).clone()
        	.css('left', $(this).position().left + $(this).width() / 2 - 17)
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
		$(".transcription").each(function(i) {
			var $radioBtn = $(this).find("label.active input");
			var result = $radioBtn.val();
			
			if (!result) {
				alert("Segment " + i + " is not annotated!");
				event.preventDefault();
				return false;
			}
			results.push($radioBtn.val());
		});
		console.log(results.join(""));
		$("#result").val(results.join(""));
	});
});