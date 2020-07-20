import sqlite3
 
#connects to database, creates a sqlite file
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()
 
cur.execute('''
DROP TABLE IF EXISTS Counts''')
 
cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')
 
#convert txt into table
fname = raw_input ('Enter file name:') #<span style="font-family: Arial, Helvetica, sans-serif;">fname = 'mbox-short.txt'</span>
if (len(fname) < 1) : fname = 'mbox-short.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From: ') : continue
    pieces = line.split('@')
    org = pieces[1]
    org = org.rstrip()#remove the blank spaces
    cur.execute('SELECT count FROM Counts WHERE org = ?', (org, ))
    try:
        count = cur.fetchone()[0]#get the current count
        cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?', (org, ))
    except:
        cur.execute('''INSERT INTO Counts (org, count)
            VALUES(?, 1)''', (org, ))
    conn.commit()
 
 
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC' #DESC LIMIT 10
 
for row in cur.execute(sqlstr):
    print str(row[0]), row[1]
 
cur.close()