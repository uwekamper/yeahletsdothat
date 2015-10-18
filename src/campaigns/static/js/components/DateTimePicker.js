'use strict';

var React = require('react');
var moment = require('moment');
var ReactDOM = require('react-dom');

var DateTimePicker = React.createClass({
  _onDateChange: function(event) {
    var value = moment(event.target.value).format('YYYY-MM-DDThh:mm');
    this.props.onChange(value);
  },

  render: function() {
    var localized_value = moment(this.props.value).format('LLL');

    // don't render anything, this is where we open the portal
    return <input type="text" className="form-control" value={localized_value}
                  onChange={this._onDateChange} onBlur={this._onDateChange} />;
  },

  componentDidMount: function() {
    this.node = ReactDOM.findDOMNode(this);

    // do the old-school stuff
    $(this.node).datetimepicker({format: 'LLL'});

    // start a new React render tree with our node and the children
    // passed in from above, this is the other side of the portal.
    //<input type="text" id="id_start_date" className="form-control"
    //            value={this.props.start_date} onChange={this._changeStartDate} date-time-picker />
    this.renderDialogContent();
  },

  renderDialogContent: function(props) {
    // if called from `componentWillReceiveProps`, then we use the new
    // props, otherwise use what we already have.
    props = props || this.props;

    // the code that used to be in `componentDidMount`
    ReactDOM.render(<div><input type="text" />{props.children}</div>, this.node);
  }
});

module.exports = DateTimePicker;