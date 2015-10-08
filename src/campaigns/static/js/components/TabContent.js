'use strict';

var EditStore = require('../stores/EditStore');
var BasicTab = require('./BasicTab');
var DateTab = require('./DateTab');
var GoalsTab = require('./GoalsTab');
var PerksTab = require('./PerksTab');
var React = require('react');

function getEditState() {
    return {
        activeTab: EditStore.getActiveTab()
    };
}

var TabContent = React.createClass({
    getInitialState: function() {
        return getEditState();
    },

    // Add change listeners to stores
    componentDidMount: function() {
        EditStore.addChangeListener(this._onChange);
    },

    // Remove change listers from stores
    componentWillUnmount: function() {
        EditStore.removeChangeListener(this._onChange);
    },


    render: function() {
        var activeTab;
        var campaign = EditStore.getCampaign();
        switch (this.state.activeTab) {
            case 'basic':
                activeTab = <BasicTab title={campaign.title} description={campaign.description}/>
                break;
            case 'date':
                activeTab = <DateTab start_date={campaign.start_date} end_date={campaign.end_date}/>
                break;
            case 'goals':
                activeTab = <GoalsTab />
                break;
            case 'perks':
                activeTab = <PerksTab />
                break;
        }

        return (
            <div className="row">
                <div className="col-xs-12">
                  <div role="tabpanel">
                    <div className="tab-content">
                      <div role="tabpanel" className="tab-pane active blafasel" id="tab-basic">
                        {activeTab}
                      </div>
                    </div>
                  </div>
                </div>
            </div>
        );
    },

    // Method to setState based upon Store changes
    _onChange: function() {
        this.setState(getEditState());
    }
});

module.exports = TabContent;

