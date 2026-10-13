import streamlit as st
import requests
import pandas as pd

st.title("جستجوی کسب‌وکارها (ایران)")

city = st.text_input("نام شهر (مثال: تهران):")
keyword = st.text_input("نام صنف (مثال: رستوران):")
limit = st.selectbox("تعداد نتایج:", [20, 50, 100, 500, "همه"])
phone_only = st.checkbox("فقط نتایجی که شماره تلفن دارند")

if st.button("جستجو"):
    if not city or not keyword:
        st.error("لطفاً شهر و صنف را وارد کنید.")
    else:
        query = f"""
        [out:json][timeout:30];
        area["name"~"{city}",i]->.searchArea;
        (
          nwr["name"~"{keyword}",i](area.searchArea);
          nwr["amenity"~"{keyword}",i](area.searchArea);
          nwr["shop"~"{keyword}",i](area.searchArea);
        );
        out center;
        """
        
        try:
            response = requests.get("http://overpass-api.de/api/interpreter", params={'data': query})
            data = response.json().get('elements', [])
            
            results = []
            for item in data:
                tags = item.get('tags', {})
                name = tags.get('name', 'بدون نام')
                phone = tags.get('phone', tags.get('contact:phone', None))
                
                if phone_only and not phone:
                    continue
                
                results.append({
                    "نام": name,
                    "تلفن": phone if phone else "موجود نیست",
                    "آدرس": tags.get('addr:street', 'نامشخص')
                })
            
            df = pd.DataFrame(results)
            if not df.empty:
                if limit != "همه": df = df.head(int(limit))
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8-sig')
                st.download_button("دانلود اکسل", csv, "results.csv", "text/csv")
            else:
                st.warning("موردی پیدا نشد. عبارت ساده‌تری مثل 'پزشک' یا 'رستوران' را امتحان کنید.")
        except Exception as e:
            st.error(f"خطا در ارتباط با نقشه: {e}")
