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
            var view = app.AppView(); //{model: User.profile()});
            React.renderComponent(view, $("#app-view")[0]);
        },

        step1: function() {
            var view = app.BasicInfoView(); //{model: User.profile()});
            React.renderComponent(view, $("#app-view")[0]);
        },

        step2: function() {
            var view = app.HeadCountView(); //{model: User.profile()});
            React.renderComponent(view, $("#app-view")[0]);
        }
    });


    app.router = new app.Router();



}(jQuery));