'use strict';

var EditStore = require('../stores/EditStore');
var EditActions = require('../actions/EditActions');
var Perkulator3000 = require('../components/Perkulator3000');
var Perk = require('./Perk');
var React = require('react');

function getPerksState() {
    return {
        perks: EditStore.getPerks()
    };
}

var PerksTab = React.createClass({

  getInitialState: function() {
    return getPerksState();
  },
  // Add change listeners to stores
  componentDidMount: function() {
      EditStore.addChangeListener(this._onChange);
  },

  // Remove change listers from stores
  componentWillUnmount: function() {
      EditStore.removeChangeListener(this._onChange);
  },

  addPerk: function(e) {
    e.preventDefault();
    EditActions.addPerk();
  },

  render: function() {
    // Create a list of <Perk /> components that will later be added.
    var perkComponents = [];
    for (var i=0; i < this.state.perks.length; i++) {
      var perk = this.state.perks[i];
      perkComponents.push(<Perk perk={perk} index={i}/>);
    }
    var campaignGoal = EditStore.getCampaign().goal;
    return (
      <div className="row">
        <div className="col-xs-6">
          <h3>Perks</h3>

          <span>
            {perkComponents}
          </span>

          <div className="col-xs-6">
              <div className="perk-wrapper perk-add" onClick={this.addPerk}>
                  <div className="perk-add-symbol">
                      <span className="glyphicon glyphicon-plus"></span>
                  </div>
                  Add perk
              </div>
          </div>

        </div>
        <Perkulator3000 perks={this.state.perks} goal={campaignGoal} />
      </div>
    );
  },
  // Method to setState based upon Store changes
  _onChange: function() {
      this.setState(getPerksState());
  }

});

module.exports = PerksTab;
