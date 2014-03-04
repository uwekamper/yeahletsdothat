/**
 * @jsx React.DOM
 */

var app = app || {};






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
