/* React */
import React from 'react';

/* Router */
import { BrowserRouter, Switch, Redirect } from 'react-router-dom';
import { PublicRoute } from './components/Routes';

/* Layout */
import MainLayout from './layouts/MainLayout'

/* View Components */
import { MainView } from './views';

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
            component={ MainView }
          />
          <Redirect from="*" to="/" />
        </Switch>
      </MainLayout>
    </BrowserRouter>
  );
}

/* Prop Types */
App.propTypes = { }

/* Default Props */
App.defaultProps = { }

/* Exports */
export default App;
