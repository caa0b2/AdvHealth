import pandas as pd
import sqlite3

conn = sqlite3.connect('advhealth.sqlite')
cur = conn.cursor()

# basic summary stats of carrier table
cur.execute('''
SELECT
    count(distinct clm_id) as NBR_CLMS,
    count(distinct desynpuf_id) as BENES,
    count(distinct prf_physn_npi_1) as SVCG_PROVS,
    count(distinct tax_num_1) as BILL_PROVS,
    sum(LINE_NCH_PMT_AMT_1 + LINE_NCH_PMT_AMT_2 + LINE_NCH_PMT_AMT_3 + LINE_NCH_PMT_AMT_4 + LINE_NCH_PMT_AMT_5 + LINE_NCH_PMT_AMT_6 + LINE_NCH_PMT_AMT_7 + LINE_NCH_PMT_AMT_8 + LINE_NCH_PMT_AMT_9 + LINE_NCH_PMT_AMT_10 + LINE_NCH_PMT_AMT_11 + LINE_NCH_PMT_AMT_12 + LINE_NCH_PMT_AMT_13) as TTL_PAID,
    min(clm_from_dt) as FST_FROM_DT,
    max(clm_from_dt) as LST_FROM_DT,
    min(clm_thru_dt) as FST_THRU_DT,
    max(clm_thru_dt) as LST_THRU_DT,
    avg(clm_thru_dt - clm_from_dt) as AVG_CLM_DAYS
FROM Carrier;
''')

results1 = pd.DataFrame(cur.fetchall(), columns=['NBR_CLMS', 'BENES', 'SVCG_PROVS', 'BILL_PROVS', 'TTL_PAID', 'FST_FROM_DT', 'LST_FROM_DT', 'FST_THRU_DT', 'LST_THRU_DT', 'AVG_CLM_DAYS'])
print(results1.to_string(index=False))

# NBR_CLMS   BENES   SVCG_PROVS  BILL_PROVS  TTL_PAID     FST_FROM_DT LST_FROM_DT FST_THRU_DT LST_THRU_DT  AVG_CLM_DAYS
# 2,373,609  49,304  499,190     197,160     207,543,100  2008-01-01  2010-12-31  2008-01-01  2010-12-31   0.000448


# Find top ten transportation providers whose claims overlap with inpatient stays. 
# HCPCS beginning with A0 and T200 denote transporation services.
cur.execute('''
select x.TAX_NUM_1 as TAX_ID, 
	count(distinct x.desynpuf_id) as BENES,
	count(distinct x.clm_id) as NBR_CLMS,
	sum(LINE_NCH_PMT_AMT_1 +
		LINE_NCH_PMT_AMT_1 +
		LINE_NCH_PMT_AMT_1 +
		LINE_NCH_PMT_AMT_1 +
		LINE_NCH_PMT_AMT_1 +
		LINE_NCH_PMT_AMT_1 +
		LINE_NCH_PMT_AMT_1 +
		LINE_NCH_PMT_AMT_1 +
		LINE_NCH_PMT_AMT_1 +
		LINE_NCH_PMT_AMT_1 +
		LINE_NCH_PMT_AMT_1 +
		LINE_NCH_PMT_AMT_1 +
		LINE_NCH_PMT_AMT_1) as TTL_PAID
from 		Carrier as x
inner join	Inpatient as y
	on	x.clm_from_dt > y.clm_from_dt
	and	x.clm_thru_dt < y.clm_thru_dt
	and x.desynpuf_id = y.desynpuf_id
where
	substr(x.HCPCS_CD_1,1,2) = 'A0' or 
	substr(x.HCPCS_CD_2,1,2) = 'A0' or 
	substr(x.HCPCS_CD_3,1,2) = 'A0' or 
	substr(x.HCPCS_CD_4,1,2) = 'A0' or 
	substr(x.HCPCS_CD_5,1,2) = 'A0' or 
	substr(x.HCPCS_CD_6,1,2) = 'A0' or 
	substr(x.HCPCS_CD_7,1,2) = 'A0' or 
	substr(x.HCPCS_CD_8,1,2) = 'A0' or 
	substr(x.HCPCS_CD_9,1,2) = 'A0' or 
	substr(x.HCPCS_CD_10,1,2) = 'A0' or 
	substr(x.HCPCS_CD_11,1,2) = 'A0' or 
	substr(x.HCPCS_CD_12,1,2) = 'A0' or 
	substr(x.HCPCS_CD_13,1,2) = 'A0' or 
	substr(x.HCPCS_CD_1,1,4) = 'T200' or 
	substr(x.HCPCS_CD_2,1,4) = 'T200' or 
	substr(x.HCPCS_CD_3,1,4) = 'T200' or 
	substr(x.HCPCS_CD_4,1,4) = 'T200' or 
	substr(x.HCPCS_CD_5,1,4) = 'T200' or 
	substr(x.HCPCS_CD_6,1,4) = 'T200' or 
	substr(x.HCPCS_CD_7,1,4) = 'T200' or 
	substr(x.HCPCS_CD_8,1,4) = 'T200' or 
	substr(x.HCPCS_CD_9,1,4) = 'T200' or 
	substr(x.HCPCS_CD_10,1,4) = 'T200' or 
	substr(x.HCPCS_CD_11,1,4) = 'T200' or 
	substr(x.HCPCS_CD_12,1,4) = 'T200' or 
	substr(x.HCPCS_CD_13,1,4) = 'T200'
GROUP BY tax_id
ORDER BY ttl_paid desc
LIMIT 10;
''')

