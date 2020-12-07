/* React */
import React from 'react';
import PropTypes from 'prop-types';

/* Styled */
import styled from 'styled-components';

/* Styled Component */
const Container = styled.section`
  /* @TODO Write Style */
`;

/* Main Component */
const Section = ( props )=>{
  /* Porps */
  const {
    children,
    ...rest
  } = props;

  /* Render */
  return (
    <Container>
      { children }
    </Container>
  );
}

/* Props Type */
Section.propTypes = {
  // @TODO: Write prop types.
}

/* Props Default */
Section.defaultProps = {
  // @TODO: Write default props.
}

/* Exports */
export default Section;