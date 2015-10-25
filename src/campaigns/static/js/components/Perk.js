'use strict';

var EditActions = require('../actions/EditActions');
var EditStore = require('../stores/EditStore');
var currency = require('../utils/currency');

var React = require('react');

var Perk = React.createClass({

  getInitialState: function() {
    var perk = this.props.perk;
    return {
      title: perk.title,
      text: perk.text,
      state: perk.state,
      amount: currency.format(perk.amount),
      currency: EditStore.getCampaign().currency,
      available: perk.available
    }
  },

  onChangeTitle: function(e) {
    this.setState({title: e.target.value});
  },

  onChangeDescription: function(e) {
    this.setState({description: e.target.value});
  },

  onChangeAmount: function(e) {
    this.setState({amount: e.target.value});
  },

  onChangeAvailable: function(e) {
    this.setState({available: e.target.value});
  },

  onBlurAmount: function(e) {
    var value = currency.unformat(e.target.value);
    this.setState({amount: currency.format(value)});
  },

  editPerk: function(e) {
    e.preventDefault();
    var index = this.props.index;
    EditActions.editPerk(index);
  },

  uneditPerk: function(e) {
    e.preventDefault();
    var index = this.props.index;
    var data = this.state;
    EditActions.uneditPerk(index, data);
  },

  deletePerk: function(e) {
    e.preventDefault();
    var index = this.props.index;
    EditActions.deletePerk(index);
  },

  undeletePerk: function(e) {
    e.preventDefault();
    var index = this.props.index;
    EditActions.undeletePerk(index);
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
          <a onClick={this.deletePerk}>Delete</a>
          <a onClick={this.editPerk}>Edit</a>
        </div>
      </div>
    );
  },

  renderStateEditable: function() {
    var perk = this.state;
    var index = this.props.index;
    var idTitle = 'id-title-' + index;
    var idDescription = 'id-description-' + index;
    return (
      <div className="col-xs-12">
        <div className="perk-wrapper">
          <div className="input-group">
            <label htmlFor={idTitle}>Title</label>
            <input type="text" className="form-control perk-title-input" id={idTitle}
                   value={this.state.title} onChange={this.onChangeTitle} />
          </div>
          <div className="input-group">
            <label htmlFor={idDescription}>Description <small>supports Markdown</small></label>
            <textarea className="form-control perk-text-input" onChange={this.onChangeDescription}
                      id={idDescription}>{this.state.text}</textarea>
          </div>
          <div className="input-group">
            <input className="form-control perk-amount-input" type="text"
                   value={this.state.amount} onChange={this.onChangeAmount} onBlur={this.onBlurAmount} />
            <span className="input-group-addon">{this.state.currency}</span>
          </div>

          <div className="input-group">
            <input className="form-control perk-available-input" type="number"
                   value={this.state.available} onChange={this.onChangeAvailable} />
          </div>
          <br/>
          <a onClick={this.uneditPerk}>Done</a>
        </div>
      </div>
    );
  },

  renderStateDeleted: function() {
    var perk = this.props.perk;
    return (
      <div className="col-xs-6">
        <div className="perk-wrapper perk-deleted">
          <h3>{perk.title}</h3>
          <span className="perk-amount">{perk.amount}</span>
          <span className="perk-currency">{perk.currency}</span>
          <br/>
          <a onClick={this.undeletePerk}>Undo</a>
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