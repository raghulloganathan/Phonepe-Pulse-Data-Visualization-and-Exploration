# Importing Libraries
import pandas as pd
import mysql.connector as sql
import streamlit as st
import plotly.express as px
import os
import json
import requests
from streamlit_option_menu import option_menu
from PIL import Image
import plotly.graph_objects as go
from streamlit_extras.add_vertical_space import add_vertical_space

# Setting up page configuration
icon = Image.open(r"C:\\Users\\rghlr\\Desktop\\PYTHON\\Logo.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization | By Raghul",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by * Raghul *!"""})

st.sidebar.header(":violet[**PHONEPE ANALYSIS**]")


# Creating connection with mysql workbench
mydb = sql.connect(host="localhost",
                   user="root",
                   password="raghul6379128502",
                   database= "phonepe_pulse",
                   auth_plugin="mysql_native_password"
                   
                  )
mycursor = mydb.cursor(buffered=True)

# Aggregated_insurance

mycursor.execute("SELECT * FROM aggregated_insurance;")
table1 = mycursor.fetchall()
Aggre_insurance = pd.DataFrame(table1, columns=("States", "Years", "Quarter", "Transaction_Type", "Transaction_Count", "Transaction_Amount"))

# Aggregated_transaction
                                
mycursor.execute("SELECT * FROM aggregated_transaction;")
table2 = mycursor.fetchall()
Aggre_transaction = pd.DataFrame(table2, columns=("States", "Years", "Quarter", "Transaction_Type", "Transaction_Count", "Transaction_Amount"))

# Aggregated_user
mycursor.execute("SELECT * FROM aggregated_user;")
table3 = mycursor.fetchall()
Aggre_user = pd.DataFrame(table3, columns=("States", "Years", "Quarter", "Brands", "Counts", "Percentages"))

# Map_insurance
mycursor.execute("SELECT * FROM map_insurance;")
table4 = mycursor.fetchall()
Map_insurance = pd.DataFrame(table4, columns=("States", "Years", "Quarter", "Districts", "Transaction_Count", "Transaction_Amount"))

# Map_transaction
mycursor.execute("SELECT * FROM map_transaction;")
table5 = mycursor.fetchall()
Map_transaction = pd.DataFrame(table5, columns=("States", "Years", "Quarter", "Districts", "Transaction_Count", "Transaction_Amount"))

# Map_user
mycursor.execute("SELECT * FROM map_user;")
table6 = mycursor.fetchall()
Map_user = pd.DataFrame(table6, columns=("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

# Top_insurance
mycursor.execute("SELECT * FROM top_insurance;")
table7 = mycursor.fetchall()
Top_insurance = pd.DataFrame(table7, columns=("States", "Years", "Quarter", "Pincode", "Transaction_Count", "Transaction_Amount"))

# Top_transaction
mycursor.execute("SELECT * FROM top_transaction;")
table8 = mycursor.fetchall()
Top_transaction = pd.DataFrame(table8, columns=("States", "Years", "Quarter", "Pincode", "Transaction_Count", "Transaction_Amount"))

# Top_user
mycursor.execute("SELECT * FROM top_user;")
table9 = mycursor.fetchall()
Top_user = pd.DataFrame(table9, columns=("States", "Years", "Quarter", "Pincode", "RegisteredUsers"))


def Aggre_insurance_Y(df,year):
    aiy= df[df["Years"] == year]
    aiy.reset_index(drop= True, inplace= True)

    aiyg=aiy.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum()
    aiyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(aiyg, x="States", y= "Transaction_Amount",title= f"YEAR {year} TRANSACTION AMOUNT",
                           width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count= px.bar(aiyg, x="States", y= "Transaction_Count",title= f"YEAR {year} TRANSACTION COUNT",
                          width=600, height= 650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()
        

        fig_india_1= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_Amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_Amount"].min(),aiyg["Transaction_Amount"].max()),
                                 hover_name= "States",title = f"YEAR {year}  TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_Count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_Count"].min(),aiyg["Transaction_Count"].max()),
                                 hover_name= "States",title = f"YEAR {year} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)

    return aiy

def Aggre_insurance_Y_Q(df,quarter):
    aiyq= df[df["Quarter"] == quarter]
    aiyq.reset_index(drop= True, inplace= True)

    aiyqg= aiyq.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum()
    aiyqg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:
        fig_q_amount= px.bar(aiyqg, x= "States", y= "Transaction_Amount", 
                            title= f"YEAR {aiyq['Years'].min()} AND QUARTER {quarter} TRANSACTION AMOUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count= px.bar(aiyqg, x= "States", y= "Transaction_Count", 
                            title= f"YEAR {aiyq['Years'].min()} AND QUARTER {quarter} TRANSACTION COUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_Amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_Amount"].min(),aiyqg["Transaction_Amount"].max()),
                                 hover_name= "States",title = f"YEAR {aiyq['Years'].min()} AND QUARTER {quarter} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)
    with col2:

        fig_india_2= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_Count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_Count"].min(),aiyqg["Transaction_Count"].max()),
                                 hover_name= "States",title = f"YEAR {aiyq['Years'].min()} AND QUARTER {quarter} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)
    
    return aiyq

def Aggre_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    agttg= df_state.groupby("Transaction_Type")[["Transaction_Count", "Transaction_Amount"]].sum()
    agttg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_hbar_1= px.bar(agttg, x= "Transaction_Count", y= "Transaction_Type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(agttg, x= "Transaction_Amount", y= "Transaction_Type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)
        
def Aggre_user_plot_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Counts"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Brands",y= "Counts", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=auqs, names= "Brands", values="Counts", hover_data= "Percentages",
                      width=1000,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["Counts"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brands", y= "Counts", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)

def map_insure_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_Count","Transaction_Amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_Amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_Count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)

def map_insure_plot_2(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_Count","Transaction_Amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_Amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_Count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)

def map_user_plot_1(df, year):
    muy= df[df["Years"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyqg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                title= f"{df['Years'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muyq

def map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("Districts")[["RegisteredUser", "AppOpens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "RegisteredUser",y= "Districts",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "AppOpens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)

def top_user_plot_1(df,year):
    tuy= df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUsers", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quarter")["RegisteredUsers"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuys, x= "Quarter", y= "RegisteredUsers",barmode= "group",
                           width=1000, height= 800,color= "Pincode",hover_data="Pincode",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)

def ques1():
    brand= Aggre_user[["Brands","Counts"]]
    brand1= brand.groupby("Brands")["Counts"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Counts", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "TOP MOBILE BRANDS OF TRANSACTION COUNT")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Aggre_transaction[["States", "Transaction_Amount"]]
    lt1= lt.groupby("States")["Transaction_Amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_Amount",title= "LOWEST TRANSACTION AMOUNT AND STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= Map_transaction[["Districts", "Transaction_Amount"]]
    htd1= htd.groupby("Districts")["Transaction_Amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_Amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= Map_transaction[["Districts", "Transaction_Amount"]]
    htd1= htd.groupby("Districts")["Transaction_Amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_Amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)

def ques5():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="TOP 10 STATES WITH APPOPENS",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="LOWEST 10 STATES WITH APPOPENS",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Aggre_transaction[["States", "Transaction_Count"]]
    stc1= stc.groupby("States")["Transaction_Count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_Count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Aggre_transaction[["States", "Transaction_Count"]]
    stc1= stc.groupby("States")["Transaction_Count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_Count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Aggre_transaction[["States", "Transaction_Amount"]]
    ht1= ht.groupby("States")["Transaction_Amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_Amount",title= "HIGHEST TRANSACTION AMOUNT AND STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt = Map_transaction[["Districts", "Transaction_Amount"]]
    dt1 = dt.groupby("Districts")["Transaction_Amount"].sum().sort_values(ascending=True)
    dt2 = pd.DataFrame(dt1).reset_index().head(50)

    fig_dt = px.bar(dt2, x = "Districts", y = "Transaction_Amount", title = "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence = px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)

# Creating option menu in the side bar
with st.sidebar:
    select = option_menu("Menu", ["Home","Top Charts","Data APIs","Insights","About"], 
                icons=["house","graph-up-arrow","bar-chart-line","toggles" ,"exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "24px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
# MENU 1 - HOME
if select == "Home":
    #st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
    st.markdown(
    """
    <style>
        .title {
            font-family: 'Copperplate Gothic';
            font-size: 36px;}
    </style>
    """,
    unsafe_allow_html=True
)

    st.markdown('<p class="title">PHONEPE DATA VISUALIZATION AND EXPLORATION</p>', unsafe_allow_html=True)
    #st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    
    st.markdown("### :violet[Domain :] Fintech")
    st.markdown("### :violet[Technologies used :] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
    st.markdown("### :violet[Overview :] In this streamlit web app you can visualize the phonepe pulse data and gain lot of insights on transactions, number of users, top 10 state, district, pincode and which brand has most number of users and so on. Bar charts, Pie charts and Geo map visualization are used to get some insights.")
    
# MENU 2 - TOP CHARTS
if select == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Years**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
        
# Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="medium")
        
        with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"SELECT states, SUM(Transaction_Count) AS Transactions_Count, sum(Transaction_Amount) as Total from aggregated_transaction where years = {Year} and quarter = {Quarter} group by states order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='States',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select Districts , sum(Transaction_Count) as Total_Count, sum(Transaction_Amount) as Total from map_transaction where years = {Year} and quarter = {Quarter} group by districts order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Districts', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='Districts',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select pincode, sum(Transaction_Count) as Total_Transactions_Count, sum(Transaction_Amount) as Total from top_transaction where years = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
# Top Charts - USERS          
    if Type == "Users":
        tabs = ["Brands", "District", "Pincode", "State"]
        selected_tab = st.radio("Select a tab:", tabs)

        if selected_tab == "Brands":
            if Year == 2023 and Quarter in [1, 2, 3, 4]:
                st.markdown("#### Sorry No Data to Display for 2023 Qtr 1,2,3,4")
            elif Year == 2024 and Quarter in [1,2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2024 Qtr 1,2,3,4")
            elif Year == 2022 and Quarter in [2, 3, 4]:
                st.markdown("#### No Data Available for Quarters 2, 3, and 4 of 2022")
            else:
                mycursor.execute(f"select Brands, sum(Counts) as Total_Count, avg(Percentages)*100 as Avg_Percentage from aggregated_user where years = {Year} and quarter = {Quarter} group by Brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brands', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                            title='Top 10',
                            x="Total_Users",
                            y="Brands",
                            orientation='h',
                            color='Avg_Percentage',
                            color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig, use_container_width=True)

        elif selected_tab == "District":
            mycursor.execute(f"select Districts, sum(RegisteredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where years = {Year} and quarter = {Quarter} group by Districts order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Districts', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                        title='Top 10',
                        x="Total_Users",
                        y="Districts",
                        orientation='h',
                        color='Total_Users',
                        color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

        elif selected_tab == "Pincode":
            mycursor.execute(f"select Pincode, sum(RegisteredUsers) as Total_Users from Top_User where years = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                        values='Total_Users',
                        names='Pincode',
                        title='Top 10',
                        color_discrete_sequence=px.colors.sequential.Agsunset,
                        hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        elif selected_tab == "State":
            mycursor.execute(f"select states, sum(RegisteredUsers) as Total_Users, sum(AppOpens) as Total_Appopens from Map_User where years = {Year} and quarter = {Quarter} group by states order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['States', 'Total_Users','Total_AppOpens'])
            fig = px.pie(df, values='Total_Users',
                            names='State',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Total_AppOpens'],
                            labels={'Total_Appopens':'Total_AppOpens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

# EXPLORE DATA - USERS      
if select == "Data APIs":
    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("**Select the Analysis Method**", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            years_range = range(Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max() + 1)
            years = st.selectbox("**Select the Year**", years_range, index=0)  # Assuming the default value is the minimum year

            df_agg_insur_Y = Aggre_insurance_Y(Aggre_insurance, years)

            quarters_range = range(df_agg_insur_Y["Quarter"].min(), df_agg_insur_Y["Quarter"].max() + 1)
            quarters = st.selectbox("**Select the Quarter**", quarters_range, index=0)  # Assuming the default value is the minimum quarter

            Aggre_insurance_Y_Q(df_agg_insur_Y, quarters)

        elif method == "Transaction Analysis":
            years_range = range(Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max() + 1)
            years_at = st.selectbox("**Select the Year**", years_range, index=0)  # Assuming the default value is the minimum year

            df_agg_tran_Y = Aggre_insurance_Y(Aggre_transaction, years_at)

            quarters_range = range(df_agg_tran_Y["Quarter"].min(), df_agg_tran_Y["Quarter"].max() + 1)
            quarters_at = st.selectbox("**Select the Quarter**", quarters_range, index=0)  # Assuming the default value is the minimum quarter

            df_agg_tran_Y_Q = Aggre_insurance_Y_Q(df_agg_tran_Y, quarters_at)

            # Select the State for Analyze the Transaction type
            states_unique = df_agg_tran_Y_Q["States"].unique()
            state_Y_Q = st.selectbox("**Select the State**", states_unique, index=0)  # Assuming the default value is the first state

            Aggre_Transaction_type(df_agg_tran_Y_Q, state_Y_Q)

        elif method == "User Analysis":
            year_au = st.selectbox("Select the Year_AU", Aggre_user["Years"].unique(), index=0)  # Assuming the default value is the first year
            agg_user_Y = Aggre_user_plot_1(Aggre_user, year_au)

            quarter_au = st.selectbox("Select the Quarter_AU", agg_user_Y["Quarter"].unique(), index=0)  # Assuming the default value is the first quarter
            agg_user_Y_Q = Aggre_user_plot_2(agg_user_Y, quarter_au)

            states_unique_au = agg_user_Y["States"].unique()
            state_au = st.selectbox("**Select the State_AU**", states_unique_au, index=0)  # Assuming the default value is the first state
            Aggre_user_plot_3(agg_user_Y_Q, state_au)


    with tab2:
        method_map = st.radio("**Select the Analysis Method(MAP)**", ["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])

        if method_map == "Map Insurance Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years_m1 = st.selectbox("**Select the Year_mi**", list(range(Map_insurance["Years"].min(), Map_insurance["Years"].max() + 1)), index=0)

            df_map_insur_Y = Aggre_insurance_Y(Map_insurance, years_m1)

            col1, col2 = st.columns(2)
            with col1:
                state_m1 = st.selectbox("Select the State_mi", df_map_insur_Y["States"].unique())

            map_insure_plot_1(df_map_insur_Y, state_m1)
            
            col1, col2 = st.columns(2)
            with col1:
                quarters_m1 = st.selectbox("**Select the Quarter_mi**", df_map_insur_Y["Quarter"].unique())

            df_map_insur_Y_Q = Aggre_insurance_Y_Q(df_map_insur_Y, quarters_m1)

            col1, col2 = st.columns(2)
            with col1:
                state_m2 = st.selectbox("Select the State_miy", df_map_insur_Y_Q["States"].unique())            
            
            map_insure_plot_2(df_map_insur_Y_Q, state_m2)

        elif method_map == "Map Transaction Analysis":
            col1, col2 = st.columns(2)
            with col1:
                years_m2 = st.selectbox("**Select the Year_mi**", list(range(Map_transaction["Years"].min(), Map_transaction["Years"].max() + 1)), index=0)

            df_map_tran_Y = Aggre_insurance_Y(Map_transaction, years_m2)

            col1, col2 = st.columns(2)
            with col1:
                state_m3 = st.selectbox("Select the State_mi", df_map_tran_Y["States"].unique())

            map_insure_plot_1(df_map_tran_Y, state_m3)
            
            col1, col2 = st.columns(2)
            with col1:
                
                quarters_m2 = st.selectbox("**Select the Quarter_mi**", df_map_tran_Y["Quarter"].unique(), index=0)

            df_map_tran_Y_Q = Aggre_insurance_Y_Q(df_map_tran_Y, quarters_m2)

            col1, col2 = st.columns(2)
            with col1:
                state_m4 = st.selectbox("Select the State_miy", df_map_tran_Y_Q["States"].unique())            
            
            map_insure_plot_2(df_map_tran_Y_Q, state_m4)

        elif method_map == "Map User Analysis":
            col1, col2 = st.columns(2)
            with col1:
                year_mu1 = st.selectbox("**Select the Year_mu**", Map_user["Years"].unique(), index=0)

            map_user_Y = map_user_plot_1(Map_user, year_mu1)

            col1, col2 = st.columns(2)
            with col1:
                quarter_mu1 = st.selectbox("**Select the Quarter_mu**", map_user_Y["Quarter"].unique(), index=0)

            map_user_Y_Q = map_user_plot_2(map_user_Y, quarter_mu1)

            col1, col2 = st.columns(2)
            with col1:
                state_mu1 = st.selectbox("**Select the State_mu**", map_user_Y_Q["States"].unique(), index=0)

            map_user_plot_3(map_user_Y_Q, state_mu1)
    with tab3:
        method_top = st.radio("**Select the Analysis Method(TOP)**",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

        if method_top == "Top Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t1= st.slider("**Select the Year_ti**", Top_insurance["Years"].min(), Top_insurance["Years"].max(),Top_insurance["Years"].min())
 
            df_top_insur_Y= Aggre_insurance_Y(Top_insurance,years_t1)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t1= st.slider("**Select the Quarter_ti**", df_top_insur_Y["Quarter"].min(), df_top_insur_Y["Quarter"].max(),df_top_insur_Y["Quarter"].min())

            df_top_insur_Y_Q= Aggre_insurance_Y_Q(df_top_insur_Y, quarters_t1)

        
        elif method_top == "Top Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t2= st.slider("**Select the Year_tt**", Top_transaction["Years"].min(), Top_transaction["Years"].max(),Top_transaction["Years"].min())
 
            df_top_tran_Y= Aggre_insurance_Y(Top_transaction,years_t2)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t2= st.slider("**Select the Quarter_tt**", df_top_tran_Y["Quarter"].min(), df_top_tran_Y["Quarter"].max(),df_top_tran_Y["Quarter"].min())

            df_top_tran_Y_Q= Aggre_insurance_Y_Q(df_top_tran_Y, quarters_t2)

        elif method_top == "Top User Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t3= st.selectbox("**Select the Year_tu**", Top_user["Years"].unique())

            df_top_user_Y= top_user_plot_1(Top_user,years_t3)

            col1,col2= st.columns(2)
            with col1:
                state_t3= st.selectbox("**Select the State_tu**", df_top_user_Y["States"].unique())

            df_top_user_Y_S= top_user_plot_2(df_top_user_Y,state_t3)

#INSIGHTS OF GRAPH
if select == "Insights":

    ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Transaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Transaction Count',
                                 'States With Highest Transaction Count','States With Highest Transaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Transaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Transaction Count":
        ques7()

    elif ques=="States With Highest Transaction Count":
        ques8()

    elif ques=="States With Highest Transaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()
          
# MENU 4 - ABOUT
if select == "About":
    st.subheader("The Indian digital payments story has truly captured the world's imagination."
                 " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                 " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        
        st.write(" ")
        st.write(" ")
        st.markdown("### :blue[Download here...] ")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        
    with col2:
        
        st.subheader("Phonepe Now Everywhere..!")

