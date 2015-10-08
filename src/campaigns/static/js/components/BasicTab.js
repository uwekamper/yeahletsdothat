'use strict';

var EditActions = require('../actions/EditActions');
var React = require('react');

var BasicTab = React.createClass({
  //getInitialState: function() {
  //  return {
  //    title: this.props.title,
  //    description: this.props.description
  //  };
  //},
  _changeTitle: function(event) {
    EditActions.updateCampaign({
       title: event.target.value
    });
  },
  _changeDescription: function(event) {
    EditActions.updateCampaign({
      description: event.target.value
    });
  },
  render: function() {
    return (
      <div className="row">
        <div className="col-xs-12">

          <h3>Basic Information</h3>

          <div className="form-group">
            <label for="id_title">Title</label>
            <input type="text" id="id_title" className="form-control"
              onChange={this._changeTitle} value={this.props.title} />
          </div>

          <div className="form-group">
            <label for="id_description">Description</label>
            <textarea id="id_description" rows="20" className="form-control"
                onChange={this._changeDescription} value={this.props.description} />
          </div>

        </div>
      </div>
    );
  }
});

module.exports = BasicTab;
