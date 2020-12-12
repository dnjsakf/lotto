/* React */
import React from 'react';
import PropTypes from 'prop-types';

/* Styled */
import styled from 'styled-components';

/* Custom Components */
import ListItem from './ListItem';
import Pagination from './Pagination';

/* Styled Component */
const Conatiner = styled.ul`
  padding: 0;
  margin: 0 auto;
  /* @TODO Write Style */
`;
const ListItemHeader = styled.li`
`;
const ListItemColumn = styled.div`
  display: inline-block;
  width: ${({ theme })=> theme.width };
`;

/* Main Component */
/* UnorderdList */
const List = ( props )=>{
  /* Props */
  const {
    items,
    cols,
    pagination,
    ...rest
  } = props;

  /* Render */
  return (
    <Conatiner>
      {
        cols && (
          <ListItemHeader>
          {
            cols && cols.map(( col, idx )=>(
              <ListItemColumn
                key={ idx }
                theme={{ width: col.width }}
              >
                { col.label }
              </ListItemColumn>
            ))
          }
          </ListItemHeader>
        )
      }
      {
        !items
          ? "데이터가 존재하지 않습니다."
          : items.map(( item, idx )=>(
            <ListItem
              key={ "list-item-"+idx }
              index={ idx }
              item={ item }
              cols={ cols }
              showHeader={ true }
            />
        ))
      }
      <Pagination { ...pagination } />
    </Conatiner>
  );
}

/* Props Type */
List.propTypes = {
  // @TODO: Write prop types.
  items: PropTypes.array,
  cols: PropTypes.array,
  pagination: PropTypes.shape({
    page: PropTypes.number,
    total: PropTypes.number,
    countForPage: PropTypes.number,
    hasNextPage: PropTypes.bool,
    hasPrevPage: PropTypes.bool,
  }),
}

/* Props Default */
List.defaultProps = {
  // @TODO: Write default props.
  items: [],
  cols: [],
  pagination: {
    page: 1,
    total: 0,
    countForPage: 1,
    hasNextPage: false,
    hasPrevPage: false,
  }
}

/* Exports */
export default List;