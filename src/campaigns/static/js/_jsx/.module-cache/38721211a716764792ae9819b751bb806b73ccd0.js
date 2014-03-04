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
