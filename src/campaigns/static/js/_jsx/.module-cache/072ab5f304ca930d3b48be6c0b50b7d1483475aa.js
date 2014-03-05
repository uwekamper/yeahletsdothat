/**
 * @jsx React.DOM
 */

var app = app || {};

app.BasicInfoView = React.createClass({
    render: function () {
        return (
            React.DOM.h2(null, "Step1")
        );
    }
});

app.HeadCountView = React.createClass({
    render: function () {
        return(
            React.DOM.h2(null, "Head Count")
        );
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
                    React.DOM.div( {className:"col-xs-12"}
                    )
                )
            )
        );
    }
});