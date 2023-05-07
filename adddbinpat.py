import csv
import sqlite3

conn = sqlite3.connect('advhealth.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Inpatient;

CREATE TEMPORARY TABLE Inpatient_X (
    DESYNPUF_ID                     TEXT,  
    CLM_ID                          TEXT,
    SEGMENT                         INTEGER,
    CLM_FROM_DT                     DATE,
    CLM_THRU_DT                     DATE,
    PRVDR_NUM                       TEXT,
    CLM_PMT_AMT                     INTEGER,
    NCH_PRMRY_PYR_CLM_PD_AMT        INTEGER,
    AT_PHYSN_NPI                    TEXT,
    OP_PHYSN_NPI                    TEXT,
    OT_PHYSN_NPI                    TEXT,
    CLM_ADMSN_DT                    DATE,
    ADMTNG_ICD9_DGNS_CD             TEXT,
    CLM_PASS_THRU_PER_DIEM_AMT      INTEGER,
    NCH_BENE_IP_DDCTBL_AMT          INTEGER,
    NCH_BENE_PTA_COINSRNC_LBLTY_AM  INTEGER,
    NCH_BENE_BLOOD_DDCTBL_LBLTY_AM  INTEGER,
    CLM_UTLZTN_DAY_CNT              INTEGER,
    NCH_BENE_DSCHRG_DT              DATE,
    CLM_DRG_CD                      TEXT,
    ICD9_DGNS_CD_1                  TEXT,
    ICD9_DGNS_CD_2                  TEXT,
    ICD9_DGNS_CD_3                  TEXT,
    ICD9_DGNS_CD_4                  TEXT,
    ICD9_DGNS_CD_5                  TEXT,
    ICD9_DGNS_CD_6                  TEXT,
    ICD9_DGNS_CD_7                  TEXT,
    ICD9_DGNS_CD_8                  TEXT,
    ICD9_DGNS_CD_9                  TEXT,
    ICD9_DGNS_CD_10                 TEXT,
    ICD9_PRCDR_CD_1                 TEXT,
    ICD9_PRCDR_CD_2                 TEXT,
    ICD9_PRCDR_CD_3                 TEXT,
    ICD9_PRCDR_CD_4                 TEXT,
    ICD9_PRCDR_CD_5                 TEXT,
    ICD9_PRCDR_CD_6                 TEXT,
    HCPCS_CD_1                      TEXT,
    HCPCS_CD_2                      TEXT,
    HCPCS_CD_3                      TEXT,
    HCPCS_CD_4                      TEXT,
    HCPCS_CD_5                      TEXT,
    HCPCS_CD_6                      TEXT,
    HCPCS_CD_7                      TEXT,
    HCPCS_CD_8                      TEXT,
    HCPCS_CD_9                      TEXT,
    HCPCS_CD_10                     TEXT,
    HCPCS_CD_11                     TEXT,
    HCPCS_CD_12                     TEXT,
    HCPCS_CD_13                     TEXT,
    HCPCS_CD_14                     TEXT,
    HCPCS_CD_15                     TEXT,
    HCPCS_CD_16                     TEXT,
    HCPCS_CD_17                     TEXT,
    HCPCS_CD_18                     TEXT,
    HCPCS_CD_19                     TEXT,
    HCPCS_CD_20                     TEXT,
    HCPCS_CD_21                     TEXT,
    HCPCS_CD_22                     TEXT,
    HCPCS_CD_23                     TEXT,
    HCPCS_CD_24                     TEXT,
    HCPCS_CD_25                     TEXT,
    HCPCS_CD_26                     TEXT,
    HCPCS_CD_27                     TEXT,
    HCPCS_CD_28                     TEXT,
    HCPCS_CD_29                     TEXT,
    HCPCS_CD_30                     TEXT,
    HCPCS_CD_31                     TEXT,
    HCPCS_CD_32                     TEXT,
    HCPCS_CD_33                     TEXT,
    HCPCS_CD_34                     TEXT,
    HCPCS_CD_35                     TEXT,
    HCPCS_CD_36                     TEXT,
    HCPCS_CD_37                     TEXT,
    HCPCS_CD_38                     TEXT,
    HCPCS_CD_39                     TEXT,
    HCPCS_CD_40                     TEXT,
    HCPCS_CD_41                     TEXT,
    HCPCS_CD_42                     TEXT,
    HCPCS_CD_43                     TEXT,
    HCPCS_CD_44                     TEXT,
    HCPCS_CD_45                     TEXT
);

''')


# inpatient data
with open('cms_2008_to_2010_Inpatient_Claims_20.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader) # skip header row
    for row in csvreader:
        row = ['.' if x == '' else x for x in row]
        conn.execute('INSERT INTO Inpatient_X (DESYNPUF_ID, CLM_ID, SEGMENT, CLM_FROM_DT, CLM_THRU_DT, PRVDR_NUM, CLM_PMT_AMT, NCH_PRMRY_PYR_CLM_PD_AMT, AT_PHYSN_NPI, OP_PHYSN_NPI, OT_PHYSN_NPI, CLM_ADMSN_DT, ADMTNG_ICD9_DGNS_CD, CLM_PASS_THRU_PER_DIEM_AMT, NCH_BENE_IP_DDCTBL_AMT, NCH_BENE_PTA_COINSRNC_LBLTY_AM, NCH_BENE_BLOOD_DDCTBL_LBLTY_AM, CLM_UTLZTN_DAY_CNT, NCH_BENE_DSCHRG_DT, CLM_DRG_CD, ICD9_DGNS_CD_1, ICD9_DGNS_CD_2, ICD9_DGNS_CD_3, ICD9_DGNS_CD_4, ICD9_DGNS_CD_5, ICD9_DGNS_CD_6, ICD9_DGNS_CD_7, ICD9_DGNS_CD_8, ICD9_DGNS_CD_9, ICD9_DGNS_CD_10, ICD9_PRCDR_CD_1, ICD9_PRCDR_CD_2, ICD9_PRCDR_CD_3, ICD9_PRCDR_CD_4, ICD9_PRCDR_CD_5, ICD9_PRCDR_CD_6, HCPCS_CD_1, HCPCS_CD_2, HCPCS_CD_3, HCPCS_CD_4, HCPCS_CD_5, HCPCS_CD_6, HCPCS_CD_7, HCPCS_CD_8, HCPCS_CD_9, HCPCS_CD_10, HCPCS_CD_11, HCPCS_CD_12, HCPCS_CD_13, HCPCS_CD_14, HCPCS_CD_15, HCPCS_CD_16, HCPCS_CD_17, HCPCS_CD_18, HCPCS_CD_19, HCPCS_CD_20, HCPCS_CD_21, HCPCS_CD_22, HCPCS_CD_23, HCPCS_CD_24, HCPCS_CD_25, HCPCS_CD_26, HCPCS_CD_27, HCPCS_CD_28, HCPCS_CD_29, HCPCS_CD_30, HCPCS_CD_31, HCPCS_CD_32, HCPCS_CD_33, HCPCS_CD_34, HCPCS_CD_35, HCPCS_CD_36, HCPCS_CD_37, HCPCS_CD_38, HCPCS_CD_39, HCPCS_CD_40, HCPCS_CD_41, HCPCS_CD_42, HCPCS_CD_43, HCPCS_CD_44, HCPCS_CD_45) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (row[0], row[1], row[2], row[3][0:4] + '-' +row[3][4:6]+ '-' + row[3][6:], row[4][0:4] + '-' +row[4][4:6]+ '-' + row[4][6:], row[5], row[6], row[7], row[8], row[9], row[10], row[11][0:4] + '-' +row[11][4:6]+ '-' + row[11][6:], row[12], row[13], row[14], row[15], row[16], row[17], row[18][0:4] + '-' +row[18][4:6]+ '-' + row[18][6:], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[36], row[37], row[38], row[39], row[40], row[41], row[42], row[43], row[44], row[45], row[46], row[47], row[48], row[49], row[50], row[51], row[52], row[53], row[54], row[55], row[56], row[57], row[58], row[59], row[60], row[61], row[62], row[63], row[64], row[65], row[66], row[67], row[68], row[69], row[70], row[71], row[72], row[73], row[74], row[75], row[76], row[77], row[78], row[79], row[80]))
conn.commit()

# Inpatient data table created with 66,514 rows
# REMOVE DUPLICATES

cur.executescript('''

CREATE TABLE Inpatient (
    DESYNPUF_ID                     TEXT,  
    CLM_ID                          TEXT,
    SEGMENT                         INTEGER,
    CLM_FROM_DT                     DATE,
    CLM_THRU_DT                     DATE,
    PRVDR_NUM                       TEXT,
    CLM_PMT_AMT                     INTEGER,
    NCH_PRMRY_PYR_CLM_PD_AMT        INTEGER,
    AT_PHYSN_NPI                    TEXT,
    OP_PHYSN_NPI                    TEXT,
    OT_PHYSN_NPI                    TEXT,
    CLM_ADMSN_DT                    DATE,
    ADMTNG_ICD9_DGNS_CD             TEXT,
    CLM_PASS_THRU_PER_DIEM_AMT      INTEGER,
    NCH_BENE_IP_DDCTBL_AMT          INTEGER,
    NCH_BENE_PTA_COINSRNC_LBLTY_AM  INTEGER,
    NCH_BENE_BLOOD_DDCTBL_LBLTY_AM  INTEGER,
    CLM_UTLZTN_DAY_CNT              INTEGER,
    NCH_BENE_DSCHRG_DT              DATE,
    CLM_DRG_CD                      TEXT,
    ICD9_DGNS_CD_1                  TEXT,
    ICD9_DGNS_CD_2                  TEXT,
    ICD9_DGNS_CD_3                  TEXT,
    ICD9_DGNS_CD_4                  TEXT,
    ICD9_DGNS_CD_5                  TEXT,
    ICD9_DGNS_CD_6                  TEXT,
    ICD9_DGNS_CD_7                  TEXT,
    ICD9_DGNS_CD_8                  TEXT,
    ICD9_DGNS_CD_9                  TEXT,
    ICD9_DGNS_CD_10                 TEXT,
    ICD9_PRCDR_CD_1                 TEXT,
    ICD9_PRCDR_CD_2                 TEXT,
    ICD9_PRCDR_CD_3                 TEXT,
    ICD9_PRCDR_CD_4                 TEXT,
    ICD9_PRCDR_CD_5                 TEXT,
    ICD9_PRCDR_CD_6                 TEXT,
    HCPCS_CD_1                      TEXT,
    HCPCS_CD_2                      TEXT,
    HCPCS_CD_3                      TEXT,
    HCPCS_CD_4                      TEXT,
    HCPCS_CD_5                      TEXT,
    HCPCS_CD_6                      TEXT,
    HCPCS_CD_7                      TEXT,
    HCPCS_CD_8                      TEXT,
    HCPCS_CD_9                      TEXT,
    HCPCS_CD_10                     TEXT,
    HCPCS_CD_11                     TEXT,
    HCPCS_CD_12                     TEXT,
    HCPCS_CD_13                     TEXT,
    HCPCS_CD_14                     TEXT,
    HCPCS_CD_15                     TEXT,
    HCPCS_CD_16                     TEXT,
    HCPCS_CD_17                     TEXT,
    HCPCS_CD_18                     TEXT,
    HCPCS_CD_19                     TEXT,
    HCPCS_CD_20                     TEXT,
    HCPCS_CD_21                     TEXT,
    HCPCS_CD_22                     TEXT,
    HCPCS_CD_23                     TEXT,
    HCPCS_CD_24                     TEXT,
    HCPCS_CD_25                     TEXT,
    HCPCS_CD_26                     TEXT,
    HCPCS_CD_27                     TEXT,
    HCPCS_CD_28                     TEXT,
    HCPCS_CD_29                     TEXT,
    HCPCS_CD_30                     TEXT,
    HCPCS_CD_31                     TEXT,
    HCPCS_CD_32                     TEXT,
    HCPCS_CD_33                     TEXT,
    HCPCS_CD_34                     TEXT,
    HCPCS_CD_35                     TEXT,
    HCPCS_CD_36                     TEXT,
    HCPCS_CD_37                     TEXT,
    HCPCS_CD_38                     TEXT,
    HCPCS_CD_39                     TEXT,
    HCPCS_CD_40                     TEXT,
    HCPCS_CD_41                     TEXT,
    HCPCS_CD_42                     TEXT,
    HCPCS_CD_43                     TEXT,
    HCPCS_CD_44                     TEXT,
    HCPCS_CD_45                     TEXT
);

CREATE TEMPORARY TABLE no_dups AS 
SELECT CLM_ID, SEGMENT, CLM_THRU_DT,
    RANK() OVER (PARTITION BY CLM_ID, SEGMENT ORDER BY CLM_THRU_DT DESC) as CLM_RANK
FROM Inpatient_X
;

INSERT INTO Inpatient
SELECT x.* 
FROM        Inpatient_X as x
INNER JOIN  no_dups as y
    on  x.CLM_ID    = y.CLM_ID
    and x.SEGMENT   = y.SEGMENT
    and x.CLM_THRU_DT = y.CLM_THRU_DT
    and y.CLM_RANK = 1;

''')
conn.commit()

# RESULT: 66,514 lines. Probably no duplicates!

conn.close()