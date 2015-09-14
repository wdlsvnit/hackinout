var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
	entry : './app/js/main.js',
	output : {
		filename : 'public/bundle.js'
	},

	module : {
		loaders: [
			// SASS
			{
				test: /\.sass$/,
			    loader: ExtractTextPlugin.extract('css!sass')
			},

			// ES6
			 { 
			 	test: /\.js$/,
			 	exclude: [/bower_components/, /node_modules/, /app\/js\/app_info\.js/],
                loader: 'babel-loader' 
             }
		]
	},
	plugins : [
		 new ExtractTextPlugin('public/style.css', {
            allChunks: true
        })
	]
};