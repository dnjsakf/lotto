const path = require('path');
const config = require("./webpack.config.js");

const { merge } = require("webpack-merge");
const webpack = require("webpack");

const CopyWebpackPlugin = require("copy-webpack-plugin");
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

const ouptutPath = path.join(__dirname, "../src/dist")
const publicPath = path.join(__dirname, "../src/public")

module.exports = merge(config, {
  mode: "production",
  devtool: 'source-map',
  plugins: [
    new CleanWebpackPlugin({
      root: config.output.path,
      verbose: true,
    }),
    // new CopyWebpackPlugin({
    //   patterns: [
    //     {
    //       from: path.posix.join(
    //         path.join(__dirname, "../src/public").replace(/\\/g, "/"),
    //         "**/*"
    //       ),
    //       globOptions: {
    //         ignore: [
    //           "**/*.dat",
    //           "**/subdir/**",
    //         ],
    //       },
    //     },
    //   ],
    // }),
  ],
  optimization: {
    minimize: true,
  },
});