/* React */
import React from 'react';
import PropTypes from 'prop-types';

/* Styled */
import styled from 'styled-components';

/* Layout Components */
import Header from './Header';
import Section from './Section';
import Footer from './Footer';

/* Styled Components */
const Container = styled.div`
  height: 100%;
  width: 100%;
`;

/* Main Component */
const MainLayout = ( props )=>{
  /* Props */
  const {
    children,
    ...rest
  } = props;

  /* Render */
  return (
    <Container>
      <Header />
      <Section>
        { children }
      </Section>
      <Footer />
    </Container>
  );
}

/* Props Type */
MainLayout.propTypes = { }

/* Props Default */
MainLayout.defaultProps = { }

/* Exports */
export default MainLayout;