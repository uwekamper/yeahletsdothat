'use strict';

var React = require('react');

var BasicTab = React.createClass({
    render: function() {
        return (
            <div className="row">
              <div className="col-xs-12">

                <h3>Basic Information</h3>

                <div className="form-group">
                  <label for="id_title">Title</label>
                  <input type="text" id="id_title" className="form-control" ng-model="ctrl.campaign.title"/>
                </div>

                <div className="form-group">
                  <label for="id_description">Description</label>
                  <textarea id="id_description" rows="20" className="form-control"
                            ng-model="ctrl.campaign.description"></textarea>
                </div>

              </div>
            </div>
        );
    }
});

module.exports = BasicTab;
