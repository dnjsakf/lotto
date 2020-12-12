/* React */
import React, { useCallback } from 'react';
import PropTypes from 'prop-types';

/* Styled */
import styled from 'styled-components';

/* Styled Component */
const Container = styled.div`
  /* @TODO Write Style */
`;

const PageButton = styled.button`
`;

/* Main Component */
const Pagination = ( props )=>{
  /* Props */
  const {
    page,
    total,
    countForPage,
    hasNextPage,
    hasPrevPage,
    onClickPage,
    ...rest
  } = props;

  const startPage = parseInt(((page-1)/ countForPage))+1;
  const endPage = (startPage + countForPage) > total ? total : (startPage + countForPage);

  /* Render */
  return (
    <Container>
      <button disabled={ !hasPrevPage }>{ "<" }</button>
      {
        (()=>{
          const pages = [];
          for(let num=startPage; num<=endPage; num++ ){
            pages.push(
              <PageButton
                key={ num }
                onClick={ ( event )=>{ onClickPage(event, num) } }
              >
                { num }
              </PageButton>
            );
          }
          return pages;
        })()
      }
      <button disabled={ !hasNextPage }>{ ">" }</button>
    </Container>
  );
}

/* Props Type */
Pagination.propTypes = {
  // @TODO: Write prop types.
  page: PropTypes.number,
  total: PropTypes.number,
  countForPage: PropTypes.number,
  hasNextPage: PropTypes.bool,
  hasPrevPage: PropTypes.bool,
}

/* Props Default */
Pagination.defaultProps = {
  page: 1,
  total: 0,
  countForPage: 1,
  hasNextPage: false,
  hasPrevPage: false,
}

/* Exports */
export default Pagination;