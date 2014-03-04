/**
 * @jsx React.DOM
 */

var app = app || {};

var MenuItem = React.createClass({

    handleMenuClick: function() {
        this.props.onAction(this.props.data.page);
    },
    render: function(){
        var active = this.props.isActive === true ? 'active' : '';
        return <li className={active}><a  href="#" onClick={this.handleMenuClick}>{this.props.data.text}</a></li>
    }

});

var MenuList = React.createClass({
    render: function() {
        var _that = this, menuItemList = this.props.data.map(function(menuItem){
            var active = (_that.props.activeMenuItem === menuItem.page);

            return <MenuItem isActive={active} data={menuItem} onAction={_that.props.onAction} />;
        });

        return(
            <ul className="nav nav-pills nav-justified main-menu">
                {menuItemList}
            </ul>
        );
    }
});

var Menu = React.createClass({

    render: function() {
        return (
            <MenuList activeMenuItem={this.props.activeMenuItem} data={this.props.data} onAction={this.props.onAction} />
        );
    }
});

var OverviewForm = React.createClass({

    render: function() {
        return(
            <form role="form">
                <div className="form-group">
                    <label for="id_title">Title</label>
                    <input type="email" className="form-control" id="id_title" placeholder="" />
                </div>
                <div className="form-group">
                    <label for="id_description">Description</label>
                    <input type="email" className="form-control" id="id_description" placeholder="" />
                </div>
                <button type="submit" class="btn btn-default">Submit</button>
            </form>
        );

    }

});

var Money = React.createClass({

    render: function() {
        return <div><h1>Money</h1></div>;
    }

});

var Headcount = React.createClass({

    render: function() {
        return <div><h1>Headcount</h1></div>;
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
    menuItems: [
        {text: "Step 1: Overview", page: "overview"},
        {text: "Step 2: Money", page: "money"},
        {text: "Step 3: Headcount", page: "headcount"}
    ],
    render: function () {
        var SubView;

        if(this.state.currentStep == 'overview') {
            SubView = OverviewForm;
        }
        else if(this.state.currentStep == 'money') {
            SubView = Money;
        }
        else if(this.state.currentStep == 'headcount') {
            SubView = Headcount;
        }

        return(
            <div>
                <div className='row'>
                    <div className='col-xs-12'>
                        <Menu data={this.menuItems} activeMenuItem={this.state.currentStep} onAction={this.setCurrentStep} />
                    </div>
                </div>
                <div className='row'>
                    <div className='col-xs-12'>
                        <SubView />
                    </div>
                </div>
            </div>
        );
    }
});


