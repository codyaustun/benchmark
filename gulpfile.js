var gulp = require('gulp');

// Include plugins
var plugins = require("gulp-load-plugins")({
    pattern: ['gulp-*', 'gulp.*', 'main-bower-files', 'wiredep', 'del'],
    replaceString: /\bgulp[\-.]/
});

var config = {
    bowerDir: './bower_components',
    dest: './public/'
}

gulp.task('clean', function(cb){
    plugins.del([config.dest], cb);
});

gulp.task('css', function(){
    var injectAppFiles = gulp.src('src/sass/*.scss', {read: false});
    var injectGlobalFiles = gulp.src('src/global/*.scss', {read: false});

    function transformFilepath(filepath) {
        return '@import "' + filepath + '";';
    };

    var injectAppOptions = {
        transform: transformFilepath,
        starttag: '// inject:app',
        endtag: '// endinject',
        addRootSlash: false
    };

    var injectGlobalOptions = {
        transform: transformFilepath,
        starttag: '// inject:global',
        endtag: '// endinject',
        addRootSlash: false
    };

    return gulp.src('src/main.scss')
        .pipe(plugins.wiredep.stream())
        .pipe(plugins.inject(injectGlobalFiles, injectGlobalOptions))
        .pipe(plugins.inject(injectAppFiles, injectAppOptions))
        .pipe(plugins.sass())
        // .pipe(plugins.csso())
        .pipe(gulp.dest(config.dest + 'css'));
});

gulp.task('js', function() {
    var jsFiles = ['src/js/*'];

    return gulp.src(plugins.mainBowerFiles().concat(jsFiles))
        .pipe(plugins.filter('**/*.js'))
        .pipe(plugins.concat('main.js'))
        .pipe(gulp.dest(config.dest + 'js'))
        .pipe(plugins.rename('main.min.js'))
        // .pipe(plugins.uglify())
        .pipe(gulp.dest(config.dest + 'js'));
});

gulp.task('images', function() {
    var imgFiles = ['src/img/*'];

    return gulp.src(imgFiles)
        .pipe(plugins.imagemin({
            progressive: true 
        }))
        .pipe(gulp.dest(config.dest + 'img'))
});

gulp.task('vendors', function(){
    return gulp.src(plugins.mainBowerFiles())
        .pipe(plugins.filter('**/*.css'))
        .pipe(plugins.concat('vendors.css'))
        // .pipe(plugins.csso())
        .pipe(gulp.dest(config.dest + 'css'));
});

gulp.task('html', ['js', 'css', 'vendors'], function(){
    var injectFiles = gulp.src([
        config.dest + 'css/main.css',
        config.dest + 'css/vendors.css',
        config.dest + 'js/main.min.js'
    ]);

    var injectOptions = {
        addRootSlash: false,
    };

    return gulp.src('src/html/index.html')
        .pipe(plugins.inject(injectFiles, injectOptions))
        .pipe(gulp.dest('.'));
});

gulp.task('render', function() {
    return plugins.run('./update.sh').exec();
});

gulp.task('watch', function(){
    // Watch .js files
    gulp.watch('src/**/*.js', ['js']);

    // Watch .scss files
    gulp.watch('src/**/*.scss', ['css']);

    // Watch .html files
    gulp.watch('src/html/*.html', ['html']);

    // Watch image files
    gulp.watch('src/img/*', ['images']);

    // Watch leaderboard dependencies
    gulp.watch('results/**/*.json', ['render'])
    gulp.watch('templates/**/*.html', ['render'])
    gulp.watch('render.py', ['render'])
    gulp.watch('update.sh', ['render'])
});

gulp.task('default', ['html', 'images', 'render', 'watch']);
