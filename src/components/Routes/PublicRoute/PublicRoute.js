/* React */
import React from 'react';
import PropTypes from 'prop-types';

/* Router */
import { Route } from 'react-router-dom';

/* Main Component */
const PublicRoute = ( props )=>{
  /* Props */
  const {
    component: Component,
    ...rest
  } = props;
  
  /* Render */
  return (
    <Route
      { ...rest }
      render={
        ( matchProps )=>(
          <Component { ...matchProps }/>
        )
      }
    />
  );
}

/* Props Type */
PublicRoute.propTypes = {
  component: PropTypes.any,
}

/* Props Default */
PublicRoute.defaultProps = { }

/* Exports */
export default PublicRoute;