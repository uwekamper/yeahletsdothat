'use strict';

var enableCSRF = require('./utils/CSRFProtection');
var EditApp = require('./components/App');
var EditActions = require('./actions/EditActions');
var React = require('react');

enableCSRF($);

React.render(
  <EditApp />
  , document.getElementById('app')
);

function loadStuff() {
  var url = window.campaignUrl;
  $.ajax({
    url: url,
    success: function(data) {
      EditActions.updateREST(data);
    },
    error: function(data) {
      alert("AJAX ERROR");
    }
  });
}

loadStuff();

