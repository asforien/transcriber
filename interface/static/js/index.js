var wavesurfer = Object.create(WaveSurfer);
var regions = [];
var selectedRegion = null;

document.addEventListener('DOMContentLoaded', function () {
	wavesurfer.init({
	    container: document.querySelector('#wave'),
	    waveColor: 'blue',
	    progressColor: 'purple'
	});

	wavesurfer.on('ready', function () {
		$.each(segments, function(index, segment) {
			var region = wavesurfer.addRegion({
				start: segment.start,
				end: segment.end,
				drag: false,
				resize: false,
				color: "rgba(0, 0, 0, 0.2)"
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
		selectedRegion.update({color: "rgba(0, 255, 0, 0.2)"});

        // var spectrogram = Object.create(WaveSurfer.Spectrogram);
        // spectrogram.init({
        //     wavesurfer: wavesurfer,
        //     container: '#spectrogram',
        //     fftSamples: 1024,
        //     pixelRatio: 2
        // });

	    //wavesurfer.play();
	});

	var target = $("#transcriptions");
	$("#wave wave").scroll(function() {
		target.prop("scrollLeft", this.scrollLeft);
	});

	wavesurfer.on('region-click', function(region, e) {
		e.stopPropagation();
		if (selectedRegion != null) {
			selectedRegion.update({color: "rgba(0, 0, 0, 0.2)"});
		}
		region.play();
		region.update({color: "rgba(0, 255, 0, 0.2)"});
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
	$("#btn-submit").click(submit);
});

function submit() {
	var results = [];
	$(".transcription").each(function(i) {
		var $radioBtn = $(this).find("label.active input");
		var result = $radioBtn.val();
		
		if (!result) {
			alert("Segment " + i + " is not annotated!");
			return false;
		}
		results.push($radioBtn.val());
	});
	console.log(results);
}