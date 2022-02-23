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
ax.set(xlabel='Date', ylabel='diluted EPS (USD/share)',
       title='Quarterly diluted EPS for Apple');

show_graph = st.checkbox('Show Graph', value=True)

if show_graph:
    st.pyplot(fig)

## PART 1 - Agenda

st.write('''
# Welcome To Streamlit!
In this Streamlit app we will cover:

- Markdown
- Importing data
- Displaying dataframes
- Graphing
- Interactivity with buttons
- Mapping
- Making predictions with user input
''')


# PART 2 - Markdown Syntax

st.write(
'''
## Markdown Syntax - Testing.. testing...
You can use Markdown syntax to style your text. For example,

# Main Title
## Subtitle
### Header

**Bold Text**

*Italics*

Ordered List

1. Apples
2. Oranges
3. Bananas

[This is a link!](https://docs.streamlit.io/en/stable/getting_started.html)

'''
)


# PART 3 - Seattle House Prices Table

st.write(
'''
## Seattle House Prices
We can import data into our Streamlit app using pandas `read_csv` then display the resulting dataframe with `st.dataframe()`.

''')

data = pd.read_csv('SeattleHomePrices.csv')
data = data.rename(columns={'LATITUDE': 'lat', 'LONGITUDE': 'lon'})
st.dataframe(data)


# PART 4 - Graphing and Buttons

st.write(
'''
### Graphing and Buttons
Let's graph some of our data with matplotlib. We can also add buttons to add interactivity to our app.
'''
)

fig, ax = plt.subplots()

ax.hist(data['PRICE'])
ax.set_title('Distribution of House Prices in $100,000s')

show_graph = st.checkbox('Show Graph', value=True)

if show_graph:
    st.pyplot(fig)


# PART 5 - Mapping and Filtering Data

st.write(
'''
## Mapping and Filtering Data
We can also use Streamlit's built in mapping functionality.
Furthermore, we can use a slider to filter for houses within a particular price range.
'''
)

price_input = st.slider('House Price Filter', int(data['PRICE'].min()), int(data['PRICE'].max()), 500000 )

price_filter = data['PRICE'] < price_input
st.map(data.loc[price_filter, ['lat', 'lon']])


# PART 6 - Linear Regression Model

st.write(
'''
## Train a Linear Regression Model
Now let's create a model to predict a house's price from its square footage and number of bedrooms.
'''
) 

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

clean_data = data.dropna(subset=['PRICE', 'SQUARE FEET', 'BEDS'])

X = clean_data[['SQUARE FEET', 'BEDS']]
y = clean_data['PRICE']

X_train, X_test, y_train, y_test = train_test_split(X, y)

## Warning: Using the above code, the R^2 value will continue changing in the app. Remember this file is run upon every update! Set the random_state if you want consistent R^2 results.
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

lr = LinearRegression()
lr.fit(X_train, y_train)

st.write(f'Test R²: {lr.score(X_test, y_test):.3f}')


# PART 7 - Predictions from User Input

st.write(
'''
## Model Predictions
And finally, we can make predictions with our trained model from user input.
'''
)

sqft = st.number_input('Square Footage of House', value=2000)
beds = st.number_input('Number of Bedrooms', value=3)

input_data = pd.DataFrame({'sqft': [sqft], 'beds': [beds]})
pred = lr.predict(input_data)[0]

st.write(
f'Predicted Sales Price of House: ${int(pred):,}'
)
