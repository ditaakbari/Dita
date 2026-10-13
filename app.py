import streamlit as st
import requests
import pandas as pd

st.title("جستجوی کسب‌وکارهای ایران")

city = st.text_input("نام شهر را وارد کنید (مثل: تهران):")
category = st.text_input("صنف را وارد کنید (مثل: موبایل):")

if st.button("جستجو"):
    overpass_query = f"""
    [out:json];
    area[name="{city}"];
    node["shop"~"{category}"](area);
    out;
    """
    url = "https://overpass-api.de/api/interpreter"
    response = requests.get(url, params={'data': overpass_query})
    
    if response.status_code == 200:
        data = response.json().get('elements', [])
        if data:
            df = pd.DataFrame(data)
            st.write(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("دانلود اکسل", csv, "results.csv", "text/csv")
        else:
            st.warning("موردی یافت نشد.")
    else:
        st.error("خطا در اتصال. دوباره تلاش کنید.")
