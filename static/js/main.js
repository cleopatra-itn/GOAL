function showResults(results, map, markers) {
    // get results for each task
    const resultsIR = results['results_ir']
    const resultsLE = results['results_le']

    // show coordinates
    markers.clearLayers();
    resultsLE.forEach((result) => {
        Object.keys(result).forEach((key) => {
            // create the marker
            var marker = L.marker(result[key]);

            // label
            marker.bindPopup(key).openPopup();

            // add marker
            markers.addLayer(marker);
        })
    })
    map.addLayer(markers);

    // show results
    $('#results').empty();
    resultsIR.forEach((result, idx) => {
        // Check if is gold
        const borderClass = 'border-secondary' // ((result['is_gold']) ? 'border-success' : 'border-secondary');
        // Construct card content
        const cardContent = `
            <div class="card ${borderClass}" id="card-${idx}">
                <div class="card-body">
                    <h4 class="card-title">${result['label']}</h4>
                    <h6 class="card-subtitle mb-2 text-muted"><a href="https://www.wikidata.org/wiki/${result['id']}" target="_blank">${result['id']}</a></h6>
                    <p class="card-text cut-text">${result['summary']}</p>
                    <a href="" class="card-link" data-toggle="modal" data-target="#cardExpandModal-${idx}">Expand Card</a>
                    <a href="" class="card-link" data-toggle="modal" data-target="#cardNewsModal-${idx}">News Articles</a>
                </div>
            </div>
        `;

        // Construct card expand modal
        const cardExapndModal = `
            <div class="modal fade" id="cardExpandModal-${idx}" tabindex="-1" role="dialog" aria-labelledby="cardExpandModalLabel-${idx}" aria-hidden="true">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="flex-column">
                                <h5 class="modal-title" id="cardExpandModalLabel-${idx}">${result['label']}</h5>
                                <h6><a href="https://www.wikidata.org/wiki/${result['id']}" target="_blank">${result['id']}</a></h6>
                            </div>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <p class="card-text">${result['summary']}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Construct card new-articles modal
        const cardNewsModal = `
            <div class="modal fade" id="cardNewsModal-${idx}" tabindex="-1" role="dialog" aria-labelledby="cardNewsModalLabel-${idx}" aria-hidden="true">
                <div class="modal-dialog" role="document">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="flex-column">
                                <h5 class="modal-title" id="cardExpandModalLabel-${idx}">${result['label']}</h5>
                                <h6><a href="https://www.wikidata.org/wiki/${result['id']}" target="_blank">${result['id']}</a></h6>
                            </div>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <p>TODO</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Append newyly created card elements to the container
        $('#results').append(cardContent);
        $('#results').append(cardExapndModal);
        $('#results').append(cardNewsModal);
    })
}

$(document).ready(function() {
    var map = L.map('mapid').setView([51.1657, 10.4515], 2);
    var markers = L.markerClusterGroup();
    // page load
    $(window).on('load',function(){
        // show info modal
        $('#infoModal').modal('show');

        // create map
        // map and markers as global variables
        const layer = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
        });
        map.addLayer(layer);
        // L.marker([40.712, -74.006]).addTo(map) // .bindPopup("<strong></strong>").openPopup();
    });

    $('#imageSamples img').click(function(){
        $('.selected').removeClass('selected');
        $(this).addClass('selected');
    });

    // submit image
    $('#submit_image').click(function(e) {
        e.preventDefault();
        $('#imageModal').modal('hide');
        var image_path = $('#imageSamples').find('.selected').attr('src');
        $('#imageSamples').find('.selected').removeClass('selected');
        var langImage = $('#imageLang').children("option:selected").val();
        $.ajax({
            type : "POST",
            url : "/",
            data: {query: image_path, lang: langImage},
            success: function(results) {
                if (!jQuery.isEmptyObject(results)) { showResults(results, map, markers) }
            }
        });
    });

    // submit uploaded image
    $('#submit_upload').click(function(e) {
        e.preventDefault();
        $('#uploadModal').modal('hide');
        // var uploadQuery = $('#query').val();
        var langUpload = $('#uploadLang').children("option:selected").val();
        $.ajax({
            type : "POST",
            url : "/",
            data: {query: '', lang: langUpload},
            success: function(results) {
                if (!jQuery.isEmptyObject(results)) { showResults(results, map, markers) }
            }
        });
    });
});