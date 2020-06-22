function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
  }

$(document).ready( function() {
    // lighttslider carusel
    $('#vertical').lightSlider({
        gallery:true,
        item:1,
        vertical:true,
        verticalHeight:295,
        vThumbWidth:50,
        thumbItem:8,
        thumbMargin:4,
        slideMargin:0
    });

    // submit text
    $('#submit_text').click(function(e) {
        e.preventDefault();
        var text = $('#query').val();
        $.ajax({
            type : "POST",
            url : "/",
            data: {text_query: text},
            success: function(answer) {
                $('#answer').html(answer);
            }
        });
    });
    // submit image
    $('#submit_image').click(function(e) {
        e.preventDefault();
        var image_path = $('#vertical').find('.active').find('img').attr('src');
        $.ajax({
            type : "POST",
            url : "/",
            data: {image_query: image_path},
            success: function(answer) {
                $('#answer').html(answer);
            }
        });
    });
    // submit upload
    $('#submit_upload').click(function(e) {
        e.preventDefault();
        var uploadQuery = $('#query').val();
        $.ajax({
            type : "POST",
            url : "/",
            data: {upload_query: uploadQuery},
            success: function(answer) {
                $('#answer').html(answer);
            }
        });
    });

    // show text on click
    $('.list-group').click(function(e) {
        e.preventDefault();
        $('.list-group a').removeClass('active');
        $(event.target).addClass('active');
        var label = $(event.target).text();
        $.ajax({
            type : "POST",
            url : "/",
            data: {get_summary: label},
            success: function(query) {
                $('.form-control').val(query);
            }
        });
    });
});