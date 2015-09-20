'use strict';

var browserify = require('browserify');
var gulp = require('gulp');
var buffer = require('vinyl-buffer');
var source = require('vinyl-source-stream');

gulp.task('default', function() {
    // gulp expects tasks to return a stream, so we create one here.
    var b = browserify({
        entries: './src/campaigns/static/js/app.js',
        debug: true
    });
    return b.bundle()
        // turns the output bundle stream into a stream containing
        // the normal attributes gulp plugins expect.
        .pipe(source('./app.js'))
        .pipe(buffer())
        .pipe(gulp.dest('./static/dist/'));
});
