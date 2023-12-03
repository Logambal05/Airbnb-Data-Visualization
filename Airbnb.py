import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pymongo
import plotly.express as px
from warnings import filterwarnings
filterwarnings('ignore')

# Theme   
primaryColor="#0f8e8e"
backgroundColor="#c6f9f9"
secondaryBackgroundColor="#23b3b3"
textColor="#0a0a0a"
font="serif"

# Config
st.set_page_config(layout='wide')

# MongoDB Connection
client = pymongo.MongoClient("mongodb+srv://logi2987:Logambal2908@cluster0.efxxi9b.mongodb.net/?retryWrites=true&w=majority")
mydb = client['sample_airbnb']
collection = mydb['listingsAndReviews']

def Datacollection_one():
    data1 = collection.find_one()
    data = dict(Name = data1['name'],
           PropertyType= data1['property_type'],
           HostID = data1['host']['host_id'],
           HostName = data1 ['host']['host_name'],
           HostLocation = data1['host']['host_location'],
           HostResponseTime = data1['host']['host_response_time'],
           HostResponseRate = data1['host']['host_response_rate'],
           RoomType = data1['room_type'],
           BedType = data1['bed_type'],
           MinNights = data1['minimum_nights'],
           MaxNights = data1['maximum_nights'],
           GuestCount = data1['accommodates'],
           ExtraGuestCount = data1['extra_people'],
           GuestWithPay = data1['guests_included'],
           BedRoomsCount = data1['bedrooms'],
           No_Of_Beds= data1['beds'],
           No_Of_Bathrooms = data1['bathrooms'],
           CancellationPolicy = data1['cancellation_policy'],
           Price = data1['price'],
           Address_Property = data1['address']['street'],
           Location = data1['address']['country'],
           LocationCode = data1['address']['country_code'],
           Longitude = data1['address']['location']['coordinates'][0],
           Latitude = data1['address']['location']['coordinates'][1],
           Availability_365 = data1['availability']['availability_365'],
           Is_location_exact = data1['address']['location']['is_location_exact'],
           Total_ReviewsCount = data1['number_of_reviews'],
           ReviewScores = data1['review_scores']['review_scores_accuracy'])
    return data

# Whole Dataset
def dataframe():
    df = pd.read_csv("C:/Users/Logambal/Desktop/PROJECT-GUVI/Airbnb_Analysis.csv")
    return df

# Option Menu
with st.sidebar:
        SELECT = option_menu(None,
                options = ["🏡Home","🎢Amenity Exploration","🔚Exit"],
                default_index=0,
                orientation="vertical",
                styles={"container": {"width": "90%"},
                        "icon": {"color": "white", "font-size": "18px"},
                        "nav-link": {"font-size": "18px"}})

if SELECT == "🏡Home":
      st.header("Airbnb Analytics with MongoDB: Unveiling Trends")
      st.write("""
               This project utilizes MongoDB Atlas to analyze Airbnb data, emphasizing pricing, availability, and location trends. 
               Objectives include establishing an efficient MongoDB connection, conducting rigorous data cleaning, and developing a 
               streamlit web app with interactive geospatial visuals. The goal is to empower users to explore Airbnb listings
               comprehensively, considering factors like pricing and ratings.""")
      st.subheader("Tools Used:")
      st.markdown("""
        - **Python:** Facilitates versatile programming capabilities.
        - **MongoDB (via MongoDB Atlas):** Ensures scalable and efficient data storage.
        - **Pandas:** Refines and prepares data for accurate analysis.
        - **Matplotlib:** Crafts static visualizations to uncover trends.
        - **Plotly:** Creates dynamic and interactive visual displays.
        - **Streamlit:** Enables the development of a user-friendly web application for exploring Airbnb data.
        """)

