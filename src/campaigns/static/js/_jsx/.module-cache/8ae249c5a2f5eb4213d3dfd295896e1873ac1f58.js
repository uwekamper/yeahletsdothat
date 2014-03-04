/**
 * @jsx React.DOM
 */

var app = app || {};

var MenuItem = React.createClass({displayName: 'MenuItem',

    handleMenuClick: function() {
        this.props.onAction(this.props.data.page);
    },
    render: function(){
        var active = this.props.isActive === true ? 'active' : '';
        return React.DOM.li( {className:active}, React.DOM.a(  {href:"#", onClick:this.handleMenuClick}, this.props.data.text))
    }

});

var MenuList = React.createClass({displayName: 'MenuList',
    render: function() {
        var _that = this, menuItemList = this.props.data.map(function(menuItem){
            var active = (_that.props.activeMenuItem === menuItem.page);

            return MenuItem( {isActive:active, data:menuItem, onAction:_that.props.onAction} );
        });

        return(
            React.DOM.ul( {className:"nav nav-pills nav-justified main-menu"}, 
                menuItemList
            )
        );
    }
});

var Menu = React.createClass({displayName: 'Menu',

    render: function() {
        return (
            MenuList( {activeMenuItem:this.props.activeMenuItem, data:this.props.data, onAction:this.props.onAction} )
        );
    }
});

var OverviewForm = React.createClass({displayName: 'OverviewForm',

    render: function() {
        return(
            React.DOM.form( {role:"form"}, 

                React.DOM.div( {className:"form-group"}, 
                    React.DOM.label( {for:"exampleInputEmail1"}),
                    React.DOM.input( {type:"email", className:"form-control", id:"exampleInputEmail1", placeholder:""} )
                ),

                React.DOM.div( {className:"form-group"}, 
                    React.DOM.label( {for:"exampleInputEmail1"}),
                    React.DOM.input( {type:"email", className:"form-control", id:"exampleInputEmail1", placeholder:""} )
                ),
                
                React.DOM.button( {type:"submit", class:"btn btn-default"}, "Submit")
            )
        );

    }

});

var Money = React.createClass({displayName: 'Money',

    render: function() {
        return React.DOM.div(null, React.DOM.h1(null, "Money"));
    }

});

var Headcount = React.createClass({displayName: 'Headcount',

    render: function() {
        return React.DOM.div(null, React.DOM.h1(null, "Headcount"));
    }

});


app.Menu = Menu;

app.Wizard = React.createClass({
    getInitialState: function() {
        return {currentStep: this.props.initialStep};
    },
    setCurrentStep: function(step) {
        this.setState({currentStep: step});
    },
    menuItems: [
        {text: "Step 1: Overview", page: "overview"},
        {text: "Step 2: Money", page: "money"},
        {text: "Step 3: Headcount", page: "headcount"}
    ],
    render: function () {
        var SubView;

        if(this.state.currentStep == 'overview') {
            SubView = OverviewForm;
        }
        else if(this.state.currentStep == 'money') {
            SubView = Money;
        }
        else if(this.state.currentStep == 'headcount') {
            SubView = Headcount;
        }

        return(
            React.DOM.div(null, 
                React.DOM.div( {className:"row"}, 
                    React.DOM.div( {className:"col-xs-12"}, 
                        Menu( {data:this.menuItems, activeMenuItem:this.state.currentStep, onAction:this.setCurrentStep} )
                    )
                ),
                React.DOM.div( {className:"row"}, 
                    React.DOM.div( {className:"col-xs-12"}, 
                        SubView(null )
                    )
                )
            )
        );
    }
});


