import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import subprocess
from datetime import datetime

def get_commit_date(file_path):
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cd", "--", file_path],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

file_path = 'google_sheet_data.xlsx'

commit_date_str = get_commit_date(file_path)

if commit_date_str:
    commit_date = datetime.strptime(commit_date_str, "%a %b %d %H:%M:%S %Y %z")
    formatted_date = commit_date.strftime("%d %B %I:%M %p")
else:
    formatted_date = "No commits found."




df=pd.read_excel('google_sheet_data.xlsx')
def convert_ctc_to_numeric(ctc):
    try:
        return float(ctc.replace('LPA', '').strip())
    except:
        return np.nan

df['CTC'] = df['CTC'].apply(convert_ctc_to_numeric)

st.set_page_config(page_title="VIT Placement Tracker", page_icon="favicon-16x16.png")

st.title("VIT Placement Tracker")

with st.expander("Disclaimer", expanded=True):
    st.markdown("""
    **Please Note That:**  
    - The data is scraped from placements mail from July-18-2024.
    - It may not be accurate or up-to-date (Will try to update as new selections keep coming).
    - **The CTC information is not available for most of the Summer PPOs, and Internship Offers.
                (Please provide PPO CTC Info in the below gform if yk for the respective company)**
    - **The average,median CTC stats have been considered from available CTC information only.**
    - Only 21 Batch B.Tech details have been considered.
    """)

# st.write("Data Updated as on **07 October 2024 08:56PM**")
st.write(f"Data Updated as on **{formatted_date}**")

tab1, tab2, tab3 = st.tabs(["Branch-wise Placements", "Company-wise Placements", "Overall Statistics"])

with tab1:
    branch_name_mapping = {
        'BCE': '(BCE)Computer Science Core',
        'BAI': '(BAI)CS with AIML',
        'BEC': '(BEC)Electronics(ECE)',
        'BRS': '(BRS)CS with AI & Robotics',
        'BIT': '(BIT)Information Technology',
        'BCI': '(BCI)CS with Info Security',
        'BPS': '(BPS)CS with Cyber Physical Systems',
        'BDS': '(BDS)CS with Data Science',
        'BCT': '(BCT)CS with IOT',
        'BME': '(BME)Mechanical Engineering',
        'BBS': '(BBS)CS with Business Systems',
        'BLC': '(BLC)Electronics and Computers',
        'BEE': '(BEE)Electrical Engineering',
        'BCY': '(BCY)CS with Cyber Security',        
    }
    st.header("Branch-wise Placements")
    
    # branch_count = df['Branch'].value_counts()
    # fig = px.pie(values=branch_count, names=branch_count.index, title='Branch-wise Placement Distribution')
    # st.plotly_chart(fig)

    branch_count = df['Branch'].value_counts()
    
    # Replace branch names using the mapping dictionary
    branch_count.index = branch_count.index.to_series().replace(branch_name_mapping)
    
    # Create a pie chart
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
    st.write(f"**Number of Selections: {num_selections}**")
    st.write(f"Average CTC: {avg_ctc:.2f} LPA")
    st.write(f"Maximum CTC: {max_ctc:.2f} LPA")
    st.write(f"Minimum CTC: {min_ctc:.2f} LPA")
    st.write(f"Median CTC: {median_ctc:.2f} LPA")

    company_stats = branch_data.groupby('Company').agg(
        num_selections=('CTC', 'size'),  
        avg_ctc=('CTC', 'mean')  
    ).reset_index()
    company_stats['avg_ctc'] = company_stats['avg_ctc'].map(lambda x: f"{x:.1f}")

    st.write(f"**Companies and CTC offered under {branch}:**")
    st.write("*Avg CTC is the average of various CTCs offered by the company(if offered various CTCs)*")

    company_stats = company_stats.rename(columns={'avg_ctc': 'Average CTC (LPA)'})
    company_stats = company_stats.rename(columns={'num_selections': 'Placed'})
    st.table(company_stats[['Company', 'Placed', 'Average CTC (LPA)']]) 


# with tab2:
#     st.header("Company-wise Placements")

#     company_count = df['Company'].value_counts()
#     fig = px.pie(values=company_count, names=company_count.index, title='Company-wise Placement Distribution')
#     st.plotly_chart(fig)

#     company = st.selectbox("Select Company", options=df['Company'].unique())

#     company_data = df[df['Company'] == company]

#     num_selections_company = len(company_data)

#     company_ctc_dist = company_data['CTC'].value_counts()
#     company_ctc_dist.index = [f"{ctc} LPA" for ctc in company_ctc_dist.index]

#     branch_count_company = company_data['Branch'].value_counts()
#     st.write(f"**Branches under {company}:**")
#     st.write(branch_count_company)

#     avg_ctc_company = company_data['CTC'].mean()

#     st.write(f"**Total Selections in {company}: {num_selections_company}**")
#     st.write(f"**Average CTC in {company}: {avg_ctc_company:.2f} LPA**")

#     fig = px.pie(values=company_ctc_dist, names=company_ctc_dist.index, title=f'{company} CTC Distribution')
#     st.plotly_chart(fig)

