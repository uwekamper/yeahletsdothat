'use strict';

// React components
var EditActions = require('../actions/EditActions');
var Tabs = require('./Tabs');
var TabContent = require('./TabContent');
var EditStore = require('../stores/EditStore');
var MessageStore = require('../stores/MessageStore');

var React = require('react');

var EditApp = React.createClass({

  _onSave: function(e) {
    e.preventDefault();
    EditActions.saveCampaign();
  },

  _onMessageClick: function(e) {
    e.preventDefault();
    EditActions.hideMessage();
  },

  getInitialState: function() {
    return {
      pristine: true,
      message: 'Initial state message',
      show_message: false
    };
  },

  _onChange: function() {
    this.setState({
      pristine: EditStore.getIsPristine()
    });

  },
  _onMessageChange: function() {
    this.setState(MessageStore.getMessage());
  },

  // Add change listeners to stores
  componentDidMount: function() {
    EditStore.addChangeListener(this._onChange);
    MessageStore.addChangeListener(this._onMessageChange);
  },

  // Remove change listers from stores
  componentWillUnmount: function() {
    EditStore.removeChangeListener(this._onChange);
    MessageStore.removeChangeListener(this._onMessageChange);
  },

  // show a message above the whole thing
  renderMessage: function() {
    if (this.state.show_message) {
      return (
        <div className="alert alert-success alert-dismissible" role="alter">
          <button type="button" className="close" aria-label="Close"
                  onClick={this._onMessageClick}><span aria-hidden="true">&times;</span></button>
          <strong>Message:</strong> {this.state.message}
        </div>
      );
    }
  },

  // main rendering of the whole edit form app.
  render: function() {
    return (
      <div>
        {this.renderMessage()}
        <Tabs />
        <TabContent />
        <button type="button" className="btn btn-primary btn-lg"
                onClick={this._onSave} disabled={this.state.pristine}>Save</button>
      </div>
    );
  },

  _delete: function() {
    console.log('Deleting item key: ' + this.props.index);
    EditActions.removeItem(this.props.index);
  }
});

module.exports = EditApp;