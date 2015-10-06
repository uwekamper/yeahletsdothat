'use strict';

// React components
var EditActions = require('../actions/EditActions');
var Tabs = require('./Tabs');
var TabContent = require('./TabContent');

var React = require('react');

var EditApp = React.createClass({

  render: function() {
      return (
          <div>
              <Tabs />
              <TabContent />
          </div>
      );
  },

  _delete: function() {
    console.log('Deleting item key: ' + this.props.index);
    EditActions.removeItem(this.props.index);
  }
});

module.exports = EditApp;