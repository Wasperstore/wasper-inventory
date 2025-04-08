const path = require('path');
const { VueLoaderPlugin } = require('vue-loader');

module.exports = {
  entry: {
    'wasper_inventory': './wasper_inventory/public/js/wasper_inventory.js'
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'wasper_inventory/public/dist'),
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.vue'],
    alias: {
      'vue$': 'vue/dist/vue.esm-bundler.js'
    }
  },
  plugins: [
    new VueLoaderPlugin()
  ]
}; 