results2 = pd.DataFrame(cur.fetchall(), columns=['TAX_ID', 'BENES', 'NBR_CLMS', 'TTL_PAID'])
print(results2.to_string(index=False))

# Results
# Tax ID	Benes	Clms Paid
# 532092265	13	13	25220
# 294540272	14	16	23400
# 181719461	6	6	15470
# 144404073	10	11	13260
# 673314266	3	3	9880
# 597388679	4	4	9880
# 322988663	5	5	9880
# 414168433	1	2	9230
# 584165494	2	2	8840
# 564048790	5	5	8840


# Find top billers of orthotics. 
cur.execute('''
SELECT
	TAX_NUM_1 as TAX_ID,
	count(distinct desynpuf_id) as BENES,
	sum(case 
		when substr(HCPCS_CD_1,1,1) = 'L' then 1
		when substr(HCPCS_CD_2,1,1) = 'L' then 1
		when substr(HCPCS_CD_3,1,1) = 'L' then 1
		when substr(HCPCS_CD_4,1,1) = 'L' then 1
		when substr(HCPCS_CD_5,1,1) = 'L' then 1
		when substr(HCPCS_CD_6,1,1) = 'L' then 1
		when substr(HCPCS_CD_7,1,1) = 'L' then 1
		when substr(HCPCS_CD_8,1,1) = 'L' then 1
		when substr(HCPCS_CD_9,1,1) = 'L' then 1
		when substr(HCPCS_CD_10,1,1) = 'L' then 1
		when substr(HCPCS_CD_11,1,1) = 'L' then 1
		when substr(HCPCS_CD_12,1,1) = 'L' then 1
		when substr(HCPCS_CD_13,1,1) = 'L' then 1 
		else 0 end) as TTL_L_HCPCS,
	sum(case 
		when substr(HCPCS_CD_1,1,1) = 'L' then LINE_NCH_PMT_AMT_1
		when substr(HCPCS_CD_2,1,1) = 'L' then LINE_NCH_PMT_AMT_2 
		when substr(HCPCS_CD_3,1,1) = 'L' then LINE_NCH_PMT_AMT_3
		when substr(HCPCS_CD_4,1,1) = 'L' then LINE_NCH_PMT_AMT_4 
		when substr(HCPCS_CD_5,1,1) = 'L' then LINE_NCH_PMT_AMT_5 
		when substr(HCPCS_CD_6,1,1) = 'L' then LINE_NCH_PMT_AMT_6 
		when substr(HCPCS_CD_7,1,1) = 'L' then LINE_NCH_PMT_AMT_7 
		when substr(HCPCS_CD_8,1,1) = 'L' then LINE_NCH_PMT_AMT_8 
		when substr(HCPCS_CD_9,1,1) = 'L' then LINE_NCH_PMT_AMT_9
		when substr(HCPCS_CD_10,1,1) = 'L' then LINE_NCH_PMT_AMT_10 
		when substr(HCPCS_CD_11,1,1) = 'L' then LINE_NCH_PMT_AMT_11 
		when substr(HCPCS_CD_12,1,1) = 'L' then LINE_NCH_PMT_AMT_12 
		when substr(HCPCS_CD_13,1,1) = 'L' then LINE_NCH_PMT_AMT_13 
		else 0 end) as TTL_PAID
FROM 		Carrier
WHERE	(substr(HCPCS_CD_1,1,1) = 'L' or
		substr(HCPCS_CD_2,1,1) = 'L' or
		substr(HCPCS_CD_3,1,1) = 'L' or
		substr(HCPCS_CD_4,1,1) = 'L' or
		substr(HCPCS_CD_5,1,1) = 'L' or
		substr(HCPCS_CD_6,1,1) = 'L' or
		substr(HCPCS_CD_7,1,1) = 'L' or
		substr(HCPCS_CD_8,1,1) = 'L' or
		substr(HCPCS_CD_9,1,1) = 'L' or
		substr(HCPCS_CD_10,1,1) = 'L' or
		substr(HCPCS_CD_11,1,1) = 'L' or
		substr(HCPCS_CD_12,1,1) = 'L' or
		substr(HCPCS_CD_13,1,1) = 'L')
GROUP BY 1
ORDER by TTL_PAID DESC
LIMIT 10
;
''')

results3 = pd.DataFrame(cur.fetchall(), columns=['TAX_ID', 'BENES', 'TTL_L_HCPCS', 'TTL_PAID'])
print(results3.to_string(index=False))

# Results
# TAX)ID  BENES  TTL_L_HCPCS  TTL_PAID
# 532092265     15           15      1420
# 956348082      1            1       550
# 923368888      1            1       550
# 701854184      1            1       550
# 655410011      1            1       550
# 596181933      1            1       550
# 566672505      1            1       550
# 478841959      1            1       550
# 392613116      1            1       550
# 363692716      3            3       550

conn.close()