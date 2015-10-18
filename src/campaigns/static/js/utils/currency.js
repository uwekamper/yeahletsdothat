'use strict';

var accounting = require('accounting');

module.exports = {
  format: function(value) {
    return accounting.formatNumber(value, 2);
  },
  unformat: function(str) {
    return accounting.unformat(str, '.');
  }
};