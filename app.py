import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

df=pd.read_excel('google_sheet_data.xlsx')
def convert_ctc_to_numeric(ctc):
    try:
        return float(ctc.replace('LPA', '').strip())
    except:
        return np.nan

df['CTC'] = df['CTC'].apply(convert_ctc_to_numeric)


with st.expander("Disclaimer", expanded=True):
    st.markdown("""
    **Please Note That:**  
    - The data is scraped from placements mails from July-18-2024.
    - It may not be accurate or up-to-date (Will try to update as new selections keep coming).
    - **The CTC information is not available for most of the Summer PPOs, and Internship Offers.**
    - Only 21 Batch B.Tech details have been considered.
    - Data Updated as on 27 September 2024.
    """)



tab1, tab2, tab3 = st.tabs(["Branch-wise Placements", "Company-wise Placements", "Overall Statistics"])

with tab1:
    st.header("Branch-wise Placements")
    
    branch_count = df['Branch'].value_counts()
    fig = px.pie(values=branch_count, names=branch_count.index, title='Branch-wise Placement Distribution')
    st.plotly_chart(fig)
    
    branch = st.selectbox("Select Branch", options=df['Branch'].unique())
    
    branch_data = df[df['Branch'] == branch]
    
    avg_ctc = branch_data['CTC'].mean()
    max_ctc = branch_data['CTC'].max()
    min_ctc = branch_data['CTC'].min()
    median_ctc = branch_data['CTC'].median()
    num_selections = len(branch_data)

    
    st.write(f"**Statistics for {branch}:**")
    st.write(f"Number of Selections: {num_selections}")
    st.write(f"Average CTC: {avg_ctc:.2f} LPA")
    st.write(f"Maximum CTC: {max_ctc:.2f} LPA")
    st.write(f"Minimum CTC: {min_ctc:.2f} LPA")
    st.write(f"Median CTC: {median_ctc:.2f} LPA")

    company_stats = branch_data.groupby('Company').agg(
        num_selections=('CTC', 'size'),  
        avg_ctc=('CTC', 'mean')  
    ).reset_index().sort_values(by='num_selections', ascending=False)

    st.write(f"**Companies and CTC offered under {branch}:**")
    st.write(company_stats)


with tab2:
    st.header("Company-wise Placements")

    company_count = df['Company'].value_counts()
    fig = px.pie(values=company_count, names=company_count.index, title='Company-wise Placement Distribution')
    st.plotly_chart(fig)

    company = st.selectbox("Select Company", options=df['Company'].unique())

    company_data = df[df['Company'] == company]

    num_selections_company = len(company_data)

    company_ctc_dist = company_data['CTC'].value_counts()
    company_ctc_dist.index = [f"{ctc} LPA" for ctc in company_ctc_dist.index]

    branch_count_company = company_data['Branch'].value_counts()
    st.write(f"**Branches under {company}:**")
    st.write(branch_count_company)

    avg_ctc_company = company_data['CTC'].mean()

    st.write(f"**Total Selections in {company}: {num_selections_company}**")
    st.write(f"**Average CTC in {company}: {avg_ctc_company:.2f} LPA**")

    fig = px.pie(values=company_ctc_dist, names=company_ctc_dist.index, title=f'{company} CTC Distribution')
    st.plotly_chart(fig)

with tab3:
    st.header("Overall Placement Statistics")
    overall_avg_ctc = df['CTC'].mean()
    overall_max_ctc = df['CTC'].max()
    overall_min_ctc = df['CTC'].min()
    overall_median_ctc = df['CTC'].median()
    
    st.write(f"Average CTC: {overall_avg_ctc:.2f} LPA")
    st.write(f"Maximum CTC: {overall_max_ctc:.2f} LPA")
    st.write(f"Minimum CTC: {overall_min_ctc:.2f} LPA")
    st.write(f"Median CTC: {overall_median_ctc:.2f} LPA")
    
    total_students_placed = df['Reg_No'].count()
    st.write(f"**Total Students Placed: {total_students_placed}**")
    
    branchwise_count = df.groupby('Branch').size()
    st.write("**Students Placed by Branch:**")
    st.write(branchwise_count)

st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Made by Sumedh K</p>", unsafe_allow_html=True)