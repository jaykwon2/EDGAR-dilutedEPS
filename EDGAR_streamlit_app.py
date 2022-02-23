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

cursor.execute("SELECT DISTINCT(companyname) FROM earningspersharediluted WHERE form = '10-Q'")
results_company = cursor.fetchall()
company_list = list()
for comp in results_company:
    company_list.append(comp[0])
company_list

option = st.selectbox(
     'Select an SP500 Company from the list below:',
     company_list)
st.write('You selected:', option)

cursor.execute("SELECT * FROM earningspersharediluted WHERE form = '10-Q' AND companyname = '"+option+"'")

# cursor.execute("SELECT * FROM earningspersharediluted WHERE form = '10-Q' AND companyname = %s", option)
# cursor.execute("SELECT * FROM earningspersharediluted WHERE form = '10-Q' AND companyname = option")
results = cursor.fetchall()

df = pd.DataFrame(results, columns=['id','companyname','startdate','enddate','val','accn','fy','fp','form','filed'])
df['period'] = (df['enddate'] - df['startdate'])
quarterly_df = df.copy()
quarterly_df = quarterly_df[quarterly_df['period'].dt.days < 100]
quarterly_df['period'] = df['period'].dt.days.astype('int16')

# Quarterly EPS Table

st.write(""" ## {0} - quarterly diluted Earnings per Share (EPS)
'val' column is the diluted EPS (in USD/share)""".format(option))

# st.write(
# '''
# ## Quarterly diluted Earnings per Share (EPS)
# 'val' column is the diluted EPS (in USD/share)
# ''')

st.dataframe(quarterly_df)

# plot time series graph of quarterly diluted EPS

st.write(""" ## {0} - Time Series graph of quarterly diluted EPS""".format(option))

# st.write(
# '''
# ### Time Series graph of quarterly diluted EPS
# '''
# )

ts3 = quarterly_df[['enddate','val']] # actual enddate instead of when it was accounced/filed
fig, ax = plt.subplots()
ax.plot(ts3['enddate'], ts3['val'])
ax.set(xlabel='Date', ylabel='diluted EPS (USD/share)',
       title='Quarterly diluted EPS for Apple')

show_graph = st.checkbox('Show Graph', value=True)

if show_graph:
    st.pyplot(fig)
