/* React */
import React from 'react';

/* Router */
import { BrowserRouter, Switch, Redirect } from 'react-router-dom';
import { PublicRoute } from './components/Routes';

/* Styled */
import { createGlobalStyle } from 'styled-components'

/* Layout */
import MainLayout from './layouts/MainLayout'

/* View Components */
import { MainView, ListView } from './views';


/* Global Styled */
const GlobalStyle = createGlobalStyle`
  * {
    box-sizing: border-box;
  }

  .active {
    color: red;
  }
`

/* Main Component */
const App = ( props )=>{
  /* Render */
  return (
    <BrowserRouter>
      <MainLayout>
        <Switch>
          <PublicRoute
            exact
            path="/"
            component={ ListView }
          />
          <Redirect from="*" to="/" />
        </Switch>
      </MainLayout>
      <GlobalStyle />
    </BrowserRouter>
  );
}

/* Prop Types */
App.propTypes = { }

/* Default Props */
App.defaultProps = { }

/* Exports */
export default App;
