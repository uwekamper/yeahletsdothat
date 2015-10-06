'use strict';

var React = require('react');

//{% for currency in currencies %}
//<option value="{{ currency.id }}">{{ currency.display_name }}</option>
//{% endfor %}

var GoalsTab = React.createClass({
    render: function() {
        return (
            <div className="row">
              <div className="col-xs-12">
                <h3>Bla</h3>
              </div>

                <div className="col-xs-6">
                  <div className="form-group">
                    <label for="id_goal">Campaign goal</label>
                    <input type="text" className="form-control" id="id_goal"
                           ng-model="ctrl.campaign.goal" format-as-currency />
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
