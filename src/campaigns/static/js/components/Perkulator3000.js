'use strict';

var EditStore = require('../stores/EditStore');
var currency = require('../utils/currency');
var React = require('react');

var Perkulator3000 = React.createClass({
  /**
   * Calculate the total sum of all the perks times availability
   */
  getPerksTotal: function() {
    var sum = 0.0;
    for(var i = 0; i < this.state.perks.length; i++ ) {
        // TODO: check if perk is not deleted
        sum = sum + (this.state.perks[i].amount * this.state.perks[i].available)
    }
    return sum;
  },
  goalIsReachable: function() {
    return this.getPerksTotal() >= this.state.goal;
  },
  getInitialState: function() {
    return {
      perks: this.props.perks,
      goal: this.props.goal
    };
  },
  renderTableLine: function(perk) {
    return (
        <tr>
          <td>{ perk.title }</td>
          <td>{ perk.available }</td>

          <td>{ currency.format(perk.amount) }&nbsp;CURR</td>
          <td>{ currency.format(perk.amount * perk.available )}&nbsp;CURR</td>
        </tr>
    );
  },
  renderTable: function() {
    var lines = [];
    var perks = this.state.perks;
    for(var i = 0; i < perks.length; i++) {
      if (perks[i].ui_state != 'DELETED') {
        lines.push(this.renderTableLine(perks[i]));
      }
    }
    var tdStyle = {
      textAlign: 'right'
    };
    var total = currency.format(this.getPerksTotal());
    var goal = currency.format(this.state.goal);
    return (
      <table className="table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Available</th>
            <th>Price per Perk</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          {lines}
          <tr>
            <td colspan="3" style={tdStyle}>Total</td>
            <td>{ total } CURR</td>
          </tr>
          <tr>
            <td colspan="3" style={tdStyle}>Campaign goal</td>
            <td>{ goal }</td>
          </tr>
        </tbody>

      </table>
    );
  },
  renderAlert: function() {
    if (this.goalIsReachable()) {
      return (
        <div className="alert alert-success" role="alert">
          You have enough perks to meet your campaign goal.
        </div>
      );
    }
    else {
      return (
        <div className="alert alert-danger" role="alert">
          You do not have enough perks or your perks are not expensive enough.
          This campaign could never reach its goal. You can either lower your goal
          or add more perks and raise prices.
        </div>
      );
    }
  },
  render: function() {
    var myTable = this.renderTable();
    var myAlert = this.renderAlert();
    return (
      <div className="col-xs-6">
        <div className="row">
          <div className="col-xs-11">
            <h3>Perk-u-Lator 3000 (perk calculator)</h3>
            {myTable}
          </div>
        </div>
        <div className="row">
          <div className="col-xs-8 col-xs-offset-3">
            {myAlert}
          </div>
        </div>
      </div>
    );
  }

});

module.exports = Perkulator3000;
