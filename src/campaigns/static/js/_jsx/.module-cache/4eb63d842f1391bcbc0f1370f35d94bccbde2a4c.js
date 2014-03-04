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

//<div className='row'>
//                <div className='col-xs-12'>
//                    <ul className='nav nav-pills nav-justified'>
//                        <li className='active'><a href="#step1" >Step 1</a></li>
//                        <li><a href="#step2">Step 2</a></li>
//                        <li><a href="#">Step 3</a></li>
//                    </ul>
//                </div>
//            </div>

app.AppView = React.createClass({
    render: function () {
        return(
            React.DOM.div(null, 
                React.DOM.h1(null, "Hallo!")
            )
        );
    }
});
