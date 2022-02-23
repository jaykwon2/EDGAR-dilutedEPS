import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import psycopg2 #postgres python adapter

st.write('''
# Quarterly diluted Earnings per Share
''')

connection = psycopg2.connect(dbname="edgar_db", host="edgar.c57fovsijcwz.us-east-1.rds.amazonaws.com", port="5432", user="postgres", password="#Metis4life")
cursor = connection.cursor()
cursor.execute("SELECT * FROM earningspersharediluted WHERE form = '10-Q' AND companyname = 'Apple Inc.'")
results = cursor.fetchall()

df = pd.DataFrame(results, columns=['id','companyname','startdate','enddate','val','accn','fy','fp','form','filed'])

# Apple's quarterly EPS Table

st.write(
'''
## Apple's quarterly diluted earnings per share (EPS)
'val' column is the diluted EPS (in USD/share)
''')

st.dataframe(df)


# plot time series graph of Apple's quarterly diluted EPS

st.write(
'''
### Time Series graph of Apple's quarterly diluted EPS
'''
)

ts2 = df[['filed','val']]

# plt.figure(figsize=(15,5))
# plt.plot(ts2['filed'], ts2['val'])
# plt.ylabel('diluted EPS (USD/share)')
# plt.xlabel('Date')
# plt.xticks(rotation=45)
# plt.title('Quarterly diluted EPS for Apple')

fig, ax = plt.subplots()
ax.plot(ts2['filed'], ts2['val'])
ax.set(xlabel='Date', ylabel='diluted EPS (USD/share)',
       title='Quarterly diluted EPS for Apple');

show_graph = st.checkbox('Show Graph', value=True)

if show_graph:
    st.pyplot(fig)