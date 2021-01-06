class SQLiteConfig:
  url = 'sqlite://../app/database/example.db' # 'sqlite:///:memory:'

class OracleConfig:
  url = "localhost"
  port = 1521
  database = "CAMPDB"
  username = "SYSTEM"
  password = "campmaxquad12"

  init_res = [
    '''
      CREATE TABLE LOTTO.IF_LOTTO_PRZWIN_MST (
        DRWT_NO	            NUMBER,
        DRWT_NO_DATE		    VARCHAR2(8),
        DRWT_NO1            NUMBER,
        DRWT_NO2            NUMBER,
        DRWT_NO3            NUMBER,
        DRWT_NO4            NUMBER,
        DRWT_NO5            NUMBER,
        DRWT_NO6            NUMBER,
        DRWT_NO_BNUS        NUMBER,
        FRST_ACCUM_AMOUNT	  NUMBER,
        FRST_PRZWIN_AMOUNT  NUMBER,
        FRST_PRZWIN_CO      NUMBER,
        RTN_VAL             VARCHAR2(500),
        REG_USER            VARCHAR2(50),
        REG_DTTM            VARCHAR2(14),
        UPD_USER            VARCHAR2(50),
        UPD_DTTM            VARCHAR2(14)
      )
      TABLESPACE TS_QUADMAX_DAT
      ;

      ALTER TABLE LOTTO.IF_LOTTO_PRZWIN_MST
          ADD CONSTRAINT PK_IF_LOTTO_PRZWIN_MST
          PRIMARY KEY ( DRWT_NO )
      ;

      COMMENT ON TABLE LOTTO.IF_LOTTO_PRZWIN_MST IS 'IF_로또_추첨결과_마스터';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.DRWT_NO IS '추첨회차';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.DRWT_NO_DATE IS '추첨일';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.DRWT_NO1 IS '추첨번호1';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.DRWT_NO2 IS '추첨번호2';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.DRWT_NO3 IS '추첨번호3';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.DRWT_NO4 IS '추첨번호4';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.DRWT_NO5 IS '추첨번호5';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.DRWT_NO6 IS '추첨번호6';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.DRWT_NO_BNUS IS '보너스번호';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.FRST_ACCUM_AMOUNT IS '1등_총_당첨금액';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.FRST_PRZWIN_AMOUNT IS '1등_당첨금액';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.FRST_PRZWIN_CO IS '1등_당첨수';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.RTN_VAL IS '반환값';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.REG_USER IS '생성자';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.REG_DTTM IS '생성일시';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.UPD_USER IS '수정자';
      COMMENT ON COLUMN LOTTO.IF_LOTTO_PRZWIN_MST.UPD_DTTM IS '수정일시';

      GRANT SELECT ON LOTTO.IF_LOTTO_PRZWIN_MST TO PUBLIC;
    '''
  ]