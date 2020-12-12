/* React */
import React, { useCallback } from 'react';
import PropTypes from 'prop-types';

/* Styled */
import styled from 'styled-components';

/* 3rd Party */
import clsx from 'clsx';

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

  const startPage = (parseInt(((page-1)/(countForPage)))*countForPage)+1;
  const endPage = ((startPage-1) + countForPage) >= parseInt(total/countForPage) ? parseInt(total/countForPage) : ((startPage-1) + countForPage);

  /* Render */
  return (
    <Container>
    <button
      onClick={ ( event )=>{ console.log( endPage+1 ); onClickPage(event, 1); } }
      disabled={ page == 1 }
    >
      { "|<" }
    </button>
      <button 
        onClick={ ( event )=>{ onClickPage(event, startPage-1); } }
        disabled={ !hasPrevPage }
      >
        { "<" }
      </button>
      {
        (()=>{
          const pages = [];
          for(let num=startPage; num<=endPage; num++ ){
            pages.push(
              <PageButton
                key={ num }
                onClick={ ( event )=>{ onClickPage(event, num); } }
                className={
                  clsx({
                    "active": page == num
                  })
                }
              >
                { num }
              </PageButton>
            );
          }
          return pages;
        })()
      }
      <button
        onClick={ ( event )=>{ console.log( endPage+1 ); onClickPage(event, endPage+1); } }
        disabled={ !hasNextPage }
      >
        { ">" }
      </button>
      <button
        onClick={ ( event )=>{ console.log( endPage+1 ); onClickPage(event, parseInt(total/countForPage)); } }
        disabled={ endPage == parseInt(total/countForPage) }
      >
        { ">|" }
      </button>
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