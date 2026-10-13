import streamlit as st
import requests
import pandas as pd

st.title("جستجوی کسب‌وکارها (ایران)")

city = st.text_input("نام شهر:", "تهران")
guild = st.text_input("نام صنف یا نوع کسب‌وکار:", "رستوران")
count_limit = st.selectbox("تعداد نتایج:", [20, 50, 100, 500, "همه"])
filter_phone = st.checkbox("فقط نتایجی که شماره تلفن دارند")

if st.button("جستجو"):
    with st.spinner("در حال جستجو..."):
        overpass_query = f"""
        [out:json][timeout:25];
        area[name="{city}"];
        (
          node["shop"~"{guild}"](area);
          node["amenity"~"{guild}"](area);
          way["shop"~"{guild}"](area);
          way["amenity"~"{guild}"](area);
        );
        out center;
        """
        response = requests.get("https://overpass-api.de/api/interpreter", params={'data': overpass_query})
        
        if response.status_code == 200:
            data = response.json().get('elements', [])
            if not data:
                st.warning("نتیجه‌ای یافت نشد.")
            else:
                results = []
                for item in data:
                    tags = item.get('tags', {})
                    if filter_phone and 'phone' not in tags:
                        continue
                    results.append({
                        "نام": tags.get('name', 'بدون نام'),
                        "تلفن": tags.get('phone', 'ناموجود'),
                        "آدرس": tags.get('addr:street', 'ناموجود')
                    })
                
                df = pd.DataFrame(results)
                if count_limit != "همه":
                    df = df.head(int(count_limit))
                
                st.dataframe(df)
                st.download_button("دانلود اکسل", df.to_csv(index=False), "results.csv", "text/csv")
        else:
            st.error("خطا در اتصال به سرور.")
