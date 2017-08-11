function run($) {
  var fieldsTiedToFeaturedCards = ".quote, .bio, .interview_url";

  $(".featured").on('click', function() {
    if(!$("#id_featured").is(':checked')) {
      $(fieldsTiedToFeaturedCards).hide();
    } else {
      $(fieldsTiedToFeaturedCards).show();
    }
  });
}

django.jQuery(run.bind(django.jQuery));
