'use strict';

var gulp = require('gulp');
var gutil = require('gulp-util');
var buffer = require('vinyl-buffer');
var source = require('vinyl-source-stream');
var through = require('through2');
//var babelify = require('babelify');
var browserify = require('browserify');
var sourcemaps = require('gulp-sourcemaps');
var reactify = require('reactify');
//var webpack = require('webpack');
//var path = require('path');
//var loader = require('babel-loader');

// list every javascript source file here.
var scripts_sources = [
    './src/campaigns/static/js/main.js'
];
//
//gulp.task("webpack", function(callback) {
//    // run webpack
//    webpack({}, function(err, stats) {
//        if(err) throw new gutil.PluginError("webpack", err);
//        gutil.log("[webpack]", stats.toString({
//            // output options
//        }));
//        callback();
//    });
//});

gulp.task('scripts', function () {
    // set up the browserify instance on a task basis
    var b = browserify({
        entries: scripts_sources,
        debug: true,
        // defining transforms here will avoid crashing your stream
        transform: [reactify]
    });

    return b.bundle()
        .pipe(source('scripts.js'))
        .pipe(buffer())
        .pipe(sourcemaps.init({loadMaps: true}))
        // Add transformation tasks to the pipeline here.
        //.pipe(uglify())
        .on('error', gutil.log)
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest('./src/campaigns/static/dist/js/'));
});

// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch(scripts_sources, ['scripts']);
    //gulp.watch('scss/*.scss', ['sass']);
});