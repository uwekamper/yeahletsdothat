'use strict';
var EditActions = require('../actions/EditActions');
var React = require('react');

var Tabs = React.createClass({

  switchToDate: function(e) {
    e.preventDefault();
    EditActions.switchTab('date');
  },
  switchToBasic: function(e) {
    e.preventDefault();
    EditActions.switchTab('basic');
  },
  switchToGoals: function(e) {
    e.preventDefault();
    EditActions.switchTab('goals');
  },
  switchToPerks: function(e) {
    e.preventDefault();
    EditActions.switchTab('perks');
  },
  render: function() {
    return (
          <div className="row">

            <div className="col-xs-3">
              <div className="progress-item">
                <a href="#tab-basic" onClick={this.switchToBasic}>
                  <h3 className="progress-number">1.</h3>
                  <p className="progress-description">Basic information</p>
                </a>
              </div>
            </div>

            <div className="col-xs-3">
              <div className="progress-item">
                <a href="#tab-dates" onClick={this.switchToDate}>
                  <h3 className="progress-number">2.</h3>
                  <p className="progress-description">Dates and Preferences</p>
                </a>
              </div>
            </div>

            <div className="col-xs-3">
              <div className="progress-item">
                <a href="#tab-goal" onClick={this.switchToGoals}>
                  <h3 className="progress-number">3.</h3>
                  <p className="progress-description">Campaign Goals</p>
                </a>
              </div>
            </div>

            <div className="col-xs-3">
              <div className="progress-item">
                <a href="#tab-perks" onClick={this.switchToPerks}>
                  <h3 className="progress-number">4.</h3>
                  <p className="progress-description">Prices and Perks</p>
                </a>
              </div>
            </div>

          </div>
    );
  }
});

module.exports = Tabs;

