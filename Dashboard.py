import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import urllib.parse

# Streamlit App Title & Config

st.set_page_config(page_title = "Ola Ride Insights", page_icon = "🚕", layout = "wide")

#Creating Engine
@st.cache_resource
def get_connection():
    password = urllib.parse.quote_plus("Pillu@7800_")
    engine = create_engine(f"mysql+pymysql://root:{password}@localhost/wd_aiml")
    return engine
engine = get_connection()


# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go To", [
    "Home",
    "SQL Phase"
])


# ------------------------- Home -------------------------
if page == "Home":
    st.image("Pictures/OLA.webp")
    st.header("A Streamlit App for Ola Ride Insights")
    st.write("""
             Ola Ride Insights is an interactive data analytics dashboard built using Streamlit 
             to explore and visualize ride booking trends, customer behavior, driver performance, cancellations, 
             revenue patterns, and ride completion statistics. 
             It helps transform raw ride data into meaningful insights through dynamic charts and analysis.
             
             ##### What Will You Explore:
            - Ride booking and completion trends
            - Revenue and booking value analysis
            - Customer and driver cancellation patterns
            - Vehicle type performance and demand
            - Customer ratings and driver ratings insights
            - Payment method distribution
            - Incomplete ride reasons and ride status analysis
            - Key operational metrics and business insights from ride data
            - Short, professional, and Streamlit dashboard–friendly. 🚖📊
             

             ##### Why This Phase Matters:

            This phase is important because it helps uncover meaningful patterns from ride booking data. 
             By analyzing bookings, cancellations, revenue, customer behavior, and driver performance, 
             businesses can make data-driven decisions, improve operational efficiency, 
             and enhance the overall customer experience.
             
            **Database Used:** `wd_aiml`
            **Primary Table:** `ola_dataset`
             """)

# ------------------------- SQL Phase -------------------------