with tab2:
    st.header("Company-wise Placements")

    company_count = df['Company'].value_counts()

    fig = px.bar(x=company_count.index, y=company_count.values, 
                 labels={'x': 'Company', 'y': 'Number of Selections'},
                 title='Company-wise Placement Distribution')
    st.plotly_chart(fig)

    company = st.selectbox("Select Company", options=df['Company'].unique())

    company_data = df[df['Company'] == company]

    num_selections_company = len(company_data)

    company_ctc_dist = company_data['CTC'].value_counts()
    company_ctc_dist.index = [f"{ctc} LPA" for ctc in company_ctc_dist.index]

    branch_count_company = company_data['Branch'].value_counts()
    st.write(f"**Branches under {company}:**")
    st.table(branch_count_company)
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
    
    st.write(f"**Average CTC:** {overall_avg_ctc:.2f} LPA")
    st.write(f"**Maximum CTC:** {overall_max_ctc:.2f} LPA")
    st.write(f"**Minimum CTC:** {overall_min_ctc:.2f} LPA")
    st.write(f"**Median CTC:** {overall_median_ctc:.2f} LPA")
    
    total_students_placed = df['Reg_No'].count()
    st.write(f"**Total Students Placed:** {total_students_placed}")

    st.write("**Note that CTC information is not known for some companies (NA) so the below Bar Chart numbers might not add up to the total students placed**")

    # CTC range counts
    ctc_ranges = ['<= 10 LPA','10-15 LPA','15-20 LPA','> 20 LPA']
    ctc_counts = [
        df[df['CTC'] <= 10].shape[0]  ,
        df[(df['CTC'] > 10) & (df['CTC'] <= 15)].shape[0],
        df[(df['CTC'] > 15) & (df['CTC'] <= 20)].shape[0], 
        df[df['CTC'] > 20].shape[0]        

    ]
    
    # Create a simple bar chart
    ctc_data = {
        'CTC Range': ctc_ranges,
        'Number of Students': ctc_counts
    }
    
    fig = px.bar(
        ctc_data, 
        x='CTC Range', 
        y='Number of Students', 
        text='Number of Students',  # Display the count directly on the bars
        labels={'CTC Range': 'CTC Range (LPA)', 'Number of Students': 'Number of Students'},
        title="Number of Students Placed by CTC Range"
    )
    
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(height=400, showlegend=False)

    st.plotly_chart(fig)
    
    branchwise_count = df.groupby('Branch').size()
    st.write("**Students Placed by Branch:**")
    st.write(branchwise_count)
    
    # total_companies = df['Company'].nunique()
    # st.write(f"**Total Number of Companies:** {total_companies}")
    # st.write("*Please Note That : Some companies came for both PPO and Placements*")
    
    # company_list = df['Company'].unique()
    # company_df = pd.DataFrame(company_list, columns=["Company Name"])  
    # st.write("**List of Companies:**")
    # st.table(company_df)

    total_companies = df['Company'].nunique()
    st.write(f"**Total Number of Companies:** {total_companies}")
    st.write("*Please Note That: Some companies came for both PPO and Placements*")
    st.write("*Avg CTC is the average of various CTCs offered by the company(if offered various CTCs)*")

    company_stats = df.groupby('Company').agg(
        num_selections=('Reg_No', 'size'),  
        avg_ctc=('CTC', 'mean')  
    ).reset_index()
    company_stats['avg_ctc'] = company_stats['avg_ctc'].map(lambda x: f"{x:.1f}")

    company_stats.rename(columns={'Company': 'Company Name', 'num_selections': 'Placed', 'avg_ctc': 'Avg CTC (LPA)'}, inplace=True)

    st.write("**List of Companies:**")
    st.table(company_stats)





# st.sidebar.write("Deloitte USI made 88 offers, 84(B.Tech)+4(M.Tech)")
# st.sidebar.write("IBM PPO Updated to 12LPA")
# st.sidebar.write("Sabre CTC Info Updated SA-16.84 and BA-16.29")
# st.sidebar.write(""" Thanks for the responses, the following CTC info is updated.""")
# st.sidebar.image("imageppo.png", caption="CTC Changes", use_column_width=True)
# st.sidebar.write("The CTC Average,Median might be skewed at the end, as we don't know how many will convert some internship offers at the end.")
# st.sidebar.write("I did update the CTC Info profile-wise if the company is offering various CTCs , you can check that in company-wise stats, company's CTC distribution.")

# st.sidebar.markdown("""
#     - Please lmk the branch names which are not mentioned in pie chart agenda
                     
# Thanks for the responses, the following **CTC info** is updated.  
# """)
# st.sidebar.image("imageppo.png", caption="CTC Changes", use_column_width=True)


# st.sidebar.markdown("""
# The **CTC Average** and **Median** might be skewed at the end, as we don't know how many internship offers will convert.

# I did update the CTC info profile-wise. If the company is offering various CTCs, you can check that in the company-wise stats for the company's **CTC distribution**.
# """)

# Add the image in between the text

st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown("""
    <p style='text-align: center;'>
        For Feedback and Discrepancies: 
        <a href='https://forms.gle/ZVSaNbbFHRjwevEN6' target='_blank'>
            Google Form
        </a>
    </p>
    """, unsafe_allow_html=True)
st.markdown("""
    <p style='text-align: center;'>
        Check out the Reddit post!!  
        <a href='https://www.reddit.com/r/Vit/comments/1fqhlmp/placement_stats_up_until_now/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button' target='_blank'>
            Reddit Post
        </a>
    </p>
    """, unsafe_allow_html=True)
# st.markdown("""
#     <p style='text-align: center;'>
#         Made by  
#         <a href='https://www.linkedin.com/in/sumedh-sai-873824a6/'>
#             Sumedh K
#         </a>
#     </p>
#     """, unsafe_allow_html=True)