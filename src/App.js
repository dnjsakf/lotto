/* React */
import React from 'react';

import App2 from './App2';

/* Main Component */
const App = ( props )=>{    
  /* Render */
  return (
    <React.Fragment>
      <h5>Hello, React!!!</h5>
      <App2 />
    </React.Fragment>
  );
}

/* Prop Types */
App.propTypes = { }

/* Default Props */
App.defaultProps = { }

/* Exports */
export default App;
