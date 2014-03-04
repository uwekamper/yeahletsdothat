/**
 * @jsx React.DOM
 */

var app = app || {};

var MenuItem = React.createClass({displayName: 'MenuItem',
    handleMenuClick: function() {
        alert("click " + this.props.data.text);
        // this.props.eventBus.emit('navigate.page.start', {page: this.props.data.page});
    },
    render: function(){
        var active = this.props.isActive === true ? 'active' : '';
        //return <li class={active}><a href="javascript:void(0)" onClick={this.handleMenuClick}><span class="hidden-tablet">{this.props.data.text}</span></a></li>;
        return React.DOM.li(null, React.DOM.a( {href:"#", onClick:this.handleMenuClick}, this.props.data.text))
    }
});

var MenuList = React.createClass({displayName: 'MenuList',
    render: function() {
        var _that = this, menuItemList = this.props.data.map(function(menuItem){
            var active = (_that.props.activeMenuItem === menuItem.page);
            return MenuItem( {isActive:active, data:menuItem, eventBus:_that.props.eventBus} );
        });

        return React.DOM.ul( {className:"nav nav-pills nav-justified main-menu"}, menuItemList);
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
            MenuList( {activeMenuItem:this.state.page, data:this.props.data, eventBus:this.props.eventBus})
        );
    }
});

app.AppView = React.createClass({
    getInitialState: function() {
        return {};
    },
    menuItems: [
        {text: "Overview2", page: "overview"},
        {text: "Detail", page: "detail"}
    ],
    render: function () {
        return(
            React.DOM.div(null, 
                React.DOM.div( {className:"row"}, 
                    React.DOM.div( {className:"col-xs-12"}, 
                        Menu( {data:this.menuItems} )
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
