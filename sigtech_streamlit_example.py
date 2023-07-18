import pandas as pd
import streamlit as st
import sigtech.api as sig
import datetime
import altair as alt
import os


# initialize environment and session

st.set_page_config(layout='wide')
st.title("SigTech API Example")
st.markdown('''### Here's an example on how to leverage SigTech's API for finding asset performance, [more info here.](https://github.com/SIGTechnologies/sigtech-python)''')

c1,c2,c3 = st.columns(3)

assets = {
"S&P 500 Index Futures":"ES INDEX",
"Gold Futures":"GC COMDTY",
"Brent Crude Oil Futures":"CL COMDTY",
"U.S. Dollar Index Futures":"DX CURNCY",
"British Pound Futures":"BP CURNCY",
"US 10 Year Treasury Futures":"TY COMDTY",
"Natural Gas Futures":"NG COMDTY",
"30 Day Federal Fund Futures":"FF COMDTY"
}

asset_list = list(assets.values())

with st.sidebar:
    st.header("Please enter your API key in order to proceed: ")
    sig_key = st.text_input("SigTech API Key")

if sig_key:
    st.text('Select two assets you would like to compare their performance since a certain date.')

    os.environ['SIGTECH_API_KEY'] = sig_key
    sig.init()

    with c1:
        
        asset1 = st.selectbox("Please select first instrument below",options=asset_list)

    with c2:
        asset2 = st.selectbox("Please select second instrument below",options=asset_list,index=1)

    with c3:
        d = st.date_input(
            "Please choose a start date",
            (datetime.date(2022, 1, 1))
        )
    asset1_strategy = sig.RollingFutureStrategy(
            contract_code=f'{asset1.split()[0]}',
            contract_sector=f'{asset1.split()[1]}',
            rolling_rule='front',
            front_offset= '-4:-1',
            currency='USD',
            start_date=d
        )
    asset2_strategy = sig.RollingFutureStrategy(
            contract_code=f'{asset2.split()[0]}',
            contract_sector=f'{asset2.split()[1]}',
            rolling_rule='front',
            front_offset= '-4:-1',
            currency='USD',
            start_date=d
        )
    with st.spinner('Running backtest for your chosen instruments...'):
        data = pd.concat([asset1_strategy.history(),asset2_strategy.history()], axis=1, keys=[asset1, asset2])

    # Convert DataFrame to long format
    data = data.stack(level=0).reset_index()
    data.columns = ['date', 'instrument', 'price']

else:
    st.text('Make sure enter your API key to update the graph with your preferred instruments')

    with c1:
        
        asset1 = st.selectbox("Please select first instrument below",options=['ES INDEX'])

    with c2:
        asset2 = st.selectbox("Please select second instrument below",options=['BP CURNCY'])

    with c3:
        d = st.date_input(
            "Please choose a start date",
            (datetime.date(2022, 1, 1))
        )
    data = pd.read_csv('sample_data.csv')
chart = alt.Chart(data).mark_line().encode(
    x=alt.X('date:T', title='Date'),
    y=alt.Y('price:Q', title='Price', scale=alt.Scale(domain=(500, 1500))),
    color='instrument:N'
).properties(
    width=800,  # Width of the chart
    height=500  # Height of the chart
)
st.altair_chart(chart,use_container_width=True)
