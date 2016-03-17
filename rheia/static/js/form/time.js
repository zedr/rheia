(function (NS) {
  "use strict";

  var $ = NS.jQuery,
    zF = function zeroFill(value) {
      var value_s = value.toString();
      return value_s.length === 1 ? "0" + value_s : value_s;
    };

  function getCurrentTime() {
    var dt = new Date();

    return (
      zF(dt.getHours()) + ":" + zF(dt.getMinutes()) + ":" + zF(dt.getSeconds())
    );
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
