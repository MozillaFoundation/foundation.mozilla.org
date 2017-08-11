(function($){
  $(function() {
    $('.sortable').sortable('option', 'stop', function(event, ui) {
      var indexes = [];
      var lineItems = ui.item.parent().find('> li');

      lineItems.each(function() {
        indexes.push($(this).find(':hidden[name="pk"]').val());
      });

      $.ajax({
        url: ui.item.find('a.admin_sorting_url').attr('href'),
        type: 'POST',
        data: { indexes: indexes.join(',') }
      });
    });
  });
})(django.jQuery);
