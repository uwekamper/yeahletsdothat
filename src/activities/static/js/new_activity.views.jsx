/**
 * @jsx React.DOM
 */

var app = app || {};

app.BasicInfoView = React.createClass({
    render: function () {
        return (
            <h2>Step1</h2>
        );
    }
});

app.HeadCountView = React.createClass({
    render: function () {
        return(
            <h2>Head Count</h2>
        );
    }
})


app.AppView = React.createClass({
    render: function () {
        return(
            <div className='row'>
                <div className='col-xs-12'>
                    <ul className='nav nav-pills nav-justified'>
                        <li class="active"><a href="#step1" >Step 1</a></li>
                        <li><a href="#step2">Step 2</a></li>
                        <li><a href="#">Step 3</a></li>
                    </ul>
                </div>
            </div>
        );
    }
});
