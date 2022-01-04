import streamlit as st
import pandas as pd
import numpy as np


st.title('Attaching Geopoints to your route!')
st.write("It works only with Ada County. It will attach longitude and latitude as separate columns and create a new CSV file.")
st.write ("It doesn't work with Canyon county because the database with addresses attached on backend has only Ada county addresses. ")
st.header("Here are the simple rules to use this scritp:")
st.subheader("First, your csv file should have  these headers or lables in your route.csv file: ")
st.code("pieces	lbs	service	delname	delstreetno	delstreet	delsuite	delcity	delzip	delroute")
st.subheader("Second, make sure your delstreet column has only numbers or blanks. Make sure it doesn't have any letters or special characters")
df = pd.read_csv('dataframe2.csv')


def jtable(df0):
    try:
        df0['delstreetno'] = df0['delstreetno'].replace(np.nan, 0)
        df0['delstreetno'] = df0['delstreetno'].astype(int)

        df['AddNum'] = df['AddNum'].replace(np.nan, 0)
        df['AddNum'] = df['AddNum'].astype(int)

        df["jointadd"]=df["AddNum"].astype(str)+" "+df["StPreDir"]+" "+df["StName"]+" "+df["StSuffix"]
        df0["jointadd"]=df0["delstreetno"].astype(str)+" "+df0["delstreet"]


        result3= pd.merge(df0,df, on="jointadd",how='left')
        result4=result3.drop_duplicates(subset=["jointadd"])

        result5= result4.rename(columns = {'jointadd': 'Address Line 1',}, inplace = False)

        datapref=result5[['Address Line 1','delstreetno','delstreet','delzip','delsuite','longitude','latitude','pieces','lbs','service','delname','Name']]
        finresult = datapref.rename(columns = {'Name': 'delRoute', 'delstreetno':'houseNumber', }, inplace = False)
        return finresult
    except:
        return st.header('Not Working')


data_file = st.file_uploader("Upload CSV",type=["csv"])



if data_file is not None:
    try:
        df = jtable(pd.read_csv(data_file))
        st.dataframe(df)
    except:

        st.write("Just doesn't like you file could be column lables. delstreetno should have only numbers or empty cell.")
        st.write("Fix your file and rerun!")

@st.cache
def convert_df(datadownld):
    return df.to_csv().encode('utf-8')


csv = convert_df(df)

st.download_button(
     "Press to Download",csv,
     "your_route.csv",
     "text/csv",
     key='browser-data'
)

