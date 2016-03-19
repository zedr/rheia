(function (NS, undefined) {
  "use strict";

  var $ = NS.jQuery,
    $approvedSign = $(
      '<span data-approved title="Approved" class="ok glyphicon glyphicon-ok-circle" aria-hidden="true">'
    ),
    $toApproveSign = $(
      '<span title="Not approved yet" class="attention glyphicon glyphicon-exclamation-sign">'
    );

  function post(url, data) {
    $.ajax({
      url: url,
      type: "POST",
      data: data,
      dataType: "json"
    })
  }

  function toggleApproval() {
    var url = $(this).attr("data-url"),
      $firstSpan = $(this).find("span").first();

    if (url) {
      if ($firstSpan.attr("data-approved") === undefined) {
        post(url, {"approved": true});
        $firstSpan.replaceWith($approvedSign.clone());
      } else {
        post(url, {"approved": false});
        $firstSpan.replaceWith($toApproveSign.clone())
      }
    }
  }

  /**
   * setup JQuery's AJAX methods to setup CSRF token in the request before sending it off.
   * http://stackoverflow.com/questions/5100539/django-csrf-check-failing-with-an-ajax-post-request
   */
  function getCookie(name) {
    var cookieValue = null,
      cookies = document.cookie.split(";"),
      cookiesLen = cookies.length,
      idx,
      cookie;

    if (document.cookie) {
      for (idx = 0; idx < cookiesLen; idx++) {
        cookie = $.trim(cookies[idx]);

        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }


  function _bindToButton(_, button) {
    $(button).click(toggleApproval);
  }

  function bindToButtons() {
    var $buttons = $(".btn-approval");

    $buttons.each(_bindToButton)
  }

  function initialise() {
    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
          xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
      }
    });
    bindToButtons();
  }

  $(NS.document).ready(initialise)

}(this));
