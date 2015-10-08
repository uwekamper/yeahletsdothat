'use strict';

var enableCSRF = require('./utils/CSRFProtection')
var EditApp = require('./components/App')
var EditActions = require('./actions/EditActions')
var React = require('react');

enableCSRF($);

React.render(
  <EditApp />
  , document.getElementById('app')
);

function loadStuff() {
  var url = 'http://localhost:8000/yeah/rest/campaigns/p655SzwbICQ33UfR';
  $.ajax({
    url: url,
    success: function(data) {
      EditActions.updateREST(data);
    },
    error: function(data) {
      alert("AJAX ERROER");
    }
  });
}

loadStuff();

