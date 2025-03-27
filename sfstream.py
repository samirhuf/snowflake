import streamlit as st

import pandas as pd
import snowflake.connector
# Snowflake connection parameters
snowflake_account = "ZPMUOHI-UQB15985"  # e.g., xy12345.us-east-1
snowflake_user = "SAMIRBRD"
snowflake_password = "910BigFatHen88"
snowflake_warehouse = "COMPUTE_WH"  # e.g., COMPUTE_WH
snowflake_role = "ACCOUNTADMIN"  # e.g., ACCOUNTADMIN

# Database and table parameters
database_name = "INVENTORY"
schema_name = "PUBLIC"
table_name = "BATCHINVENTORY"
csv_file_path = "G:/My Drive/Portfolio/BatchInventoryLTP.csv"

# --- Snowflake Connection Details ---
SNOWFLAKE_ACCOUNT = "ZPMUOHI-UQB15985"  # Replace with your account identifier
SNOWFLAKE_USER = "SAMIRBRD"          # Replace with your Snowflake username
SNOWFLAKE_PASSWORD = "910BigFatHen88"      # Replace with your Snowflake password
SNOWFLAKE_DATABASE = "INVENTORY"   # Replace with your database name
SNOWFLAKE_SCHEMA = "PUBLIC"     # Replace with your schema name
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH" # Replace with your warehouse name
SNOWFLAKE_TABLE = "BATCHINVENTORY"       # Replace with the name of your table

@st.cache_data(ttl=3600)  # Cache data for 1 hour to reduce repeated queries
def load_data():
    """Establishes a connection to Snowflake and loads data into a Pandas DataFrame."""
    try:
        conn = snowflake.connector.connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
            warehouse=SNOWFLAKE_WAREHOUSE
        )
        cursor = conn.cursor()
        query = f"SELECT * FROM {SNOWFLAKE_TABLE}"  # Customize your query if needed
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(data, columns=columns)
        print(df.head())
        return df
    except snowflake.connector.Error as e:
        st.error(f"Error connecting to Snowflake: {e}")
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

# --- Streamlit App ---
st.title("Snowflake Data Dashboard")

data_df = load_data()

if data_df is not None:
    st.write("### Data from Snowflake")
    st.dataframe(data_df)

    # --- Optional: Add filters or visualizations ---
    # st.sidebar.header("Filters")
    # # Example: Add a column selector
    # selected_columns = st.sidebar.multiselect("Select Columns to Display", data_df.columns, default=data_df.columns[:5])
    # st.dataframe(data_df[selected_columns])

    # # Example: Add a simple chart
    # if len(data_df) > 0 and 'YOUR_NUMERIC_COLUMN' in data_df.columns and 'YOUR_CATEGORICAL_COLUMN' in data_df.columns:
    #     st.sidebar.header("Simple Chart")
    #     chart_type = st.sidebar.selectbox("Chart Type", ["bar", "line"])
    #     if chart_type == "bar":
    #         st.bar_chart(data_df.groupby('YOUR_CATEGORICAL_COLUMN')['YOUR_NUMERIC_COLUMN'].sum())
    #     elif chart_type == "line":
    #         st.line_chart(data_df.groupby('YOUR_CATEGORICAL_COLUMN')['YOUR_NUMERIC_COLUMN'].sum())
else:
    st.info("Failed to load data from Snowflake.")
