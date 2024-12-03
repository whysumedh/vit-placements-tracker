import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from streamlit_cookies_manager import EncryptedCookieManager
import firebase_admin
from firebase_admin import credentials, firestore
import subprocess
import datetime
import os
import json



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
    commit_date = datetime.datetime.strptime(commit_date_str, "%a %b %d %H:%M:%S %Y %z")
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

st.set_page_config(page_title="VIT Placements" ,layout="wide")

st.title("VIT Placements 2024-2025")

with st.expander("Disclaimer", expanded=True):
    st.markdown("""
    **Please Note That:**  
    - The data is scraped from placements mail from July-18-2024.
    - Statistics may not be accurate or up-to-date or even wrong.
    - **The CTC information is not available for most of the Summer PPOs and Internship Offers.**
    - **Some of The CTC Information(If not known) is taken from Internet Public Posts for some Companies**
    - **The average and median CTC stats have been considered from available CTC information only.**
    - Only 21 Batch B.Tech details have been considered.
    - **Stats include all 4 campuses; some companies might vary.**
    - Gender Classification is done by Student's name. Used [naampy library](https://pypi.org/project/naampy/) for classification; Note that the classifications may not be accurate.
    """)

st.write(f"Data Updated as on **{formatted_date}**")
st.write(f"**Note:** TCS Digital/Prime have been seperated and WITCH/Regular Offers will be updated soon.")

cookies = EncryptedCookieManager(
    prefix="poll_",  
    password="your_secret_password"  
)

if not cookies.ready():
    st.stop()


