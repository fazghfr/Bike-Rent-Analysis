import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from babel.numbers import format_currency

df_raw = pd.read_csv('data.csv')

def generate_seasonal_df(df_raw, index_season):
    season_data = df_raw[df_raw['season'] == index_season] # 3 adalah index untuk musim gugur
    season_data.loc[:, 'month'] = pd.to_datetime(season_data['dteday']).dt.month
    season_data.loc[:, 'week'] = pd.to_datetime(season_data['dteday']).dt.isocalendar().week
    return season_data

def generate_monthly_in_season_df(df_season):
    grouped_season_condition_month = df_season.groupby('month').agg({'cnt': 'sum', 'hum': 'median', 'atemp': 'median', 'windspeed': 'median'})
    return grouped_season_condition_month

def generate_weekly_in_season_df(df_season):
    grouped_season_condition_week = df_season.groupby('week').agg({'cnt': 'sum', 'hum': 'median', 'atemp': 'median', 'windspeed': 'median'})
    return grouped_season_condition_week

def generate_seasonal_comparison_cnt(df_raw):
    grouped_season = df_raw.groupby('season')['cnt'].sum()
    season_dict = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    grouped_season = grouped_season.rename(season_dict)
    grouped_season = grouped_season.sort_values(ascending=False)
    return grouped_season


st.header('Bike Renting Analysis 🔍')

st.subheader('Q1: Pada Musim apa Peminjaman Sepeda Terbanyak Terjadi? 🍂')
q1_answer = generate_seasonal_comparison_cnt(df_raw)

# plot q1_answer
fig, ax = plt.subplots(figsize=(16, 8))
q1_answer.plot(kind='bar', ax=ax, color=['red'] + ['blue'] * (len(q1_answer) - 1))  # Set the color of the first bar to red
ax.set_xlabel('Season')
ax.set_ylabel('Total Count')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)  # Set x tick labels to be horizontal
st.pyplot(fig)

st.subheader('Kesimpulan Q1')

col1, col2 = st.columns(2)
with col1:
    st.metric('Musim Terbanyak: ', q1_answer.index[0])

with col2:
    st.metric('Jumlah Total Peminjaman', q1_answer.values[0])

st.write('Maka dari itu, musim gugur adalah musim dengan peminjaman sepeda terbanyak dengan angka yang sudah disebutkan di atas.')

### Q2
st.subheader('Q2: Bagaimana kondisi cuaca saat peminjaman sepeda dilakukan terbanyak? 🤔')
seasonal_df = generate_seasonal_df(df_raw, 3)
monthly_in_fall = generate_monthly_in_season_df(seasonal_df)
weekly_in_fall = generate_weekly_in_season_df(seasonal_df)

st.write('''Kita akan melihat kondisi cuaca saat peminjaman sepeda terbanyak dilakukan pada musim gugur. Dimana kondisi cuaca akan di representasikan
         dengan 3 variabel yaitu humidity (kelembapan), atemp (suhu terasa), dan windspeed (kecepatan angin).''')

# get the median
seasonal_df_median = seasonal_df.groupby('season').agg({'cnt': 'sum', 'hum': 'median', 'atemp': 'median', 'windspeed': 'median'})
grouped_season_condition = seasonal_df_median.sort_values(by='cnt', ascending=False)
# bar plot with doubled bar side by side in x axis for cnt and hum,windspeed,atemp where hum windspeed and atemp is the secondary y, sort by highest cnt
fig1, ax = plt.subplots()
ax2 = ax.twinx()
grouped_season_condition.plot(kind='bar', y='cnt', ax=ax, color='blue', position=4, width=0.2)
grouped_season_condition.plot(kind='bar', y='hum', ax=ax2, color='red', position=1, width=0.2)
grouped_season_condition.plot(kind='bar', y='windspeed', ax=ax2, color='green', position=2, width=0.2)
grouped_season_condition.plot(kind='bar', y='atemp', ax=ax2, color='orange', position=3, width=0.2)
# set the width of the plot

ax.set_ylabel('cnt')
ax2.set_ylabel('hum, windspeed, atemp')
plt.title('Peminjaman Sepeda pada musim gugur')
st.pyplot(fig1)

