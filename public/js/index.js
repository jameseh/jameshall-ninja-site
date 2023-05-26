$(document).ready(function() {
  var table = $("#posts");
  table.find("th").each(function() {
    $(this).css("width", $(this).width() + 10);
  });

  table.find("tbody tr").each(function() {
    if ($(this).height() > 100) {
      $(this).addClass("tall");
    }
  });

  table.on("scroll", function() {
    var $tallRows = $(this).find(".tall");

    if ($tallRows.length > 0) {
      var $firstTallRow = $tallRows.first();
      var $lastVisibleRow = $(this).find("tbody tr:visible:last");

      if ($firstTallRow.position().top < $lastVisibleRow.position().top) {
        $tallRows.each(function() {
          $(this).css("position", "absolute");
          $(this).css("top", $(this).position().top - $(this).height());
        });
      } else {
        $tallRows.each(function() {
          $(this).css("position", "static");
        });
      }
    }
  });
});
