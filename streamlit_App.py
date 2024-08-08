import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as sql
import pandas as pd
import plotly.express as px
import os
import pages as pg


import streamlit as st
from streamlit_navigation_bar import st_navbar
st.set_page_config(initial_sidebar_state="collapsed", page_title="PhonePe Data Visualization", layout = "wide")

Mydb = sql.connect(host = "localhost",
                   user = "root",
                   password = "root",
                   database = "phonepedata")
mycursor = Mydb.cursor(buffered=True)

pages = ["Home", "Data Exploration", "Top10s", "Highlights", "Inspiration"]
styles = {
    "nav": {
        "background-color": "rgb(103, 57, 183)",
    },
    "div": {
        "max-width": "40rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "rgb(49, 51, 63)",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}

page = st_navbar(pages, options={"use_padding": False}, styles=styles)


#----------------------------------------------HOME PAGE-----------------------------------------------------------------

if page == "Home":
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTK72RBoNYIExapV2XAQoVVBZQJz2oJsk9SHg&s",width = 500)
    #st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTK72RBoNYIExapV2XAQoVVBZQJz2oJsk9SHg&s",width = 500)
    st.header("This is an App developed for visualizing and exploring PhonePe data.PhonePe is a digital wallet and financial services company in India that allows users to make payments and access other services. The app is based on the Unified Payments Interface (UPI) and was founded in 2015 by Sameer Nigam, Rahul Chari, and Burzin Engineer. It's available on Android and Apple phones and offers services in over 11 regional languages.")


#----------------------------------------------Top10s PAGE-----------------------------------------------------------------


if page == "Top10s":
    st.markdown("## :blue[Top 10 States with highest transaction amount]")
    mycursor.execute(f"SELECT* from (SELECT year,State,(Transaction_amount),Transaction_count, ROW_NUMBER() OVER( PARTITION BY year ORDER BY Transaction_amount DESC) rowNum FROM aggregated_trans) nn WHERE rowNum<={10}")
    df4 = pd.DataFrame(mycursor.fetchall(), columns=['year','State','Transaction_amount','Transaction_count','rowNum'])
    #fig = px.line(df4, x="Transaction_count", y="Transaction_amount",color='State',orientation='v',markers=True)

    fig = px.scatter(df4, x="year", y="Transaction_count",
                     size="Transaction_amount",
                     hover_name="State",
                     color='State', 
                     size_max=60,
                     color_continuous_scale='Plasma',
                     color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_traces(textposition="bottom right")

    st.plotly_chart(fig,use_container_width=True)

    st.markdown("## :blue[Top Charts]")
    
    colum1,colum2= st.columns([1,8],gap="small")
    with colum1:
        Type = st.selectbox("**Type**", ("Transactions", "Users", "Insurance"))

        if Type == "Insurance":
            Year=st.selectbox('**Year**',('2020','2021','2022','2023','2024'))
        else:
            Year=st.selectbox('**Year**',('2018','2019','2020','2021','2022','2023','2024'))
        

        if Year == "2024":
            Quarter=st.selectbox('**Quarter**',('1'))
        elif Type == "Insurance" and Year == "2020":
            Quarter=st.selectbox('**Quarter**',('2','3','4'))
        else:
            Quarter=st.selectbox('**Quarter**',('1','2','3','4'))


    
        
    with colum2:
        
        if Type == "Transactions":
            col1,col2,col3 = st.columns([1,1,1],gap="large")
            
            with col1:
                st.markdown("### :green[Top 10 State]")
                mycursor.execute(f"select State, sum(Transaction_count) AS Total_Transactions_Count,sum(Transaction_amount) AS Total from aggregated_trans where Year = {Year} AND Quarter = {Quarter} group by State order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions_Count', 'Total']) 
                fig = px.pie(df, values='Total',
                                names='State',
                                color_discrete_sequence=px.colors.sequential.Plasma,
                                hover_data=['Total_Transactions_Count'],
                                labels={'Total_Transactions_Count':'Total_Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
                
            with col2:
                st.markdown("### :green[Top 10 District]")
                mycursor.execute(f"select District , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where Year = {Year} and Quarter = {Quarter} group by District order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Count','Total'])

                fig = px.pie(df, values='Total',
                                names='District',
                                #  title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Count'],
                                labels={'Total_Count':'Total_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
                
            with col3:
                st.markdown("### :green[Top 10 Pincode]")
                mycursor.execute(f"select Pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_Amount) as Total from top_trans where Year = {Year} and  Quarter= {Quarter} group by Pincode  order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Transactions_Count','Total'])
                fig = px.pie(df, values='Total',
                                names='Pincode',
                                #  title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Viridis,
                                hover_data=['Total_Transactions_Count'],
                                labels={'Total_Transactions_Count':'Total_Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)    
# --------------------------------------------------------------------------------------
        if Type == "Users":
            col1,col2 = st.columns([2,2],gap="small")
            
            
                
            with col1:
                st.markdown("### :green[Pincode]")
                mycursor.execute(f"select Pincode, sum(RegisteredUsers) as Total_Users from top_user where Year = {Year} and Quarter= {Quarter} group by Pincode order by Total_Users desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'registered_user'])
                fig = px.pie(df,
                            values='registered_user',
                            names='Pincode',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Viridis,
                            hover_data=['registered_user'])
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
                
            with col2:
                st.markdown("### :green[State]")
                mycursor.execute(f"select State, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where Year = {Year} and Quarter= {Quarter} group by State order by Total_Users desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'registered_user','app_opens'])
                fig = px.pie(df, values='registered_user',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['app_opens'],
                                labels={'app_opens':'app_opens'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)

            with col1:
                st.markdown("### :green[Brands]")
                if Year == 2022 and Quarter in [2,3,4]:
                    st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
                else:
                    mycursor.execute(f"select Brands, SUM(Count) as total_user_count, AVG(Percentage) * 100 as avg_user_percentage from aggregate_user where Year = {Year} and Quarter = {Quarter} group by Brands order by total_user_count desc limit 10")
                    df = pd.DataFrame(mycursor.fetchall(), columns=['Brands', 'total_user_count', 'avg_user_percentage'])

                    import plotly.express as px
                    fig = px.bar(
                        df,
                        title='Top 10 User Brands',
                        x="total_user_count",
                        y="Brands",
                        orientation='h',
                        color='avg_user_percentage',
                        color_discrete_sequence=px.colors.sequential.Viridis)

                    fig.update_layout(xaxis_title='Total User Count', yaxis_title='User Brand')
                    st.plotly_chart(fig, use_container_width=True)
    
        
            with col2:
                st.markdown("### :green[District]")
                mycursor.execute(f"select District, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where Year = {Year} and Quarter= {Quarter} group by District,RegisteredUser order by Total_Users  desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'registered_user','app_opens'])
                df.registered_user = df.registered_user.astype(float)
                fig = px.bar(df,
                            title='Top 10',
                            x="registered_user",
                            y="District",
                            orientation='h',
                            color='registered_user',
                            color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)

        if Type == "Insurance":
            col1,col2,col3 = st.columns([1,1,1],gap="large")
            
            with col1:
                st.markdown("### :green[Top 10 State]")
                mycursor.execute(f"select State, sum(Transaction_count) AS Total_Transactions_Count,sum(Transaction_amount) AS Total from aggregated_Insur where Year = {Year} AND Quarter = {Quarter} group by State order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Transactions_Count', 'Total']) 
                fig = px.pie(df, values='Total',
                                names='State',
                                color_discrete_sequence=px.colors.sequential.Plasma,
                                hover_data=['Total_Transactions_Count'],
                                labels={'Total_Transactions_Count':'Total_Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
                
            with col2:
                st.markdown("### :green[Top 10 District]")
                mycursor.execute(f"select District , sum(Count) as Total_Count, sum(Amount) as Total from map_Insur where Year = {Year} and Quarter = {Quarter} group by District order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Count','Total'])

                fig = px.pie(df, values='Total',
                                names='District',
                                #  title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Count'],
                                labels={'Total_Count':'Total_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
                
            with col3:
                st.markdown("### :green[Top 10 Pincode]")
                mycursor.execute(f"select Pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_Amount) as Total from top_Insur where Year = {Year} and  Quarter= {Quarter} group by Pincode  order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Transactions_Count','Total'])
                fig = px.pie(df, values='Total',
                                names='Pincode',
                                #  title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Viridis,
                                hover_data=['Total_Transactions_Count'],
                                labels={'Total_Transactions_Count':'Total_Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
#----------------------------------------------Data Exploration PAGE-----------------------------------------------------------------

if page == "Data Exploration":

    st.markdown("<marquee><h4>Choose Type, Year and Quarter to Explore data</h4></marquee>", unsafe_allow_html=True)
    colum1,colum2= st.columns([1,6],gap="small")
    
    with colum1:
        
        Type = st.selectbox("**Type**", ("Transactions", "Users", "Insurance"))

        if Type == "Insurance":
            Year=st.selectbox('**Year**',('2020','2021','2022','2023','2024'))
        else:
            Year=st.selectbox('**Year**',('2018','2019','2020','2021','2022','2023','2024'))
        

        if Year == "2024":
            Quarter=st.selectbox('**Quarter**',('1'))
        elif Type == "Insurance" and Year == "2020":
            Quarter=st.selectbox('**Quarter**',('2','3','4'))
        else:
            Quarter=st.selectbox('**Quarter**',('1','2','3','4'))
    
    with colum2:
        
        #---Transactions   
        if Type == "Transactions":     
            col1,col2 = st.columns([1,1],gap="large")
            # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
            with col1:
                st.markdown("## :violet[State wise - Transactions Amount]")
                mycursor.execute(f"select State, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_trans where Year = {Year} and Quarter= {Quarter} group by State order by State")
                df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
                statename_list = "C:/Users/ashfaq.ahamed/Documents/projects1/PhonePe/state_names.csv"
                df2 = pd.read_csv(statename_list)
                df1['state'] = df2['state']
                
                
                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='state',
                            color='Total_amount',
                            color_continuous_scale='YlOrBr')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)
                
            with col2:
                    st.markdown("## :violet[State wise - Transaction count]")
                    mycursor.execute(f"select State, sum(Count) as Total_Transactions, sum(Amount) as Total_amount from map_trans where Year = {Year} and Quarter= {Quarter} group by State order by State")
                    df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
                    df2 = pd.read_csv(statename_list)
                    # df1.transaction_count = df1.transaction_count.astype(int )
                    df1['state'] = df2['state']
                    
                    
                    fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='state',
                                color='Total_Transactions',
                                color_continuous_scale='YlOrBr')

                    fig.update_geos(fitbounds="locations", visible=False)
                    st.plotly_chart(fig,use_container_width=True)
                    
            with col1:   
                    # BAR CHART - TOP PAYMENT TYPE
                    st.markdown("## :violet[Top Payment Type]")
                    mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions_count, sum(Transaction_amount) as Total_Transactions_amount from aggregated_trans where Year= {Year} and Quarter = {Quarter} group by Transaction_type order by Transaction_type")
                    df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions_count','Total_Transactions_amount'])

                    fig = px.bar(df,
                                title='Transaction Types vs Total_Transactions',
                                x="Transaction_type",
                                y="Total_Transactions_count",
                                orientation='v',
                                color='Total_Transactions_amount',
                                color_continuous_scale=px.colors.sequential.YlOrBr)
                    st.plotly_chart(fig,use_container_width=False) 
            with col2:
                    # BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
                    st.markdown("## :violet[Select any State to explore more]")
                    selected_state = st.selectbox("",
                                        ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                                        'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                                        'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                                        'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                                        'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                                        'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
                    
                    mycursor.execute(f"select State, District,Year,Quarter, sum(Count) as Total_Transactions_count, sum(Amount) as Total_transaction_amount from map_trans where Year = {Year} and Quarter = {Quarter} and State = '{selected_state}' group by State, District,Year,Quarter order by State,District")
                    
                    df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                                    'Total_Transactions_count','Total_transaction_amount'])
                    fig = px.bar(df1,
                                title=selected_state,
                                x="District",
                                y="Total_Transactions_count",
                                orientation='v',
                                color='Total_transaction_amount',
                                color_continuous_scale=px.colors.sequential.YlOrBr)
                    st.plotly_chart(fig,use_container_width=True)

    #  ------------Users-----------------------------------
    
        if Type == "Users":
            col1,col2= st.columns(2)   
            # Overall State Data - User App Opening Frequency
            st.markdown("## :violet[Overall State Data - User App Opening Frequency]")
            mycursor.execute(f"SELECT State, SUM(RegisteredUser) AS Total_Users, SUM(AppOpens) AS Total_Appopens FROM map_user WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State ORDER BY State")
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
            statename_list = "C:/Users/ashfaq.ahamed/Documents/projects1/PhonePe/state_names.csv"
            df2 = pd.read_csv(statename_list)  # Assuming you have a CSV file with state names
            df1['Total_Appopens'] = df1['Total_Appopens'].astype(float)
            df1['state'] = df2['state']

            fig = px.choropleth(
                df1,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='state',
                color='Total_Appopens',
                color_continuous_scale='YlOrBr'
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)

            # BAR CHART TOTAL USERS - DISTRICT WISE DATA
            st.markdown("## :violet[Choose State to view District trend]")
            selected_state = st.selectbox(
                "",
                ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
                'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana',
                'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'), index=30)

            mycursor.execute(
                f"SELECT State, Year, Quarter, District, SUM(RegisteredUser) AS Total_Users, SUM(AppOpens) AS Total_Appopens FROM map_user WHERE Year = {Year} AND Quarter = {Quarter} AND State = '{selected_state}' GROUP BY State, District, Year, Quarter ORDER BY State, District")

            df = pd.DataFrame(mycursor.fetchall(),
                            columns=['State', 'Year', 'Quarter', 'District', 'Total_Users', 'Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(int)

            fig = px.bar(df,
                        title=selected_state,
                        x="District",
                        y="Total_Users",
                        orientation='v',
                        color='Total_Users',
                        color_continuous_scale=px.colors.sequential.YlOrBr)
            st.plotly_chart(fig, use_container_width=True)


        if Type == "Insurance":
                col1,col2= st.columns(2)   
                # Overall State Data - User App Opening Frequency
                st.markdown("## :violet[State Wise - Insurance Count]")
                mycursor.execute(f"SELECT State, SUM(Amount) AS Total_Insurance_Amount, SUM(count) AS Total_Insurance_Count FROM map_Insur WHERE Year = {Year} AND Quarter = {Quarter} GROUP BY State ORDER BY State")
                df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Insurance_Count', 'Total_Insurance_Amount'])
                statename_list = "C:/Users/ashfaq.ahamed/Documents/projects1/PhonePe/state_names.csv"
                df2 = pd.read_csv(statename_list)  # Assuming you have a CSV file with state names
                df1['Total_Insurance_Count'] = df1['Total_Insurance_Amount'].astype(float)
                df1['state'] = df2['state']

                fig = px.choropleth(
                    df1,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='state',
                    color='Total_Insurance_Count',
                    color_continuous_scale='YlOrBr'
                )
                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig, use_container_width=True)

                # ---District-Wise Data

                st.markdown("## :violet[District Wise Data]")
                selected_state = st.selectbox(
                    "",
                    ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
                    'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana',
                    'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                    'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                    'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                    'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'), index=30)

                mycursor.execute(
                    f"SELECT State, Year, Quarter, District, SUM(Amount) AS Total_Insurance_Amount, SUM(count) AS Total_Insurance_Count FROM map_Insur  WHERE Year = {Year} AND Quarter = {Quarter} AND State = '{selected_state}' GROUP BY State, District, Year, Quarter ORDER BY State, District")

                df = pd.DataFrame(mycursor.fetchall(),
                                columns=['State', 'Year', 'Quarter', 'District', 'Total_Insurance_Count', 'Total_Insurance_Amount'])
                #df.Total_Users = df.Total_Insurance_Count.astype(int)

                fig = px.bar(df,
                            title=selected_state,
                            x="District",
                            y="Total_Insurance_Count",
                            orientation='v',
                            color='Total_Insurance_Count',
                            color_continuous_scale=px.colors.sequential.YlOrBr)
                st.plotly_chart(fig, use_container_width=True)

                
#----------------------------------------------Highlights PAGE-----------------------------------------------------------------

if page == "Highlights":

    colum1,colum2= st.columns([1,1],gap="small")
    with colum1:
        
        st.markdown("## :violet[Transaction Growth[Rupees]]")
        mycursor.execute(f"select Year, sum(Transaction_amount) AS Total_Transaction_Amount from aggregated_trans group by Year")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Year','Total_Transactions_amount'])
        #id_cols = ['Year']
        #value_cols =  ['Total_Transactions_amount', 'Total_Transactions_Count']  # Columns to transpose

        #df_melted = df.melt(id_vars=id_cols, value_vars=value_cols, 
        #         var_name='Cases', value_name='Value')
        
        fig = px.bar(df, x='Year', y='Total_Transactions_amount')
        st.plotly_chart(fig,use_container_width=True)



        #---Insurance Feedback-----------

        


    
    with colum2:
        
        st.markdown("## :violet[Transaction Count Growth]")
        mycursor.execute(f"select Year, sum(Transaction_count) AS Total_Transactions_Count from aggregated_trans group by Year")
        df2 = pd.DataFrame(mycursor.fetchall(), columns=['Year','Total_Transactions_Count'])

        fig1 = px.bar(df2, x='Year', y='Total_Transactions_Count',orientation='v')
        st.plotly_chart(fig1,use_container_width=True)


    st.markdown("## :violet[User Growth Vs Insurance Count]")
    mycursor.execute(f"select  year,quarter, SUM(RegisteredUser) AS Total_Reg_User from map_user GROUP BY year,quarter ORDER BY year,quarter;")
    df3 = pd.DataFrame(mycursor.fetchall(), columns=['year','quarter','Total_Insurance_count'])

    mycursor.execute(f"select  year, quarter, sum(Transaction_count) AS Total_Insurance_count from aggregated_Insur group by year, quarter order by year, quarter")
    df4 = pd.DataFrame(mycursor.fetchall(), columns=['year','quarter','Total_Reg_User'])

    outdf = pd.merge(df3,df4, on = ["year", "quarter"],how ='right')

        

    fig1 = px.line(outdf, x="Total_Insurance_count", y="Total_Reg_User",hover_data=['year','quarter'],orientation='v')

    st.plotly_chart(fig1,use_container_width=True)
    #with colum2:

if page == "Inspiration":
    st.link_button("Inspired From", "https://www.phonepe.com/pulse/explore/transaction/2024/2/")