st.write('''Karena data cuaca berganti ganti, berikut merupakan data Bulanan dan Mingguan pada musim tersebut''')

# weekly
# Sort the grouped_week DataFrame by highest cnt
weekly_in_fall_median = weekly_in_fall.sort_values(by='cnt', ascending=False)


# bar plot with doubled bar side by side in x axis for cnt and hum,windspeed,atemp where hum windspeed and atemp is the secondary y, sort by highest cnt
fig2, ax = plt.subplots()
ax2 = ax.twinx()
weekly_in_fall_median.plot(kind='bar', y='cnt', ax=ax, color='gray', position=4, width=0.2)
weekly_in_fall_median.plot(kind='bar', y='hum', ax=ax2, color='red', position=1, width=0.2)
weekly_in_fall_median.plot(kind='bar', y='windspeed', ax=ax2, color='green', position=2, width=0.2)
weekly_in_fall_median.plot(kind='bar', y='atemp', ax=ax2, color='orange', position=3, width=0.2)

# set the width of the plot
ax.set_ylabel('cnt')
ax2.set_ylabel('hum, windspeed, atemp')
plt.title('Peminjaman Sepeda pada musim gugur mingguan')

monthly_in_fall_median = monthly_in_fall.sort_values(by='cnt', ascending=False)


# bar plot with doubled bar side by side in x axis for cnt and hum,windspeed,atemp where hum windspeed and atemp is the secondary y, sort by highest cnt
fig3, ax = plt.subplots()
ax2 = ax.twinx()
monthly_in_fall_median.plot(kind='bar', y='cnt', ax=ax, color='blue', position=4, width=0.2)
monthly_in_fall_median.plot(kind='bar', y='hum', ax=ax2, color='red', position=1, width=0.2)
monthly_in_fall_median.plot(kind='bar', y='windspeed', ax=ax2, color='green', position=2, width=0.2)
monthly_in_fall_median.plot(kind='bar', y='atemp', ax=ax2, color='orange', position=3, width=0.2)

# set the width of the plot

ax.set_ylabel('cnt')
ax2.set_ylabel('hum, windspeed, atemp')
plt.title('Peminjaman Sepeda pada musim gugur bulanan')

col3, col4 = st.columns(2)

with col3:
    st.write('Data mingguan')
    st.pyplot(fig2)

with col4:
    st.write('Data bulanan')
    st.pyplot(fig3)

st.write('''Dari data di atas, sulit menyimpulkan bahwa ada hubungan kondisi cuaca dengan jumlah peminjaman sepeda, Maka akan dicari korelasi secara statisik''')

st.subheader('Mencari Korelasi')
st.write('Karena ini adalah data cuaca, maka data weekly akan dijadikan acuan untuk mencari korelasi')

correlation_week = weekly_in_fall_median[['cnt', 'hum', 'windspeed', 'atemp']].corr()
st.write(correlation_week)

st.write('''dimana kelembapan dan kecepatan angin berkorelasi secara negatif terhadap jumlah peminjaman, sementara atemp tidak memiliki korelasi karena mendekati nol. Dengan keterangan korelasi dari kelembapan dan kecepatan angin 
             cenderung lemah untuk kecepatan angin, sementara untuk kelembapan cenderung sedikit lebih kuat.''')

atemp_mean = seasonal_df['atemp'].mean()
actual_atemp = atemp_mean*50
hum_mean = seasonal_df['hum'].mean()
actual_hum = hum_mean*100
windspeed_mean = seasonal_df['windspeed'].mean()
actual_windspeed = windspeed_mean*67

st.subheader('Kesimpulan Q2')
st.text('Kondisi Cuaca pada Musim dengan Peminjaman Terbanyak')

col5, col6, col7 = st.columns(3)
with col5:
    st.metric('Rata-rata Atemp', format(actual_atemp, '.2f'))
with col6:
    st.metric('Rata-rata Humidity', format(actual_hum, '.2f'))
with col7:
    st.metric('Rata-Rata Windspeed', format(actual_windspeed, '.2f'))

st.write('Dengan keterangan kelembapan dan kecepatan angin berkorelasi dengan jumlah peminjaman, meskipun relatif lemah')