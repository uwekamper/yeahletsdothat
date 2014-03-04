/**
 * @jsx React.DOM
 */

var app = app || {};

var MenuItem = React.createClass({displayName: 'MenuItem',
    handleMenuClick: React.autoBind(function() {
        this.props.eventBus.emit('navigate.page.start', {page: this.props.data.page});
    }),
    render: function(){
        var active = this.props.isActive === true ? 'active' : '';
        return React.DOM.li( {class:active}, React.DOM.a( {href:"javascript:void(0)", onClick:this.handleMenuClick}, React.DOM.span( {class:"hidden-tablet"}, this.props.data.text)));
    }
});

var MenuList = React.createClass({displayName: 'MenuList',
    render: function() {
        var _that = this, menuItemList = this.props.data.map(function(menuItem){
            var active = (_that.props.activeMenuItem === menuItem.page);
            return MenuItem( {isActive:active, data:menuItem, eventBus:_that.props.eventBus} );
        });

        return React.DOM.ul( {class:"nav nav-tabs nav-stacked main-menu"}, menuItemList);
    }
});

var Menu = React.createClass({displayName: 'Menu',

    getInitialState: function(){
        return {page: 'overview'};
    },
    componentDidMount: function() {
        var _that = this;
        this.props.eventBus.on('navigate.page.finished', function(data) {
            _that.setState(data);
        });
    },
    render: function() {
        return (
            React.DOM.div( {class:"span2 main-menu-span"}, 
                React.DOM.div( {class:"nav-collapse sidebar-nav"}, 
                    MenuList( {activeMenuItem:this.state.page, data:this.props.data, eventBus:this.props.eventBus})
                )
            )
        );
    }
});





app.AppView = React.createClass({
    render: function () {
        return(
            React.DOM.div(null, 
                React.DOM.div( {className:"row"}, 
                    React.DOM.div( {className:"col-xs-12"}, 
                        " Menu "
                    )
                ),
                React.DOM.div( {className:"row"}, 
                    React.DOM.div( {className:"col-xs-12"}, 
                        " Step ", this.props.step,": "+
                        "basic "
                    )
                )
            )
        );
    }
});
