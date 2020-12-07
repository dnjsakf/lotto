/* Webpack */
import { hot } from 'react-hot-loader/root';

/* React */
import React from 'react';

/* React Dom */
import { render as RouterDomRender } from "react-dom";

/* Redux */
import { Provider as StoreProvider } from 'react-redux';

/* Redux: store */
import store from '@reducers/store';

/* Material-UI */
import { ThemeProvider } from "@material-ui/styles";
import theme from "./theme";

/* Main Component */
import App from './App';

/* Functions: Renderer */
function render(Component){
  const root = document.getElementById("root");
  
  Component = module.hot ? hot( Component ) : Component;
  
  RouterDomRender((
    <React.StrictMode>
      <StoreProvider store={ store }>
        <ThemeProvider theme={ theme }>
          <Component />
        </ThemeProvider>
      </StoreProvider>
    </React.StrictMode>
   ), document.getElementById("root"));
}

/* Render Application */
render(App);