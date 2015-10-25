'use strict';

var AppDispatcher = require('../dispatcher/AppDispatcher');
var EditConstants = require('../constants/EditConstants');
var ObjectAssign = require('object-assign');
var EventEmitter = require('events').EventEmitter;

var CHANGE_EVENT = 'change';

var _message = {
  type: 'success',
  message: 'Everything is okay',
  show_message: false
};

// Define the public event listeners and getters that
// the views will use to listen for changes and retrieve
// the store
var MessageStore = ObjectAssign({}, EventEmitter.prototype, {
  addChangeListener: function(cb) {
    this.on(CHANGE_EVENT, cb);
  },

  removeChangeListener: function(cb) {
    this.removeListener(CHANGE_EVENT, cb);
  },

  getMessage: function() {
    return _message;
  }
});

AppDispatcher.register(function(payload) {
  var action = payload.action;
  switch (action.actionType) {

    case EditConstants.SHOW_MESSAGE:
      // Add the data defined in the TodoActions
      // which the View will pass as a payload
      _message.type = action.type;
      _message.message = action.message;
      _message.show_message = true;
      MessageStore.emit(CHANGE_EVENT);
      break;

     case EditConstants.HIDE_MESSAGE:
      // Add the data defined in the TodoActions
      // which the View will pass as a payload
      _message.show_message = false;
      MessageStore.emit(CHANGE_EVENT);
      break;
    default:
      return true;
  }
});

module.exports = MessageStore;