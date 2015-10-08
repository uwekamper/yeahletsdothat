'use strict';

// React components
var EditActions = require('../actions/EditActions');
var Tabs = require('./Tabs');
var TabContent = require('./TabContent');

var React = require('react');

var EditApp = React.createClass({
  _onSave: function(e) {
    e.preventDefault();
    EditActions.saveCampaign();
  },
  render: function() {
      return (
          <div>
              <Tabs />
              <TabContent />
              <a href='#' onClick={this._onSave} className="btn">Save</a>
          </div>
      );
  },

  _delete: function() {
    console.log('Deleting item key: ' + this.props.index);
    EditActions.removeItem(this.props.index);
  }
});

module.exports = EditApp;