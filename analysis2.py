import sqlite3
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Goal. To forecast amount paid.

conn = sqlite3.connect('advhealth.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS PaidMonth;

CREATE TABLE PaidMonth (
   CLM_FROM_DT  DATETIME  NOT NULL PRIMARY KEY,
   NBR_CLMS     INTEGER,
   BENES        INTEGER,
   NBR_PROCS    INTEGER,
   AMOUNT_PAID  INTEGER
);


INSERT INTO PaidMonth
SELECT 
	clm_from_dt,
    count(distinct clm_id) as NBR_CLMS,
	count(distinct desynpuf_id) as BENES,
	sum(case 
		when HCPCS_CD_13 !='.' then 13 
		when HCPCS_CD_12 !='.' then 12 
		when HCPCS_CD_11 !='.' then 11 
		when HCPCS_CD_10 !='.' then 10
		when HCPCS_CD_9 !='.' then 9
		when HCPCS_CD_8 !='.' then 8 
		when HCPCS_CD_7 !='.' then 7
		when HCPCS_CD_6 !='.' then 6
		when HCPCS_CD_5 !='.' then 5
		when HCPCS_CD_4 !='.' then 4
		when HCPCS_CD_3 !='.' then 3
		when HCPCS_CD_2 !='.' then 2
		when HCPCS_CD_1 !='.' then 1 		
		else 0 end) as NBR_PROCS,
	sum(LINE_NCH_PMT_AMT_1 + 
		LINE_NCH_PMT_AMT_2 + 
		LINE_NCH_PMT_AMT_3 + 
		LINE_NCH_PMT_AMT_4 +
		LINE_NCH_PMT_AMT_5 +
		LINE_NCH_PMT_AMT_6 +
		LINE_NCH_PMT_AMT_7 +
		LINE_NCH_PMT_AMT_8 +
		LINE_NCH_PMT_AMT_9 +
		LINE_NCH_PMT_AMT_10 +
		LINE_NCH_PMT_AMT_11 +
		LINE_NCH_PMT_AMT_12 +
		LINE_NCH_PMT_AMT_13) as AMOUNT_PAID 
FROM Carrier as x
where clm_from_dt is not null and clm_from_dt !='.'
GROUP BY 1
;

''')

# PART 1. Time series regression.
df = pd.read_sql_query("SELECT * from PaidMonth", conn)

conn.close()

# df.to_csv('paidmonthdb.csv')

# convert CLM_FROM_DT to datetime
df['CLM_FROM_DT'] = pd.to_datetime(df['CLM_FROM_DT'])


# correlation matrix
corr_matrix = df.corr()
print(corr_matrix)

#              CLM_FROM_DT  NBR_CLMS     BENES  NBR_PROCS  AMOUNT_PAID
# CLM_FROM_DT     1.000000 -0.531830 -0.523230  -0.505610    -0.478635
# NBR_CLMS       -0.531830  1.000000  0.999814   0.997190     0.990468
# BENES          -0.523230  0.999814  1.000000   0.997285     0.990866
# NBR_PROCS      -0.505610  0.997190  0.997285   1.000000     0.992759
# AMOUNT_PAID    -0.478635  0.990468  0.990866   0.992759     1.000000


# define the index - time sequence.
df['day'] = df.index

# fit linear regression model
model = LinearRegression()
model.fit(df[['day']],df['AMOUNT_PAID'])

# show the slope and intercept
print('slope:',model.coef_)
print('intercept:',model.intercept_)
print('R^2:',model.score(df[['day']],df['AMOUNT_PAID']))

# slope: [-80.07567721]
# intercept: 233205.57560766255
# R^2: 0.22909129418706609

# y prediction
y_pred = pd.Series(model.predict(df[['day']]))
y_pred
# graph the predictions
plt.figure(figsize=(12,8))
plt.scatter(df['day'],df['AMOUNT_PAID'])
plt.plot(df['day'],y_pred,color='red')
plt.xlabel('Day')
plt.ylabel('Amount Paid')
plt.title('Amount Paid vs Day')
plt.show()
# show row 500
df.iloc[500]
df.describe()


# PART 2. Multiple regression.
# Split the data into training and testing sets using the "good" data.
train = df[180:456]
test = df[456:731]
subset = df[180:731]

# Create the linear regression model and fit it to the training data
model = LinearRegression()
model.fit(train[['BENES','NBR_PROCS']], train['AMOUNT_PAID'])

# Use the model to make predictions on the testing data
predictions = model.predict(test[['BENES', 'NBR_PROCS']])

print('coefficients', model.coef_)
print('intercept:', model.intercept_)

# coefficients [48.64975211 27.11206409]
# intercept: -28681.814790318545

# Plot the actual and predicted values
plt.scatter(subset['day'], subset['AMOUNT_PAID'], label='Actual', color='blue')
plt.plot(test['day'], predictions, label='Predicted', color='red')
plt.title('Predicted daily paid amounts based on beneficiaries and procedures')
plt.legend()
plt.show()