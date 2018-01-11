'use strict';

const gulp = require('gulp');

const less = require('gulp-less');
const gIf = require('gulp-if');
const autoprefixer = require('gulp-autoprefixer');
const cleanCSS = require('gulp-clean-css');
const argv = require('yargs').argv;
const plumber = require('gulp-plumber');
const babel = require('gulp-babel');
const uglify = require('gulp-uglify');
const concat = require('gulp-concat');
const sourcemaps = require('gulp-sourcemaps');
const gutil = require('gulp-util');
const del = require('del');
const htmlmin = require('gulp-htmlmin');

const watch_argv = !!argv.watch;
const production = !!argv.production;

gulp.task('js', function () {
    gutil.log(gutil.colors.bgGreen(production));

    if (production) {
        del(['vd-theme/static/js/*']);
    }

    gulp.src('bower_components/anchor-js/anchor.js')
        .pipe(gIf(production, uglify()))
        .pipe(gulp.dest('vd-theme/static/js/'));

    gulp.src('bower_components/jquery/dist/jquery.slim.js')
        .pipe(gIf(production, uglify()))
        .pipe(gulp.dest('vd-theme/static/js/'));

    gulp.src('bower_components/lity/dist/lity.js')
        .pipe(gIf(production, uglify()))
        .pipe(gulp.dest('vd-theme/static/js/'));
});

gulp.task('minify', function () {
    return gulp.src('published/**/*.html')
        .pipe(htmlmin({collapseWhitespace: true}))
        .pipe(gulp.dest('published'));
});

gulp.task('less', () => {
        gutil.log(gutil.colors.bgGreen(production));

        if (production) {
            del(['vd-theme/static/css/*']);
        }

        gulp.src(['vd-theme/static-source/less/*.less', 'bower_components/lity/dist/lity.css'])
            .pipe(gIf(!production, sourcemaps.init()))
            .pipe(less())
            .pipe(concat('build.css'))
            .pipe(gIf(production, cleanCSS({compatibility: 'ie9'})))
            .pipe(autoprefixer({browsers: ['last 3 versions'], cascade: false}))
            .pipe(gIf(!production, sourcemaps.write('.')))
            .pipe(gulp.dest('vd-theme/static/css/'));

        if (watch_argv) {

        }

    }
);

gulp.task('build', function () {
    gulp.start(['less', 'js']);

    if (watch_argv) {
        gulp.watch('vd-theme/static-source/less/*.less', ['less']);
    }
});
