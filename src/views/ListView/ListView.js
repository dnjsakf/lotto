/* React */
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

/* Styled */
import styled from 'styled-components';

/* Axios */
import axios from 'axios';

/* Styled Component */
const Container = styled.section`
  /* @TODO Write Style */
`;

/* Main Component */
const ListView = ( props )=>{
  
  /* State */
  const [ datas, setDatas ] = useState([]);

  /* Side Effects: Component did mounted. */
  useEffect(()=>{
    axios({
      url: "http://localhost:3000/data"
    }).then((result)=>{
      setDatas(result.data.datas)
    })
  }, []);

  /* Redner */
  return (
    <Container>
      <ul>
      {
        datas && datas.map(( item, idx )=>{
        return (
          <li key={item[0]}>
            <span>회차:{ item[0] }</span> /
            <span>{ item[12] }</span> / 
            <span>{ item[13] }</span> / 
            <span>{ item[14] }</span> / 
            <span>{ item[15] }</span> / 
            <span>{ item[16] }</span> / 
            <span>{ item[17] }</span> / 
            <span>{ item[18] }</span>
            <hr/>
          </li>
        )
        })
      }
      </ul>
    </Container>
  );
}

/* Props Type */
ListView.propTypes = {
  // @TODO: Write prop types.
}

/* Props Default */
ListView.defaultProps = {
  // @TODO: Write default props.
}

/* Exports */
export default ListView;