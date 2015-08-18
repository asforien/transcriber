var wavesurfer = Object.create(WaveSurfer);

var segments = [
	{ start: 0.10, end: 0.159 },
	//{ start: 0.16, end: 0.289 },
	{ start: 0.29, end: 0.329 },
	//{ start: 0.33, end: 0.509 },

	{ start: 0.95, end: 1.009 },
	//{ start: 1.01, end: 1.209 },
	{ start: 1.23, end: 1.309 },
	//{ start: 1.31, end: 1.359 },
	{ start: 1.36, end: 1.509 },
]

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