if not firebase_admin._apps:
    cred = credentials.Certificate("fbcredss.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def fetch_poll_data():
    poll_ref = db.collection("poll").document("poll_data")
    doc = poll_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        initial_data = {"integrate": 109, "separate": 133}
        poll_ref.set(initial_data)
        return initial_data

def update_poll_data(option):
    poll_ref = db.collection("poll").document("poll_data")
    poll_data = fetch_poll_data()
    poll_data[option] += 1
    poll_ref.set(poll_data)

poll_data = fetch_poll_data()
total_votes = poll_data["integrate"] + poll_data["separate"]

def calculate_percentage(votes, total):
    return int((votes / total) * 100) if total > 0 else 0

has_voted = cookies.get("voted", "false") == "true"

# st.write("**How Should The Upcoming WITCH(TCS(Only Ninja), Cognizant, etc)(<5LPA) Offers be Updated?**")

# col1, col2 = st.columns(2)

# with col1:
#     if not has_voted:
#         if st.button(f"Integrate into the whole current data ({poll_data['integrate']})"):
#             update_poll_data("integrate")
#             cookies["voted"] = "true"
#             cookies.save()
#             st.rerun()
#     else:
#         st.write(f"Integrate into the whole current data ({poll_data['integrate']})")
#     st.progress(calculate_percentage(poll_data["integrate"], total_votes))

# with col2:
#     if not has_voted:
#         if st.button(f"Create a separate section for WITCH Offers ({poll_data['separate']})"):
#             update_poll_data("separate")
#             cookies["voted"] = "true"
#             cookies.save()
#             st.rerun()
#     else:
#         st.write(f"Create a separate section for WITCH Offers ({poll_data['separate']})")
#     st.progress(calculate_percentage(poll_data["separate"], total_votes))


# if not cookies.ready():
#     st.stop()

# poll_file = "poll_data.json"

# if not os.path.exists(poll_file):
#     poll_data = {"integrate": 0, "separate": 0}
#     with open(poll_file, "w") as file:
#         json.dump(poll_data, file)
# else:
#     with open(poll_file, "r") as file:
#         poll_data = json.load(file)

# total_votes = poll_data["integrate"] + poll_data["separate"]

# def calculate_percentage(votes, total):
#     return int((votes / total) * 100) if total > 0 else 0

# has_voted = cookies.get("voted", "false") == "true"

# st.write("**How Should The Upcoming WITCH(TCS(Only Ninja), Cognizant, etc)(<5LPA) Offers be Updated ?**")

# col1, col2 = st.columns(2)

# with col1:
#     if not has_voted:
#         if st.button(f"Integrate into the whole current data ({poll_data['integrate']})"):
#             poll_data["integrate"] += 1
#             with open(poll_file, "w") as file:
#                 json.dump(poll_data, file)
#             cookies["voted"] = "true"
#             cookies.save()
#             st.rerun()
#     else:
#         st.write(f"Integrate into the whole current data ({poll_data['integrate']})")
#     st.progress(calculate_percentage(poll_data["integrate"], total_votes))

# with col2:
#     if not has_voted:
#         if st.button(f"Create a separate section for WITCH Offers ({poll_data['separate']})"):
#             poll_data["separate"] += 1
#             with open(poll_file, "w") as file:
#                 json.dump(poll_data, file)
#             cookies["voted"] = "true"
#             cookies.save()
#             st.rerun()
#     else:
#         st.write(f"Create a separate section for WITCH Offers ({poll_data['separate']})")
#     st.progress(calculate_percentage(poll_data["separate"], total_votes))

tab1, tab2, tab3 = st.tabs(["Branch-wise Placements", "Company-wise Placements", "Overall Statistics"])

with tab1:
    branch_name_mapping = {
        'BCE': '(BCE) Computer Science & Engineering',
        'BAI': '(BAI) CSE with AIML',
        'BEC': '(BEC) Electronics(ECE)',
        'BRS': '(BRS) CSE with AI & Robotics',
        'BIT': '(BIT) Information Technology',
        'BCI': '(BCI) CSE with Info Security',
        'BPS': '(BPS) CSE with Cyber Physical Systems',
        'BDS': '(BDS) CSE with Data Science',
        'BCT': '(BCT) CSE with IOT',
        'BME': '(BME) Mechanical Engineering',
        'BBS': '(BBS) CSE with Business Systems',
        'BLC': '(BLC) Electronics and Computers',
        'BEE': '(BEE) Electrical Engineering',
        'BCY': '(BCY) CSE with Cyber Security',
        'BKT': '(BKT) CSE with Blockchain',
        'BCB': '(BCB) CSE with Bio',
        'BHI': '(BHI) CSE with Health Informatics',
        'BBT': '(BBT) Biotechnology'        
    }
    st.header("Branch-wise Placements")
    branch_count = df['Branch'].value_counts()
    branch_count.index = branch_count.index.to_series().replace(branch_name_mapping)
    fig = px.pie(values=branch_count, names=branch_count.index, title='Branch-wise Placement Distribution')
    st.plotly_chart(fig)
    dropdown_options = [
        branch_name_mapping.get(branch, branch) for branch in df['Branch'].unique()
    ]
    
    selected_branch_display = st.selectbox("Select Branch", options=dropdown_options)
    
    selected_branch = {v: k for k, v in branch_name_mapping.items()}.get(selected_branch_display, selected_branch_display)
    
    branch_data = df[df['Branch'] == selected_branch]
    
    avg_ctc = branch_data['CTC'].mean()
    max_ctc = branch_data['CTC'].max()
    min_ctc = branch_data['CTC'].min()
    median_ctc = branch_data['CTC'].median()
    num_selections = len(branch_data)

    
    st.write(f"**Statistics for {selected_branch_display}:**")
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

    st.write(f"**Companies and CTC offered under {selected_branch_display}:**")
    st.write("*Avg CTC is the average of various CTCs offered by the company(if offered various CTCs)*")

    company_stats = company_stats.rename(columns={'avg_ctc': 'Average CTC (LPA)'})
    company_stats = company_stats.rename(columns={'num_selections': 'Placed'})
    company_stats['Average CTC (LPA)'] = company_stats['Average CTC (LPA)'].astype(float)

    sort_options = {
    'Company Name': 'Company',
    'Number of Selections': 'Placed',
    'Average CTC': 'Average CTC (LPA)'
    }
    selected_sort_option = st.selectbox("Sort by", options=['Company Name', 'Number of Selections', 'Average CTC'],index=0)

    ascending_order = selected_sort_option == 'Company Name' 
    sorted_company_stats = company_stats.sort_values(by=sort_options[selected_sort_option], ascending=ascending_order)

    sorted_company_stats['Average CTC (LPA)'] = sorted_company_stats['Average CTC (LPA)'].map(lambda x: f"{x:.1f}")

    st.table(sorted_company_stats[['Company', 'Placed', 'Average CTC (LPA)']])



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
    
    male_count = (company_data['Gender'] == 'Male').sum()
    female_count = (company_data['Gender'] == 'Female').sum()
    if female_count > 0:
        gender_ratio = male_count / female_count
    else:
        gender_ratio = None

    company_ctc_dist = company_data['CTC'].value_counts()
    company_ctc_dist.index = [f"{ctc} LPA" for ctc in company_ctc_dist.index]

    branch_count_company = company_data['Branch'].value_counts()
    if company == 'Bank of America':
        st.write("**Note:** BOFA selected 147 (B.Tech) Students + 23 (M.Tech) Students (In the initial selection list)")
    if company == 'TCS Digital/Prime':
        st.write("**Note:** B.Tech Digital Selections: 406 and B.Tech Prime Selections : 44")
    
    
    st.write(f"**Total Selections in {company}: {num_selections_company}**")
    st.write(f"**Number of Male Selections: {male_count}**")
    st.write(f"**Number of Female Selections: {female_count}**")
    if gender_ratio is not None:
        st.write(f"**Gender Ratio (Male to Female): {gender_ratio:.2f}**")
    else:
        st.write("**Gender Ratio (Male to Female): N/A**")

    st.write(f"**Branches under {company}:**")
    st.table(branch_count_company)
    avg_ctc_company = company_data['CTC'].mean()
    st.write(f"**Average CTC in {company}: {avg_ctc_company:.2f} LPA**")

    fig = px.pie(values=company_ctc_dist, names=company_ctc_dist.index, title=f'{company} CTC Distribution')
    st.plotly_chart(fig)


# count_file = 'last_total_students_placed.json'
# total_students_placed = df['Reg_No'].count()
# if os.path.exists(count_file):
#     try:
#         with open(count_file, 'r') as f:
#             previous_data = json.load(f)
#             previous_count = previous_data.get('total_students_placed', 0)
#     except json.JSONDecodeError:
#         previous_count = 0
# increase = total_students_placed - previous_count


with tab3:
    st.header("Overall Placement Statistics")
    
    overall_avg_ctc = df['CTC'].mean()
    overall_max_ctc = df['CTC'].max()
    overall_min_ctc = df['CTC'].min()
    overall_median_ctc = df['CTC'].median()
    total_students_placed = df['Reg_No'].count()
    overall_male_count = (df['Gender'] == 'Male').sum()
    overall_female_count = (df['Gender'] == 'Female').sum()
    overall_gender_ratio = overall_male_count / overall_female_count 
    avg_male_ctc = df[df['Gender'] == 'Male']['CTC'].mean()
    avg_female_ctc = df[df['Gender'] == 'Female']['CTC'].mean()
    
    
    
    col1, col2 = st.columns([0.5, 1])

    with col1:
        st.write(f"**Total Students Placed:** {total_students_placed}")
        st.write(f"**Average CTC:** {overall_avg_ctc:.2f} LPA")
        st.write(f"**Maximum CTC:** {overall_max_ctc:.2f} LPA")
        st.write(f"**Minimum CTC:** {overall_min_ctc:.2f} LPA")
        st.write(f"**Median CTC:** {overall_median_ctc:.2f} LPA")
        
    
    with col2:
        st.write(f"**Overall Male Selections:** {overall_male_count}")
        st.write(f"**Overall Female Selections:** {overall_female_count}")
        st.write(f"**Overall Gender Ratio (Male to Female): {overall_gender_ratio:.2f}**")
        st.write(f"**Average Male CTC: {avg_male_ctc:.2f} LPA**" if overall_male_count > 0 else "**Average Male CTC: N/A**")
        st.write(f"**Average Female CTC: {avg_female_ctc:.2f} LPA**" if overall_female_count > 0 else "**Average Female CTC: N/A**")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("**Note that CTC information is not known for some companies (NA) so the below Bar Chart numbers might not add up to the total students placed**")
    ctc_ranges = ['<= 10 LPA', '10-15(Inclusive) LPA', '15-20(Inclusive)LPA', '> 20 LPA']
    ctc_counts = [
        df[df['CTC'] <= 10].shape[0],
        df[(df['CTC'] > 10) & (df['CTC'] <= 15)].shape[0],
        df[(df['CTC'] > 15) & (df['CTC'] <= 20)].shape[0],
        df[df['CTC'] > 20].shape[0]
    ]
    
    ctc_data = {
        'CTC Range': ctc_ranges,
        'Number of Students': ctc_counts
    }
    
    fig = px.bar(
        ctc_data, 
        x='CTC Range', 
        y='Number of Students', 
        text='Number of Students',  
        labels={'CTC Range': 'CTC Range (LPA)', 'Number of Students': 'Number of Students'},
        title="Number of Students Placed by CTC Range"
    )
    
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(height=400, showlegend=False)

    st.plotly_chart(fig)
    
    branchwise_count = df.groupby('Branch').size()
    st.write("**Students Placed by Branch:**")
    st.write(branchwise_count)
    
    total_companies = df['Company'].nunique()
    st.write(f"**Total Number of Companies:** {total_companies}")
    st.write("*Please Note That: Some companies came for both PPO and Placements*")
    st.write("*Avg CTC is the average of various CTCs offered by the company (if offered various CTCs)*")

    company_stats = df.groupby('Company').agg(
        num_selections=('Reg_No', 'size'),  
        avg_ctc=('CTC', 'mean')  
    ).reset_index()
    company_stats['avg_ctc'] = company_stats['avg_ctc'].astype(float)

    sort_options = {
    'Company': 'Company',
    'Selections': 'num_selections',
    'Average CTC': 'avg_ctc'
    }
    selected_sort_option = st.selectbox("Sort by", options=['Company', 'Selections', 'Average CTC'],index=0)

    ascending_order = selected_sort_option == 'Company'  
    sorted_company_stats = company_stats.sort_values(by=sort_options[selected_sort_option], ascending=ascending_order)

    sorted_company_stats['avg_ctc'] = sorted_company_stats['avg_ctc'].map(lambda x: f"{x:.1f}")
    sorted_company_stats = sorted_company_stats.rename(columns={'avg_ctc': 'Average CTC (LPA)'})
    sorted_company_stats = sorted_company_stats.rename(columns={'num_selections': 'Placed'})

    st.table(sorted_company_stats[['Company', 'Placed', 'Average CTC (LPA)']])




st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown("""
    <p style='text-align: center;'>
        For Feedback and Discrepancies: 
        <a href='https://forms.gle/ZVSaNbbFHRjwevEN6' target='_blank'>
            Google Form
        </a>
    </p>
    """, unsafe_allow_html=True)
# st.markdown("""
#     <p style='text-align: center;'>
#         Check out the Reddit post!!  
#         <a href='https://www.reddit.com/r/Vit/comments/1fqhlmp/placement_stats_up_until_now/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button' target='_blank'>
#             Reddit Post
#         </a>
#     </p>
#     """, unsafe_allow_html=True)
# st.markdown("""
#     <p style='text-align: center;'>
#         Made by  
#         <a href='https://www.linkedin.com/in/sumedh-sai-873824a6/'>
#             Sumedh K
#         </a>
#     </p>
#     """, unsafe_allow_html=True)


