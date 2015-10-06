'use strict';

var EditActions = require('../actions/EditActions');
var React = require('react');

var Perk = React.createClass({

  editPerk: function(e) {
    e.preventDefault();
    var index = this.props.index;
    EditActions.editPerk(index);
  },

  uneditPerk: function(e) {
    e.preventDefault();
    var index = this.props.index;
    EditActions.uneditPerk(index);
  },


  renderStateOK: function() {
    var perk = this.props.perk;
    return(
      <div className="col-xs-6">
        <div className="perk-wrapper" ng-switch on="perk.available">
          <h3>{this.props.perk.title}</h3>
          <span className="perk-amount">{perk.amount} </span>
          <span className="perk-currency">{perk.currency}</span>
          <br/>
              <span className="perk-available" ng-switch-when="0">
                  <span className="perk-available-number">unlimited</span> perks available.
              </span>

              <span className="perk-available" ng-switch-when="1">
                  <span className="perk-available-number">{this.props.perk.available}</span>
                  perk available
              </span>

              <span className="perk-available" ng-switch-default>
                  <span className="perk-available-number">{this.props.perk.available}</span>
                  perks available
              </span>
          <br/>
          <br/>
          <a ng-click="ctrl.delete_perk($index)">Delete</a>
          <a onClick={this.editPerk}>Edit</a>
        </div>
      </div>
    );
  },

  renderStateEditable: function() {
    var perk = this.props.perk;
    var index = this.props.index;
    var idTitle = 'id-title-' + index;
    var idDescription = 'id-description-' + index;
    return (
      <div className="col-xs-12">
        <div className="perk-wrapper">
          <div className="input-group">
            <label htmlFor={idTitle}>Title</label>
            <input className="form-control perk-title-input"
                   id={idTitle} type="text" value={perk.title} />
          </div>
          <div className="input-group">
            <label htmlFor={idDescription}>Description <small>supports Markdown</small></label>
            <textarea className="form-control perk-text-input"
                      id={idDescription}>{perk.text}</textarea>
          </div>
          <div className="input-group">
            <input className="form-control perk-amount-input" type="text" value={perk.amount} />
            <span className="input-group-addon">{perk.currency}</span>
          </div>

          <div className="input-group">
            <input className="form-control perk-available-input" type="number"
                   ng-model="perk.available"/>
          </div>
          <br/>
          <a onClick={this.uneditPerk}>Done</a>
        </div>
      </div>
    );
  },

  renderStateDeleted: function() {
    return (
      <div ng-if="perk.state == 'DELETED' " className="col-xs-6">
        <div className="perk-wrapper perk-deleted">
          <h3>{ perk.title }</h3>
          <span className="perk-amount">{ perk.amount|currency }</span>
          <span className="perk-currency">{ ctrl.getCurrencyDisplay() }</span>
          <br/>
          <a ng-click="ctrl.undelete_perk($index)">Undo</a>
        </div>
      </div>
    );
  },

  render: function() {
    switch(this.props.perk.state) {
      case 'OK':
        return this.renderStateOK();
        break;
      case 'EDITABLE':
        return this.renderStateEditable();
        break;
      case 'DELETED':
        return this.renderStateDeleted();
        break;
    }
  }
});

module.exports = Perk;