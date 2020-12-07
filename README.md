
1.Babel
npm install --save-dev @babel/core @babel/preset-env @babel/preset-react babel-plugin-module-resolver

2.Babel Loaders
npm install --save-dev babel-loader css-loader react-hot-loader @hot-loader/react-dom

3.Webpack
npm install -g webpack webpack-cli
npm install --save-dev webpack webpack-cli webpack-dev-server webpack-merge

4.Webpack Plugins
npm install --save-dev html-webpack-plugin mini-css-extract-plugin clean-webpack-plugin copy-webpack-plugin

[ Install Dependencies Packages ]

1. React
npm install --save react react-dom react-router-dom

2. Redux ( with. React Redux )
npm install --save redux react-redux redux-actions redux-thunk redux-logger

3. Template
npm install --save @material-ui/core @material-ui/icons

4. Polyfill
npm install --save @babel/polyfill

999. 3rd party
npm install --save clsx 
npm install --save axios 
npm install --save notistack 
npm install --save prop-types 
npm install --save styled-components 

999. Full Scripts

npm install --save ^
	react react-dom react-router-dom ^
	redux react-redux redux-actions redux-thunk redux-logger ^
	@material-ui/core @material-ui/icons ^
	styled-components ^
	@babel/polyfill
    
npm install --save-dev ^
	@babel/core ^
	@babel/preset-env  ^
	@babel/preset-react  ^
	babel-plugin-module-resolver ^
	babel-loader css-loader react-hot-loader @hot-loader/react-dom ^
	webpack@4 webpack-cli@3 webpack-dev-server@3 webpack-merge ^
	html-webpack-plugin mini-css-extract-plugin clean-webpack-plugin copy-webpack-plugin

	
