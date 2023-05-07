import sqlite3

conn = sqlite3.connect('advhealth.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS ICD9_Ref;
DROP TABLE IF EXISTS Proc_Ref;
DROP TABLE IF EXISTS Code_Ref;

CREATE TABLE ICD9_Ref (
    CODE_TYPE                       TEXT,
    ICD_CPT_HCPCS                   TEXT,
    DESCRIPTION                     TEXT
);

CREATE TABLE Proc_Ref (
    CODE_TYPE                       TEXT,
    ICD_CPT_HCPCS                   TEXT,
    DESCRIPTION                     TEXT
);

''')


# make code reference table
with open('cms-icd9-longdesc.txt', 'r') as txtfile:
    for line in txtfile:
        code_type = 'DIAG'
        icd_cpt_hcpcs = line[:5].strip()
        description = line[6:].strip()
        conn.execute('INSERT INTO ICD9_Ref (CODE_TYPE, ICD_CPT_HCPCS, DESCRIPTION) VALUES (?, ?, ?)',
                     (code_type, icd_cpt_hcpcs, description))
conn.commit()

with open('cms-pfs-proccodes20120.txt', 'r') as txtfile:
    for line in txtfile:
        code_type = 'PROC'
        icd_cpt_hcpcs = line[:5].strip()
        description = line[7:57].strip()
        conn.execute('INSERT INTO Proc_Ref (CODE_TYPE, ICD_CPT_HCPCS, DESCRIPTION) VALUES (?, ?, ?)',
                     (code_type, icd_cpt_hcpcs, description))
conn.commit()


cur.executescript('''

CREATE TABLE Code_Ref AS SELECT * FROM ICD9_Ref UNION ALL SELECT * FROM Proc_Ref;

DROP TABLE IF EXISTS ICD9_Ref;
DROP TABLE IF EXISTS Proc_Ref;

''')

# do duplicate rows per check in DB Browser for SQLite.

conn.close()