'use strict';

var updateCampaign = require('../actions/EditActions').updateCampaign;
var Datetime = require('react-datetime');
var DateTimePicker = require('./DateTimePicker');
var React = require('react');

var DateTab = React.createClass({
  _changeStartDate: function(startDate) {
    console.log(startDate);
    updateCampaign({start_date: startDate});
  },
  _changeEndDate: function(endDate) {
    updateCampaign({end_date: endDate});
  },
  onIsPrivateChange: function(event) {
    debugger;
    updateCampaign({is_private: jQuery(event.target).is(':checked')});
  },

  render: function() {

    return (
      <div className="row">
        <div className="col-xs-12">
          <h3>Dates</h3>

          <div className="form-group">
            <label for="id_start_date">Start date and time</label>
            <div className='input-group date' id='datetimepicker3'>
              <DateTimePicker value={this.props.start_date} onChange={this._changeStartDate} />
              <span className="input-group-addon">
                <span className="glyphicon glyphicon-calendar"></span>
              </span>
            </div>
          </div>

          <div className="form-group">
            <label for="id_end_date">End date and time</label>
            <div className='input-group date' id='datetimepicker4'>
              <DateTimePicker value={this.props.end_date} onChange={this._changeEndDate} />
              <span className="input-group-addon">
                <span className="glyphicon glyphicon-calendar"></span>
              </span>
            </div>
          </div>

          <h3>Preferences</h3>

          <div className="form-group">
            <label for="id_is_private">
              <input type="checkbox" id="id_is_private" name="is_private"
                     ng-model="ctrl.campaign.is_private" value
                     onChange={this.onIsPrivateChange} />
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
