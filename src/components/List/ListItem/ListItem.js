/* React */
import React from 'react';
import PropTypes from 'prop-types';

/* Styled */
import styled from 'styled-components';

/* Styled Component */
const Container = styled.li`
  /* @TODO Write Style */
`;
const ListItemColumn = styled.div`
  display: inline-block;
  width: ${({ theme })=> theme.width };
`;

/* Main Component */
const ListItem = ( props )=>{
  /* Props */
  const {
    index,
    item,
    cols,
    ...rest
  } = props;

  /* Render */
  return (
    <Container>
    {
      cols && cols.map(( col )=>(
        <ListItemColumn
          key={ col.name+item[name] }
          theme={{
            width: col.width 
          }}
        >
          { item[col.name] }
        </ListItemColumn>
      ))
    }
    </Container>
  );
}

/* Props Type */
ListItem.propTypes = {
  // @TODO: Write prop types.
}

/* Props Default */
ListItem.defaultProps = {
  // @TODO: Write default props.
}

/* Exports */
export default ListItem;