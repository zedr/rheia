(function (NS) {
  "use strict";

  var $ = NS.jQuery;

  function getCurrentTime() {
    var dt = new Date();

    return dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds();
  }

  function initialize() {
    function updateTime(event) {
      $(event.data).val(getCurrentTime);
    }

    if ($) {
      var $nowButton = $('<input type="button" value="now"></input>'),
        $startTimeInput = $("#id_start_time");

      $startTimeInput.after($nowButton);
      $nowButton.click($startTimeInput, updateTime);

    }
  }

  $(NS.document).ready(initialize);

}(this));
