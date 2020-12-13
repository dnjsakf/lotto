/* React */
import React, { useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';

/* Styled */
import styled from 'styled-components';

/* Recharts */
import { LineChart, Line, Tooltip, CartesianGrid, XAxis } from 'recharts';
import { Chart } from 'react-google-charts';

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
      <LineChart
        width={ 800 }
        height={ 400 }
        data={ datas }
        margin={{ top: 5, right: 40, left: 40, bottom: 5 }}
      >
        <XAxis dataKey="NO" />
        <Tooltip />
        <CartesianGrid stroke="#f5f5f5" />
        <Line type="monotone" dataKey="NUM1" stroke="#ff7300" yAxisId={0} />
        <Line type="monotone" dataKey="NUM2" stroke="#387908" yAxisId={1} />
        <Line type="monotone" dataKey="NUM3" stroke="#387908" yAxisId={2} />
        <Line type="monotone" dataKey="NUM4" stroke="#387908" yAxisId={3} />
        <Line type="monotone" dataKey="NUM5" stroke="#387908" yAxisId={4} />
        <Line type="monotone" dataKey="BONUS" stroke="#387908" yAxisId={5} />
      </LineChart>
      <Chart
        width={'500px'}
        height={'300px'}
        chartType="BubbleChart"
        loader={<div>Loading Chart</div>}
        data={[
          ['ID', 'Life Expectancy', 'Fertility Rate', 'Region', 'Population'],
          ['CAN', 80.66, 1.67, 'North America', 33739900],
          ['DEU', 79.84, 1.36, 'Europe', 81902307],
          ['DNK', 78.6, 1.84, 'Europe', 5523095],
          ['EGY', 72.73, 2.78, 'Middle East', 79716203],
          ['GBR', 80.05, 2, 'Europe', 61801570],
          ['IRN', 72.49, 1.7, 'Middle East', 73137148],
          ['IRQ', 68.09, 4.77, 'Middle East', 31090763],
          ['ISR', 81.55, 2.96, 'Middle East', 7485600],
          ['RUS', 68.6, 1.54, 'Europe', 141850000],
          ['USA', 78.09, 2.05, 'North America', 307007000],
        ]}
        options={{
          title:
            'Correlation between life expectancy, fertility rate ' +
            'and population of some world countries (2010)',
          hAxis: { title: 'Life Expectancy' },
          vAxis: { title: 'Fertility Rate' },
          bubble: { textStyle: { fontSize: 11 } },
        }}
        rootProps={{ 'data-testid': '1' }}
      />
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