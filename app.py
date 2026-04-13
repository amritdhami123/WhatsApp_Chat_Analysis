import streamlit as st
import preprocessor
import streamlit as st

st.set_page_config(layout="wide")
st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:  # Corrected this line to check when a file IS uploaded
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    # st.write(df.columns) <-- REMOVED this line to hide the extra column list
    st.dataframe(df)

    users_list = df['user'].unique().tolist()
    users_list.insert(0, 'Overall')  # This already keeps "Overall" at the beginning perfectly!

    selected_user = st.sidebar.selectbox("Show analysis for", options=users_list)

    col1, col2, col3, col4 = st.columns(4)

    # Calculate your actual total messages
    total_messages = df.shape[0]
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("<h3 style='white-space: nowrap;'>Total Messages:</h3>", unsafe_allow_html=True)
        # Put your calculated variable here instead of a random number
        st.title(total_messages)



