/**
 * @jsx React.DOM
 */

var app = app || {};

var BasicInfoView = React.createClass({displayName: 'BasicInfoView',
    render: function () {
        return (
            React.DOM.h2(null, "BasicInfoView")
        );
    }
});

var HeadCountView = React.createClass({displayName: 'HeadCountView',
    render: function () {
        return(
            React.DOM.h2(null, "Head Count")
        );
    }
});

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
                        React.DOM.ul( {className:"nav nav-pills nav-justified"}, 
                            React.DOM.li( {className:"active"}, React.DOM.a( {href:"#step1"} , "Step 1")),
                            React.DOM.li(null, React.DOM.a( {href:"#step2"}, "Step 2")),
                            React.DOM.li(null, React.DOM.a( {href:"#"}, "Step 3"))
                        )
                    )
                ),
                React.DOM.div( {className:"row"}, 
                    React.DOM.div( {className:"col-xs-12"}, 
                        " Step ", this.props.step,": ",
                        BasicInfoView(null )
                    )
                )
            )
        );
    }
});