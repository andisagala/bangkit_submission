import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


st.header('Beijing Air Quality Dashboard :sparkles:')

st.subheader('Daily Air Quality')

weather_df = pd.read_csv('dashboard/main_data.csv')
weather_df['date'] = pd.to_datetime(weather_df[['year', 'month', 'day']])
datetime_columns = ["datetime"]
weather_df.sort_values(by="datetime", inplace=True)
weather_df.reset_index(inplace=True)

min_date = weather_df["date"].min()
max_date = weather_df["date"].max()
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    genre = st.radio(
    label="Pilih rentang waktu",
    options=('Tahun', 'Bulan', 'Hari',),
    horizontal=False
    )

if genre == 'Tahun':
    ruless = 'Y'
elif genre == 'Bulan':
    ruless = 'M'
elif genre == 'Hari':
    ruless = 'D'

def create_air_quality(df):
    air_quality_df = df.resample(rule=ruless, on='date').agg({
        "Overall_AQI": "mean",
    })

    return air_quality_df
def create_timeline(df):
    air_quality_df = df.resample(rule=ruless, on='date').agg({
        "date":"first"
    }


    )

    return air_quality_df

def create_overall(df):
    rfm_df = df.groupby(by="station", as_index=False).agg({
        "TEMP": "mean",
        "PRES": "mean"
    })

    return rfm_df


main_df = weather_df[(weather_df["date"] >= str(start_date)) & 
                (weather_df["date"] <= str(end_date))]

air_quality = create_air_quality(main_df)
datetime = create_timeline(main_df)
print(air_quality)
print(datetime)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    
    datetime["date"],
    air_quality["Overall_AQI"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_ylabel("Overall AQI",fontsize=20)
ax.set_xlabel("Date", fontsize=20)
ax.set_title("Air Quality Index in Beijing's District", loc="center", fontsize=40)
 
st.pyplot(fig)


st.subheader('Best and Worst Air Quality District')

sum_order_items_df = main_df.groupby("station").Overall_AQI.sum().sort_values(ascending=False).reset_index()
sum_order_items_df.head(15)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]


sns.barplot(x="Overall_AQI", y="station", data=sum_order_items_df.head(6), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Overall AQI", fontsize=30)
ax[0].set_title("Worst Air Quality District", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="Overall_AQI", y="station", data=sum_order_items_df.sort_values(by="Overall_AQI", ascending=True).head(6), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Overall AQI", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Best Air Quality District", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)


st.subheader('Overall Condition')


rfm_df=create_overall(main_df)

col1, col2 = st.columns(2)
 
with col1:
    avg_temp = round(rfm_df.TEMP.mean(), 1)
    st.metric("Average Temperature (°C)", value=avg_temp)
 
with col2:
    avg_pressure = round(rfm_df.PRES.mean(), 2)
    st.metric("Average Pressure", value=avg_pressure)

 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
 
sns.barplot(y="TEMP", x="station", data=rfm_df.sort_values(by="TEMP", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Station", fontsize=30)
ax[0].set_title("By Temperature (°C)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="PRES", x="station", data=rfm_df.sort_values(by="PRES", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Station", fontsize=30)
ax[1].set_title("By Pressure", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
 
 
st.pyplot(fig)
 
st.caption('Andi Sagala')

