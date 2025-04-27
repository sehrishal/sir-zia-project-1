
import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title= "Data Sweeper", layout='wide') # type: ignore

#custom css
st.markdown(
    """
    <style>
    .stApp{
       background-color:black;
       color: white;
       }
       </style>

       """,
       unsafe_allow_html=True
)

# tital and discription
st.title(" 📀Datasweeper Sterling Integrator By sehrish Muhammad Ali")
st.write("Transfrom your files between CSV and Excel formats with built-in data cleaning and visuelization creating the project for quarter3")

# file uploader
uploader_file = st.file_uploader(" ✅Upload your files (accepts CSV or Excel):", type=["cvs","xlsx"])

if uploader_file:
    for file in uploader_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f" unsupported file type: {file_ext}")
            continue

    # file details
    st.write(" 🔍Preview the head of the Dataframe")       
    st. dataframe(df.head())

     # file  data cleaning options 
    st.subheader(" 🛠 Data Cleaning Options")
    if st.checkbox(f"Clean data for{file.name}"):
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Remove duplicate from the file : {file.name}"):
                  df.drop_duplicates(inplace=True)
                  st.write(" ✅Duplicates removed!")
        
        with col2:
            if st.button(f"Fill missing Values for {file.name}"):
                 numeric_cols = df.select_dtypes(include=['number']).columns
                 df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                 st.write(" ✅Missing Values have been filled!")
        
        st.subheader(" 🪩Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for{file.name}", df.columns, default=df.columns)
        df = df[columns]

        #Data visualization
        st.subheader(" 📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # file Converstion options
        st.subheader(" 👁‍🗨Conversion options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["Csv", "Excel"], key=file.name)
        if st.button(f"convert{file.name}"):
            buffer = BytesIO()
            if conversion_type =="CVS":
                df.to.csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("All files processed successfully!")

                 