elif page == "SQL Phase":
 
    st.title("SQL Phase")
    st.write(""" In this phase, SQL is used to extract, filter, aggregate, and analyze ride booking data. 
             Various queries are performed to uncover trends, measure performance, 
             and generate meaningful insights from the dataset.
            """)
    query1 = """
        SELECT SUM(Booking_Value) AS Total_Booking_Value
        FROM ola_dataset
        WHERE Booking_Status = 'Success'
        """
    
        # Customer Cancelled Rides
    query2 = """
        SELECT COUNT(*) AS Cancelled_by_customers
        FROM ola_dataset
        WHERE Booking_Status = 'Canceled by Customer'
        """
    
        # Prime Sedan Ratings
    query3 = """
        SELECT
            MIN(Driver_Ratings) AS Min_Driver_Rating,
            MAX(Driver_Ratings) AS Max_Driver_Rating
        FROM ola_dataset
        WHERE Vehicle_Type = 'Prime Sedan'
        """
    df_booking = pd.read_sql(query1, con=engine)
    df_cancel = pd.read_sql(query2, con=engine)
    df_rating = pd.read_sql(query3, con=engine)
    
    total_booking_value = df_booking.iloc[0, 0]
    cancelled_rides = df_cancel.iloc[0, 0]
    
    min_rating = df_rating['Min_Driver_Rating'][0]
    max_rating = df_rating['Max_Driver_Rating'][0]
    
    st.markdown("""
            <style>
            .kpi-card {
                padding: 20px;
                border-radius: 18px;
                text-align: center;
                color: white;
                box-shadow: 0px 8px 25px rgba(0,0,0,0.25);
                transition: 0.3s;
            }

            .kpi-card:hover {
                transform: translateY(-5px);
            }

            .revenue {
                background: linear-gradient(135deg,#667eea,#764ba2);
            }

            .cancel {
                background: linear-gradient(135deg,#ff6b6b,#ee0979);
            }

            .max-rating {
                background: linear-gradient(135deg,#11998e,#38ef7d);
            }

            .min-rating {
                background: linear-gradient(135deg,#f7971e,#ffd200);
            }

            .kpi-title{
                font-size:16px;
                font-weight:600;
            }

            .kpi-value{
                font-size:32px;
                font-weight:bold;
            }
            </style>
            """, unsafe_allow_html=True)
    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card revenue">
            <div class="kpi-title">💰 Total Booking Value</div>
            <div class="kpi-value">₹{total_booking_value:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card cancel">
            <div class="kpi-title">❌ Customer Cancellations</div>
            <div class="kpi-value">{cancelled_rides:,}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card max-rating">
            <div class="kpi-title">⭐ Max Driver Rating</div>
            <div class="kpi-value">{max_rating}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card min-rating">
            <div class="kpi-title">⭐ Min Driver Rating</div>
            <div class="kpi-value">{min_rating}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.subheader("Data Set")
    @st.cache_data
    def load_data():
        query = "select * from ola_dataset Limit 5"
        return pd.read_sql(query, con = engine)
    df_sql = load_data()
    st.write(df_sql)

     #Row Count Check
    st.subheader("Total Row")
    st.write("""In a SQL database, a row (also called a record or tuple) represents a single, 
             complete structured data item within a table.""")
    row = pd.read_sql("select count(*) as Total_Row from ola_dataset",
                      con = engine)
    st.write(row)


     #Schema Check
    st.subheader("Schema Check")
    st.write("""A SQL schema is a blueprint or logical container that 
             organizes database objects like tables, views, and stored procedures.""")
    Schema = pd.read_sql("Describe ola_dataset", con = engine)
    st.write(Schema)

    st.write("#### SQL Queries Started")

# 1. Retrieve all successful bookings:
    with st.expander("1. Retrieve all successful bookings"):
        
        st.write("""
        **Description:**
        
        This query retrieves all ride bookings that were completed successfully.
        It helps analyze completed rides and understand successful booking patterns.
        """)

        query = """
        SELECT *
        FROM ola_dataset
        WHERE Booking_Status = 'Success'
        """

        st.code(query, language="sql")

        df = pd.read_sql(query, con=engine)

        st.write("### Output")
        st.dataframe(df)
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")


# 2. Find the average ride distance for each vehicle type:
    with st.expander("2. Find the average ride distance for each vehicle type:"):

        st.write("""
        **Description:**      
        This query calculates the average ride distance for each vehicle type. 
        It helps compare how far customers typically travel using different 
        vehicle categories and identifies usage patterns across services.
                 """)
        
        query = """
                  select Vehicle_Type,
                  Round(Avg(Ride_Distance), 2) as Avg_Ride_Distance
                  from ola_dataset
                  Group by Vehicle_Type
                  Order by Avg_Ride_Distance
                """
        st.code(query, language = "sql")
        df = pd.read_sql(query, con = engine)
        st.write("#### Output")
        fig, ax = plt.subplots(figsize = (10,4))
        plt.bar(
            data = df,
            x = "Vehicle_Type",
            height = "Avg_Ride_Distance",
            color = "Green",
            width = 0.4
        )
        plt.title("Average Ride Distance for each Vehicle type")
        plt.xlabel("Vehicle Type")
        plt.ylabel("Avg Distance of Rides")
        st.dataframe(df)
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")
        st.pyplot(fig)


# 3. Get the total number of cancelled rides by customers:
    with st.expander("3. Get the total number of cancelled rides by customers:"):

        st.write(""" 
                 **Description:**
                 This query calculates the total number of rides cancelled by customers. 
                 It helps measure customer cancellation behavior and identify its impact on overall ride operations.
                 """)

        query = """
                select count(*) as Cancelled_by_customers
                from ola_dataset
                where Booking_Status = 'Canceled by Customer'
                """
        st.code(query, language="sql")
        df = pd.read_sql(query, con = engine)
        st.write("#### Output")
        st.dataframe(df)
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")


# 4. List the top 5 customers who booked the highest number of rides:
    with st.expander("4. List the top 5 customers who booked the highest number of rides:"):

        st.write("""
                 **Description:**
                 This query identifies the top 5 customers with the highest number of ride bookings. 
                 It helps recognize frequent users and analyze customer engagement patterns.
                """)

        query = """
                select Customer_ID, count(*) as Total_Rides
                from ola_dataset
                Group by Customer_ID
                Order by Total_Rides Desc
                Limit 5
                """
        st.code(query, language="sql")
        df = pd.read_sql(query, con = engine)
        st.write("#### Output")
        fig, ax = plt.subplots(figsize = (10,4))
        plt.bar(
            data = df,
            x = "Customer_ID",
            height = "Total_Rides",
            color = "Red",
            width = 0.4)
        plt.title("TOp 5 Customers with Highest Booking Number of Rides")
        plt.xlabel("Customers ID")
        plt.ylabel("Total no. of Rides")
        st.dataframe(df)
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")
        st.pyplot(fig)


# 5. Get the number of rides cancelled by drivers due to personal and car-related issues:

    with st.expander("5. Get the number of rides cancelled by drivers due to personal and car-related issues:"):

        st.write(""" 
                 **Description:**
                 This query calculates the number of rides cancelled by drivers due to personal or car-related issues. 
                 It helps identify operational challenges and understand the impact of 
                 driver-side cancellations on service reliability.
                """)

        query = """
                select Canceled_Rides_by_Driver, count(*) as Total_Cancelled_Rides
                from ola_dataset
                Where Canceled_Rides_by_Driver = "Personal & Car related issue"
                Group by Canceled_Rides_by_Driver
                """
        st.code(query, language="sql")
        df = pd.read_sql(query, con = engine)
        st.write("#### Output")
        fig, ax = plt.subplots(figsize = (10,4))
        sns.boxplot(x = "Canceled_Rides_by_Driver", 
                    y = "Total_Cancelled_Rides",
                    data = df, 
                    color = "Red")
        plt.title("Rides Cancelled by Drivers due to Personal and Car-Related Issues")
        plt.xlabel("Reason")
        plt.ylabel("No. of cancelled rides")
        st.dataframe(df)
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")
        st.pyplot(fig)


# 6. Find the maximum and minimum driver ratings for Prime Sedan bookings:
    with st.expander("6. Find the maximum and minimum driver ratings for Prime Sedan bookings:"):

        st.write("""
                 **Description:** This query finds the highest and lowest driver ratings for Prime Sedan bookings. 
                 It helps evaluate the range of driver performance and service quality within the Prime Sedan category.
                 """)

        query = """ select Vehicle_Type,
                    MIN(Driver_Ratings) as Min_Driver_Rating,
                    MAX(Driver_Ratings) as Max_Driver_Rating
                    from ola_dataset
                    Where Vehicle_Type = "Prime Sedan"
                    Group by Vehicle_Type
                """
        st.code(query, language = "sql")
        df = pd.read_sql(query, con = engine)
        st.write("#### Output")
        fig, ax = plt.subplots(figsize = (10,4))
        plt.axis('off')
        plt.text(0.2, 0.5, f"Min Rating: {df['Min_Driver_Rating'][0]}", fontsize=14)
        plt.text(0.6, 0.5, f"Max Rating: {df['Max_Driver_Rating'][0]}", fontsize=14)

        st.dataframe(df)
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")
        st.pyplot(fig)


# 7.  Retrieve all rides where payment was made using UPI:
    with st.expander("7.  Retrieve all rides where payment was made using UPI:"):

        st.write(""" 
                 **Description:** This query retrieves all rides where the payment was made using UPI. 
                 It helps analyze customer payment preferences and track the usage of digital payment methods.
                 """)

        query = """ 
                    select *
                    from ola_dataset
                    Where Payment_Method = "UPI"
                """
        st.code(query, language="sql")
        df = pd.read_sql(query, con = engine)
        st.write("#### Output")
        st.dataframe(df)
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")


# 8. Find the average customer rating per vehicle type:

    with st.expander("8. Find the average customer rating per vehicle type:"):

        st.write("""
                 **Description:** This query calculates the average customer rating for each vehicle type. 
                 It helps compare customer satisfaction levels across different 
                 vehicle categories and identify the best-performing services.
                 """)

        query = """ 
                   select Vehicle_Type,
                   Round(AVG(Customer_Rating), 2) as Avg_Customer_Rating
                   from ola_dataset
                   Group by Vehicle_Type
                   Order by Avg_Customer_Rating desc
                """
        st.code(query, language = "sql")
        df = pd.read_sql(query, con = engine)
        st.write("#### Output")
        fig, ax = plt.subplots(figsize = (10,4))
        plt.bar(
                data = df,
                x = "Vehicle_Type",
                height = "Avg_Customer_Rating",
                color = "Black"
                )
        plt.title("Average Customers Rating per Vehicle")
        plt.xlabel("Vehicle Type")
        plt.ylabel("Ratings")
        st.dataframe(df)
        st.write(f"Row: {df.shape[0]}")
        st.write(f"Column: {df.shape[1]}")
        st.pyplot(fig)


# 9. Calculate the total booking value of rides completed successfully:
    with st.expander("9. Calculate the total booking value of rides completed successfully:"):

        st.write(""" 
                 **Description:** This query calculates the total booking value generated from successfully completed rides. 
                 It helps measure overall revenue and evaluate the financial performance of ride operations.
                """)

        query = """ 
                   select SUM(Booking_Value) as Total_Booking_Value
                   from ola_dataset
                   Where Booking_Status = "Success"
                """
        st.code(query, language = "sql")
        df = pd.read_sql(query, con = engine)
        st.write("#### Output")
        st.dataframe(df)
        st.write(f"Row: {df.shape[0]}")
        st.write(f"Column: {df.shape[1]}")


# 10. List all incomplete rides along with the reason
    with st.expander("10. List all incomplete rides along with the reason"):

        st.write("""
                 **Description:** This query retrieves all incomplete rides along with their respective reasons. 
                 It helps identify service issues, understand ride completion challenges, and analyze 
                 the factors contributing to incomplete trips.
                """)

        query = """ 
                    select Incomplete_Rides_Reason, count(*) as Total_Ride
                    from ola_dataset
                    where Incomplete_Rides = "Yes"
                    Group by Incomplete_Rides_Reason
                    Order by Total_Ride
                """
        st.code(query, language = "sql")
        df = pd.read_sql(query, con = engine)
        st.write("#### Output")
        fig, ax = plt.subplots(figsize = (10,4))
        plt.bar(data = df,
                x = "Incomplete_Rides_Reason",
                height = "Total_Ride",
                 color = "Red",
                 width = 0.4 
                 )
        plt.xlabel("Number of Rides")
        plt.ylabel("Reason")
        plt.title("Incomplete Rides by Reason")
        st.dataframe(df)
        st.write(f"Row: {df.shape[0]}")
        st.write(f"Column: {df.shape[1]}")
        st.pyplot(fig)