if SELECT == "🎢Amenity Exploration":
    Option = st.sidebar.selectbox("**Select Any One Option:**", (None,'Data Acquisition','Geographical Details','Property Highlights','Host Profile Analysis','Tenant Testimonials Analysis'))
    if Option == None:
        st.subheader('**_You Can Explore The GUI With Below Options!_**')
        st.markdown ("""
                - **Data Acquisition**
                - **Geographical Details**
                - **Property Highlights**
                - **Host Profile Analysis**
                - **Tenant Testimonials Analysis**""")
    if Option == 'Data Acquisition':
        tab1, tab2 = st.tabs([f'**_Represented A Data In JSON_**', f'**_Organized Data In A DataFrame_**'])
        with tab1:
            st.write(Datacollection_one())
        with tab2:
            df = dataframe()
            st.dataframe(df)

    if Option == "Geographical Details":
        df = dataframe()
        tab3,tab4=st.tabs([f'**_Map Visualizing Average Property Prices Across Countries._**', f'**_Visualize Property Prices Across Room Types On A Map_**'])
        with tab3:
            df_con = df.groupby(['Location', 'PropertyType']).agg({'Price': 'mean'}).reset_index().sort_values(by='PropertyType', ascending=False)
            fig = px.scatter_geo(data_frame=df_con,
                                locations='Location',
                                color= 'Price', 
                                hover_data=['PropertyType'],
                                locationmode='country names',
                                color_continuous_scale='teal',
                                size='Price',
                                title= 'Average Price Of The Property In Different Countries')
            st.plotly_chart(fig,use_container_width=True)
        with tab4:
            df_concode = df.groupby(['Location', 'RoomType','LocationCode']).agg({'Price': 'mean','Availability_365': lambda x: round(x.mean())}).reset_index().sort_values(by='RoomType')
            fig = px.scatter_geo(data_frame=df_concode,
                           locations='Location',
                           color= 'Price', 
                           hover_data=['RoomType','LocationCode'],
                           locationmode='country names',
                           color_continuous_scale='teal',
                           size='Price',
                           title= 'Price Of The Property Based On Types Of Rooms')
            st.plotly_chart(fig,use_container_width=True)

    if Option == 'Property Highlights':
        df = dataframe()
        colors =['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
        tab5,tab6=st.tabs([f'**_Verify The Availability of Rooms_**',f'**_Viewing The Properties Of The Features_**'])
        with tab5:
            country = st.selectbox('Select a Country',sorted(df.Location.unique()))
            prop = st.selectbox('Select Property Type',sorted(df.PropertyType.unique()))
            room=st.selectbox('Select Room Type',sorted(df.RoomType.unique()))
            button=st.button("Click Me To Discover More!")
            if button:               
                df1=df[(df["Location"]==country)&(df["PropertyType"]==prop)&(df["RoomType"]==room)]
                df2=df1[["Location","PropertyType","RoomType","Price","Availability_365","MinNights","MaxNights"]].sort_values(by="Price",ascending=False).reset_index(drop=True)
                st.dataframe(df2)
        with tab6:
            st.subheader('**_Price Distribution Using Various Features_**')
            result_df = df.groupby('RoomType')['Price'].mean().reset_index()
            fig = px.pie(result_df, names='RoomType', values='Price', title='Average Price Distribution by Room Type',color_discrete_sequence = colors)
            fig.update_traces(textposition='inside', textinfo='label+percent')
            fig.update_layout(width=300, height=400)
            st.plotly_chart(fig,use_container_width=True)

            result_df1 = df.groupby('PropertyType')['Price'].mean().reset_index().sort_values(by='Price', ascending=True)
            fig = px.bar(result_df1, x="PropertyType", y="Price", title="Average Price Distribution by Property Type")
            fig.update_traces(marker_color='teal')
            fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Property Type Nationwide')
            fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Average Price Of Property')
            fig.update_layout(width=10,height=500)
            st.plotly_chart(fig,use_container_width=True)

            df_ni = df.groupby(['Location','Currency']).agg({'Price': 'mean'}).reset_index().sort_values(by='Price', ascending=False)
            df_ni.reset_index(drop=True, inplace=True)
            fig = px.pie(df_ni, names='Location', values='Price',hover_data ='Currency', title='Average Price Distribution by Location',color_discrete_sequence = colors)
            fig.update_traces(textposition='inside', textinfo='label+percent')
            fig.update_layout(width=300, height=400)
            st.plotly_chart(fig,use_container_width=True)  
            
    
    if Option == "Host Profile Analysis":
        df = dataframe()
        result_df4 = df.groupby('HostName')['Total_ReviewsCount'].sum().reset_index().sort_values(by='Total_ReviewsCount', ascending=False).head(10)
        fig = px.bar(result_df4 , x="HostName", y="Total_ReviewsCount", title="Top10 Host Based On Reviews Count")
        fig.update_traces(marker_color='teal')
        fig.update_xaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Top10 HostName')
        fig.update_yaxes(title_font=dict(size=18, family='serif', color='black'), title_text='Top Reviews Count Based HostName')
        fig.update_layout(width=10,height=600)
        st.plotly_chart(fig,use_container_width=True)

        colors = ['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
        fig = px.pie(df, names='HostResponseTime', title='Host Response Time', color='HostResponseTime', color_discrete_sequence=colors)
        fig.update_traces(textposition='inside', textinfo='label+percent')
        fig.update_layout(width=300, height=400)
        st.plotly_chart(fig, use_container_width=True)

    if Option == "Tenant Testimonials Analysis":
        df = dataframe()
        colors = ['mediumturquoise', 'teal', 'darkcyan', 'cadetblue', 'lightseagreen']
        tab7 , tab8 =st.tabs(['**_Total Review Counts_**','**_Review Score Accuracy_**'])
        with tab7:
            # Total Review count Based On Property Type
            st.subheader("**_Total Review Count Based On Property_**")
            df_ni = df.groupby('PropertyType').agg({'Total_ReviewsCount': 'sum'}).reset_index().sort_values(by='Total_ReviewsCount', ascending=False)
            fig = px.pie(df_ni, names='PropertyType', values= 'Total_ReviewsCount', title='Total Review Count Based On Property Type', color='Total_ReviewsCount', color_discrete_sequence=colors)
            fig.update_traces(textposition='inside', textinfo='label+percent')
            fig.update_layout(width=300, height=500)
            st.plotly_chart(fig, use_container_width=True)
            # Total Review count Based On Room Type
            st.subheader("**_Total Review Count Based On Rooms_**")
            df_ni = df.groupby('RoomType').agg({'Total_ReviewsCount': 'sum'}).reset_index().sort_values(by='Total_ReviewsCount', ascending=False)
            st.dataframe(df_ni)
            fig = px.pie(df_ni, names='RoomType', values= 'Total_ReviewsCount', title='Total Review Count Based On Room Type', color='Total_ReviewsCount', color_discrete_sequence=colors)
            fig.update_traces(textposition='inside', textinfo='label+percent')
            fig.update_layout(width=300, height=400)
            st.plotly_chart(fig, use_container_width=True)

        with tab8:
            # Total Review Score Accuracy Based On Property Type
            st.subheader("**_Review Score Accuracy Based On Property_**")
            df_ni = df.groupby('PropertyType').agg({'ReviewScores': 'mean'}).reset_index().sort_values(by='ReviewScores', ascending=False)
            fig = px.pie(df_ni, names='PropertyType', values= 'ReviewScores', title='Total Review Score Accuracy Based On Property Type', color='ReviewScores', color_discrete_sequence=colors)
            fig.update_traces(textposition='inside', textinfo='label+percent')
            fig.update_layout(width=300, height=500)
            st.plotly_chart(fig, use_container_width=True)
            # Total Review Score Accuracy Based On Room Type
            st.subheader("**_Review Score Accuracy Based On Rooms_**")
            df_ni = df.groupby('RoomType').agg({'ReviewScores': 'mean'}).reset_index().sort_values(by='ReviewScores', ascending=False)
            st.dataframe(df_ni)
            fig = px.pie(df_ni, names='RoomType', values= 'ReviewScores', title='Total Review Score Accuracy Based On Room Type', color='ReviewScores', color_discrete_sequence=colors)
            fig.update_traces(textposition='inside', textinfo='label+percent')
            fig.update_layout(width=300, height=400)
            st.plotly_chart(fig, use_container_width=True)

if SELECT == "🔚Exit":
    st.header("OverView Of The UI")
    st.write("""Thank you for exploring the Airbnb Data Analysis GUI. This tool provides valuable insights into pricing variations, availability patterns, and location-based trends in 
            the Airbnb dataset. Users can interactively explore dynamic visualizations, gaining a deeper understanding of the data. Remember to check the comprehensive dashboard in 
            Power BI for a consolidated view of key insights.""")
    st.subheader('**_Happy Analyzing!_**')
    but=st.button("EXIT!")
    if but:
        st.success("Thank you for utilizing this platform. I hope you gained some knowledge regarding Airbnb and found useful information to make your trip easier and more insightful!❤️")
   
                    



