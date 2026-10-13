import streamlit as st
import requests
import pandas as pd

st.title("جستجوی کسب‌وکارها")
city = st.text_input("نام شهر:")
keyword = st.text_input("نام صنف:")

if st.button("جستجو"):
    query = f"""
    [out:json][timeout:25];
    area["name"~"{city}",i]->.searchArea;
    (node["shop"~"{keyword}",i](area.searchArea);
     way["shop"~"{keyword}",i](area.searchArea);
     node["amenity"~"{keyword}",i](area.searchArea);
     way["amenity"~"{keyword}",i](area.searchArea););
    out center;
    """
    try:
        r = requests.get("https://overpass-api.de/api/interpreter", params={'data': query})
        data = r.json().get('elements', [])
        if not data:
            st.write("چیزی پیدا نشد. صنف دیگری را امتحان کنید (مثلاً: رستوران)")
        else:
            df = pd.DataFrame([e.get('tags', {}) for e in data])
            st.dataframe(df[['name', 'phone', 'addr:street']])
            st.download_button("دانلود", df.to_csv(), "file.csv")
    except:
        st.write("ارتباط با نقشه برقرار نشد. دوباره دکمه جستجو را بزنید.")
