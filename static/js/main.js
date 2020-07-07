function showResults(results, map, markers) {
    // get results for each task
    const resultsIR = results['ir']
    const resultsLE = results['le']

    // show coordinates
    markers.clearLayers();
    resultsLE.forEach((coord, idx) => {
        // create the marker
        var marker = L.marker(coord);

        // label
        const labelContent = `
            <div>Rank: ${(idx+1).toString()}</div>
            <div>${coord.join(', ')}</div>
        `;
        marker.bindPopup(labelContent).openPopup();

        // add marker
        markers.addLayer(marker);
    })
    map.addLayer(markers);
    map.fitBounds(markers.getBounds());

    // show results
    $('#results').empty();
    resultsIR.forEach((result, idx) => {
        // check if is gold for border color
        const borderClass = ((result['is_gold']) ? 'border-success' : 'border-secondary'); // 'border-secondary'

        // create card content
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

        // create card expand modal
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
                        <div class="modal-body" style="max-height: 500px; overflow-y:auto;">
                            <p class="card-text">${result['summary']}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // create content for new-articles modal
        const cardnewsArticlesModalContent = []
        const newsArticles = result['news_articles']

        if (newsArticles.length > 0) {
            newsArticles.forEach((article, article_idx) => {
                cardnewsArticlesModalContent.push(`
                    <div class="card" id="cardNewsModalContent-${article_idx}">
                        <div class="card-body">
                            <h4 class="card-title">${article['title']}</h4>
                            <div style="display: flex; flex-direction: row; flex-wrap: nowrap; justify-content: space-between;">
                                <h6 class="card-subtitle mb-2 text-muted">Source: <a href="${article['source']}" target="_blank">${article['source']}</a></h6>
                                <h6 class="card-subtitle mb-2 text-muted">Date: ${article['date']}</h6>
                            </div>
                            <p class="card-text cut-text">${article['body']}</p>
                            <a href="${article['url']}" class="card-link" target="_blank">Read more</a>
                        </div>
                    </div>
                `)
            })
        } else {
            cardnewsArticlesModalContent.push(`<p>No news articles.</p>`)
        }

        // create new-articles modal
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
                        <div class="modal-body" style="max-height: 500px; overflow-y:auto;">
                            ${cardnewsArticlesModalContent.join('')}
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
        // $('#infoModal').modal('show');

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

    $(document).ajaxSend(function() {
		$("#overlay").fadeIn(300);　
	});

    // submit image
    $('#submit_image').click(function(e) {
        e.preventDefault();
        $('#imageModal').modal('hide');
        var image_path = $('#imageSamples').find('.selected').attr('src');
        // $('#imageSamples').find('.selected').removeClass('selected');
        var lang = $('#imageLang').children("option:selected").val();
        var image_id = image_path.split('/').slice(-1)[0].split('_')[0];
        $.ajax({
            type : 'POST',
            url : '/mlm-demo/predict',
            data: {'query': image_path, 'lang': lang, 'sample_id': image_id},
            error: function(e) {
                setTimeout(function(){$("#overlay").fadeOut(300);}, 500);
                $('#ajaxAlertBody').empty();
                $('#ajaxAlertBody').append(e.responseText);
                $('#ajaxAlert').modal('show');
                console.log(e);
            },
            success: function(results) {
                if (!jQuery.isEmptyObject(results)) { showResults(results, map, markers) }
                setTimeout(function(){$("#overlay").fadeOut(300);}, 500);
            }
        });
    });

    // submit uploaded image
    $('#submit_upload').click(function(e) {
        e.preventDefault();
        $('#uploadModal').modal('hide');
        // var uploadQuery = $('#query').val();
        var form_data = new FormData();
        form_data.append('file', $('#uploadImage').prop('files')[0]);
        form_data.append('lang', $('#uploadLang').children("option:selected").val());
        $.ajax({
            type : 'POST',
            url : '/mlm-demo/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            error: function(e) {
                setTimeout(function(){$("#overlay").fadeOut(300);}, 500);
                $('#ajaxAlertBody').empty();
                $('#ajaxAlertBody').append(e.responseText);
                $('#ajaxAlert').modal('show');
                console.log(e);
            },
            success: function(results) {
                if (!jQuery.isEmptyObject(results)) { showResults(results, map, markers) }
                setTimeout(function(){$("#overlay").fadeOut(300);}, 500);
            }
        });
    });
});
