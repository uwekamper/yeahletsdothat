var app = app || {};
var ENTER_KEY = 13;

$(function ($) {
    'use strict';

    var DescriptionView = Backbone.View.extend({
        el: '#form_content',
        render: function () {
            var data = {next: 'head_count'};
            var template = $('#base_template').html();
            var partials = {form: $('#details_template').html()};
            var html = Mustache.to_html(template, data, partials);
            this.$el.html(html);
        }
    });

    var HeadCountView = Backbone.View.extend({
        el: '#form_content',
        render: function () {
            var data = {next: ''};
            var template = $('#base_template').html();
            var partials = {form: $('#head_count_template').html()};
            var html = Mustache.to_html(template, data, partials);
            this.$el.html(html);
        }
    });

    var Router = Backbone.Router.extend({
        routes: {
            '': 'home',
            'head_count': 'head_count'
        }
    });

    var description_view = new DescriptionView();
    var head_count_view = new HeadCountView();
    var router = new Router();

    router.on('route:home', function () {
        description_view.render();
    });

    router.on('route:head_count', function () {
        head_count_view.render();
    })

    Backbone.history.start();

}(jQuery));