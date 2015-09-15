var gulp = require('gulp'),
    gulpLoadPlugins = require('gulp-load-plugins'),
    plugins = gulpLoadPlugins(),
    autoprefixer = require('gulp-autoprefixer'),
    sourcemaps = require('gulp-sourcemaps')
    sass = require('gulp-ruby-sass');

var app = 'src';

var onError = function(err) {
    console.log(err);
};

gulp.task('Sass', function() {
	gulp.src('app/scss/**/*.scss')
        .pipe(plugins.plumber({
            errorHandler: onError
        }))
        .pipe(sourcemaps.init())
        .pipe(plugins.rubySass({
            style: 'expanded',
            check: true,
            "sourcemap=none": true
        }))
        .pipe(plugins.rename({suffix: '.min'}))
        .pipe(autoprefixer({
            browsers: ['last 3 versions'],
            cascade: false
        }))
        .pipe(plugins.minifyCss({keepSpecialComments:0}))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('inout/static/inout/'));
});

gulp.task('watch', function() {
    gulp.watch('app/scss/**/*.scss', ['Sass']);
});

gulp.task('default', ['Sass']);

