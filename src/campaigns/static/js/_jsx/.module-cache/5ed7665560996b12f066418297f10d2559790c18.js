/**
 * @jsx React.DOM
 */

var app = app || {};

var MenuItem = React.createClass({displayName: 'MenuItem',
    handleMenuClick: function() {
        this.props.onAction();
    },
    render: function(){
        var active = this.props.isActive === true ? 'active' : '';
        return React.DOM.li(null, React.DOM.a( {className:active, href:"#", onClick:this.handleMenuClick}, this.props.data.text))
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

    getInitialState: function(){
        return {page: 'overview'};
    },
    render: function() {
        return (
            MenuList( {activeMenuItem:this.state.page, data:this.props.data, onAction:this.props.onAction} )
        );
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
    nextStep: function() {
        var step = this.state.currentStep + 1;
        if(step >= 4) {
            step = 1;
        }
        this.setState({currentStep: step});
    },
    menuItems: [
        {text: "Step 1", page: "overview"},
        {text: "Step 2", page: "detail"},
        {text: "Step 3", page: "bla"}
    ],
    render: function () {
        return(
            React.DOM.div(null, 
                React.DOM.div( {className:"row"}, 
                    React.DOM.div( {className:"col-xs-12"}, 
                        Menu( {data:this.menuItems, activeMenuItem:"overview", onAction:this.nextStep} )
                    )
                ),
                React.DOM.div( {className:"row"}, 
                    React.DOM.div( {className:"col-xs-12"}, 
                        " Step: ", this.state.currentStep 
                    )
                )
            )
        );
    }
});


