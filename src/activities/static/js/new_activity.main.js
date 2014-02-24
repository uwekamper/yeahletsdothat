var app = app || {};

$(function ($) {
    'use strict';

    app.ActivityModel = Backbone.Model.extend({

    });

    app.Router = Backbone.Router.extend({
        routes: {
            "": "kick_off",
            "step1": "step1",
            "step2": "step2"
        },

        kick_off: function() {
            var view = new app.Wizard({initialStep: 'overview'}); //{model: User.profile()});
            React.renderComponent(view, $("#app-view")[0]);
        },
        step1: function() {
            var view = new app.Wizard({initialStep: 2}); //{model: User.profile()});
            React.renderComponent(view, $("#app-view")[0]);
        },
        step2: function() {
            var view = new app.AppView({initialStep: 3}); //{model: User.profile()});
            React.renderComponent(view, $("#app-view")[0]);
        }


    });


    app.router = new app.Router();



}(jQuery));