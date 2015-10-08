'use strict';

var updateCampaign = require('../actions/EditActions').updateCampaign;
var React = require('react');

var DateTab = React.createClass({
  _changeStartDate: function(event) {
    updateCampaign({start_date: event.target.value});
  },
  _changeEndDate: function(event) {
    updateCampaign({end_date: event.target.value});
  },
  render: function() {
    return (
      <div className="row">
        <div className="col-xs-12">
          <h3>Dates</h3>

          <div className="form-group">
            <label for="id_start_date">Start date and time</label>
            <div className='input-group date' id='datetimepicker3'>
              <input type="text" id="id_start_date" className="form-control"
                value={this.props.start_date} onChange={this._changeStartDate} date-time-picker />
              <span className="input-group-addon"><span className="glyphicon glyphicon-calendar"></span>
              </span>
            </div>
          </div>

          <div className="form-group">
            <label for="id_end_date">End date and time</label>
            <div className='input-group date' id='datetimepicker3'>

              <input type="text" id="id_end_date" className="form-control" name="is_private"
                value={this.props.end_date} onChange={this._changeEndDate} date-time-picker />
              <span className="input-group-addon"><span className="glyphicon glyphicon-calendar"></span>
              </span>
            </div>
          </div>

          <h3>Preferences</h3>

          <div className="form-group">
            <label for="id_is_private">
              <input type="checkbox" id="id_is_private" name="is_private"
                     ng-model="ctrl.campaign.is_private"/>
              Make this campaign private.
            </label>
          </div>
          <div className="form-group">
            <label for="id_end_when_goal_reached">
              <input type="checkbox" id="id_end_when_goal_reached" name="is_private"/>
              End this campaign before the end date when the campaign goal is reached.
            </label>
          </div>
        </div>
      </div>
    );
  }
});

module.exports = DateTab;
