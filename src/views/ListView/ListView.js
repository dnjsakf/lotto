/* React */
import React, { useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';

/* Styled */
import styled from 'styled-components';

/* Custom Components */
import List from '@components/List';

/* Axios */
import axios from 'axios';

/* Styled Component */
const Container = styled.section`
  /* @TODO Write Style */
`;

/* Constants */
const initColumns = [
  /* @TODO: Write Column Description */
  { label: "회차", name: "NO", width: "10%" },
  { label: "번호1", name: "NUM1", width: "10%" },
  { label: "번호2", name: "NUM2", width: "10%" },
  { label: "번호3", name: "NUM3", width: "10%" },
  { label: "번호4", name: "NUM4", width: "10%" },
  { label: "번호5", name: "NUM5", width: "10%" },
  { label: "보너스", name: "BONUS", width: "10%" },
  { label: "추첨일", name: "WIN_DATE", width: "30%" },
];

/* Main Component */
const ListView = ( props )=>{
  /* Props */
  const {
    ...rest
  } = props;
  
  /* State */
  const [ datas, setDatas ] = useState( [] );
  const [ page, setPage ] = useState( 1 );
  const [ pagination, setPagination ] = useState({
    page: 1,
    total: 0,
    countForPage: 10,
    hasNextPage: false,
    hasPrevPage: false
  });

  /* Handlers: Change Page. */
  const handleClickPage = useCallback(( event, movePage )=>{
    setPage(( movePage > 0 ? movePage : 1 ));
  }, []);

  /* Side Effects: Component did mounted. */
  useEffect(()=>{
    axios({
      url: "http://localhost:3000/api/lotto/list/"+page
    }).then((result)=>{
      setDatas(result.data.datas);
      setPagination({
        ...pagination,
        ...result.data.pagination
      });
    });
  }, [ page ]);

  /* Redner */
  return (
    <Container>
      <List
        items={ datas }
        cols={ initColumns }
        pagination={{
          ...pagination,
          onClickPage: handleClickPage,
        }}
      />
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