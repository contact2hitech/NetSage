import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config("Internet Usage Viewer", layout="wide")
st.title("📡 Internet Usage Dashboard")

# Unit conversion helper
def convert_units(series, unit):
    factors = {
        "MB": 1,
        "GB": 1 / 1024,
        "TB": 1 / (1024 ** 2),
    }
    return series * factors[unit]

# Upload CSV
default_file_path = "usage/you_usage.csv"
uploaded_file = None

# Check if default file exists
if os.path.exists(default_file_path):
    st.success(f"✅ Loaded default file: {default_file_path}")
    uploaded_file = default_file_path
else:
    uploaded_file = st.file_uploader("📁 Upload Internet Usage CSV", type="csv")

if uploaded_file is not None:
    if isinstance(uploaded_file, str):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)


    df.columns = [col.strip() for col in df.columns]

    # Parse and clean
    df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
    df = df.dropna(subset=['Start Date', 'MB Consumption'])
    df['MB Consumption'] = pd.to_numeric(df['MB Consumption'], errors='coerce').fillna(0)

    df['Year'] = df['Start Date'].dt.year
    df['Month'] = df['Start Date'].dt.month

    # Sidebar filters
    st.sidebar.header("🔎 Filter Options")
    years = sorted(df['Year'].dropna().unique())
    months = sorted(df['Month'].dropna().unique())

    selected_year = st.sidebar.selectbox("Year", years, index=len(years) - 1)
    selected_month = st.sidebar.selectbox(
        "Month", months, format_func=lambda x: pd.to_datetime(f'{x}', format='%m').strftime('%B'))

    unit = st.sidebar.selectbox("Units", ["MB", "GB", "TB"])

    # Filtered DataFrame
    filtered_df = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]

    # Group by date
    usage_by_date = (
        filtered_df.groupby(filtered_df['Start Date'].dt.date)['MB Consumption']
        .sum()
        .reset_index()
        .rename(columns={'Start Date': 'Date', 'MB Consumption': 'Total MB'})
    )
    usage_by_date['Usage'] = convert_units(usage_by_date['Total MB'], unit)

    # Monthly stats
    monthly_total = filtered_df['MB Consumption'].sum()
    monthly_avg_daily = monthly_total / usage_by_date.shape[0] if usage_by_date.shape[0] > 0 else 0
    monthly_total_unit = convert_units(pd.Series([monthly_total]), unit).iloc[0]
    monthly_avg_daily_unit = convert_units(pd.Series([monthly_avg_daily]), unit).iloc[0]

    # Yearly stats
    df['Usage'] = convert_units(df['MB Consumption'], unit)
    yearly_usage = df[df['Year'] == selected_year].groupby('Month')['Usage'].sum()
    yearly_total = yearly_usage.sum()
    monthly_average = yearly_usage.mean()

    # Display Stats
    st.subheader(f"📌 Summary Statistics ({unit})")
    col1, col2, col3 = st.columns(3)
    col1.metric("Monthly Total", f"{monthly_total_unit:.2f} {unit}")
    col2.metric("Avg Daily (in Month)", f"{monthly_avg_daily_unit:.2f} {unit}")
    col3.metric("Yearly Total", f"{yearly_total:.2f} {unit}")

    st.metric("Average Monthly Usage (in Year)", f"{monthly_average:.2f} {unit}")

    # Table
    st.subheader(f"📅 Daily Usage for {selected_year}-{selected_month:02d}")
    st.dataframe(
        usage_by_date[['Date', 'Usage']]
        .rename(columns={'Usage': f'Total {unit}'})
        .sort_values('Date'),
        use_container_width=True
    )

    # Chart
    st.subheader(f"📈 Usage Chart ({unit})")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(usage_by_date['Date'], usage_by_date['Usage'], color='cornflowerblue')
    ax.set_xlabel("Date")
    ax.set_ylabel(f"Usage ({unit})")
    ax.set_title("Daily Internet Usage")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

else:
    st.info("Upload a CSV file to begin. Format: `Ip-Mac, Start Date, Start Time, End Date, End Time, MB Consumption`")
