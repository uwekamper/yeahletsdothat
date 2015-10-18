'use strict';

var updateCampaign = require('../actions/EditActions').updateCampaign;
var React = require('react');
var currency = require('../utils/currency');

var GoalsTab = React.createClass({
  _onGoalDone: function(event) {
    var value = currency.unformat(event.target.value);
    this.setState({goal: currency.format(value)});
    updateCampaign({goal: value});
  },
  _onGoalChange: function(event) {
    this.setState({goal: event.target.value});
  },
  getInitialState: function () {
    return {
      goal: currency.format(this.props.goal)
    };
  },
  render: function() {
    // var formatted = currency.format(this.state.goal);
    return (
        <div className="row">
          <div className="col-xs-12">
            <h3>Campaign Goal</h3>
          </div>

            <div className="col-xs-6">
              <div className="form-group">
                <label for="id_goal">Campaign goal</label>
                <input type="text" className="form-control" id="id_goal"
                       value={this.state.goal} onChange={this._onGoalChange}
                       onBlur={this._onGoalDone} />
              </div>
            </div>

            <div className="col-xs-6">
              <div className="form-group">
                <label for="id_goal">Currency</label>
                <select className="form-control" id="id_goal" ng-model="ctrl.campaign.currency">
                    <option value="bla">Blub</option>
                </select>
              </div>
            </div>
        </div>
    );
  }
});

module.exports = GoalsTab;
