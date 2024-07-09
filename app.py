import streamlit as st
import pandas as pd
import os
from gspread_pandas import Spread, Client
from google.oauth2 import service_account

# Set up Google Drive credentials and client
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope
)

client = Client(scope=scope, creds=credentials)

# Get the Google Sheets URL from secrets
gsheets_url = st.secrets["private_gsheets_url"]
sh = client.open_by_url(gsheets_url)
worksheet_list = sh.worksheets()


# Functions
@st.cache_data()
def worksheet_names():
    sheet_names = []
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)
    return sheet_names


def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df


def update_the_spreadsheet(spreadsheetname, dataframe):
    spread.df_to_sheet(dataframe, sheet=spreadsheetname, index=False)
    st.write(
        "Success! Your feedback has been uploaded to this GoogleSheet: ", spread.url
    )


# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = {
        "Context-rich QA": [],
        "Retrieval-augmented QA": [],
        "Context Ranking": [],
        "Retrieval-augmented Ranking": [],
    }

# Sidebar for navigation
st.sidebar.title("Navigation")
options = ["Home/Add Data", "View Data"]
choice = st.sidebar.radio("Go to", options)

# Home/Add Data page
if choice == "Home/Add Data":
    st.title("Data Collection for RankRAG")
    st.write(
        "Welcome to the data collection app for RankRAG training! We implement the data collection process in 'RankRAG: Unifying Context Ranking with Retrieval-Augmented Generation in LLMs': https://arxiv.org/html/2407.02485v1"
    )

    st.write(
        """
        Use this app to:
        - Input questions and answers
        - Upload relevant documents
        - Label context passages
        Navigate using the sidebar.
    """
    )
    # Display an image in the Home/Add Data page
    st.image(
        "assets/img/dataset_generations.png",
        caption="Dataset Types",
        use_column_width=True,
    )

    st.header("Add Data")

    task_type = st.selectbox(
        "Select Task Type",
        [
            "Context-rich QA",
            "Retrieval-augmented QA",
            "Context Ranking",
            "Retrieval-augmented Ranking",
        ],
    )

    with st.form("data_form"):
        question = st.text_input("Question")
        answer = st.text_input("Answer")

        if task_type in ["Retrieval-augmented QA", "Retrieval-augmented Ranking"]:
            context = [
                st.text_area(
                    f"Context Passage {i+1}",
                    help=f"Paste or type context passage {i+1} here.",
                )
                for i in range(5)
            ]
        else:
            context = st.text_area(
                "Context Passage", help="Paste or type context passage here."
            )

        submit = st.form_submit_button("Submit")

        if submit:
            if question and answer and context:
                st.session_state.data[task_type].append(
                    {
                        "question": question,
                        "answer": answer,
                        "context": context if isinstance(context, list) else [context],
                    }
                )
                st.success("Data added successfully!")
            else:
                st.error("Please fill in all fields.")

# View Data page
if choice == "View Data":
    st.title("View Data")

    for task_type, data in st.session_state.data.items():
        st.subheader(task_type)
        if data:
            df = pd.DataFrame(data)
            st.write(df)

            if st.button(f"Upload {task_type} to Google Sheet"):
                existing_df = load_the_spreadsheet(task_type)
                new_df = existing_df.append(df, ignore_index=True)
                update_the_spreadsheet(task_type, new_df)
        else:
            st.write("No data collected yet for this task type.")
