import streamlit as st
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
import io
import altair as alt
import uuid


container_style = """
    <style>
        .st-key-container {
            background-color: #FFFFFF;
            padding: 20px;
            border: 3px solid #000000; /* Adjust the border color as needed */
            border-radius: 10px; /* Optional: for rounded corners */
            margin-bottom: 20px; /* Space below the container */
        }

        .st-key-search {
            background-color: #000000; /* Yellow background */
            border: 3px solid #000000; /* Thick black border */
            color: #FFFFFF; /* Black text */
            font-size: 24px; /* Larger font size */
            padding: 10px 10px; /* Adjust padding as needed */
            border-radius: 10px; /* Optional: for rounded corners */
            font-weight: bold; /* Make text stand out */
            cursor: pointer; /* Indicate it's clickable */
        }

        .st-key-search:hover {
            background-color: #FFD700; /* Slightly darker yellow on hover */
        }

        .st-key-chart {
            background-color: #FFFFFF
            padding: 20px;
        }
        
        .st-key-download {
            background-color: #FFFFFF
            text-align: right;
            color: grey;
            border: None;

        }
    </style>
"""
st.markdown(container_style, unsafe_allow_html=True)


with st.container(border=False,key="container"):
    # Streamlit UI
    #st.title("EDGAR Tool Search")
    st.text(" ")
    st.html("<p style='font-size: 32px; text-align: center; font-weight: bold;'>🔍 SEC Filings Text Analytics 📈</p>")
    st.html("<p style='font-size: 20px; text-align: center;'>Search millions of SEC 10-K filings for keywords and visualize trends.</p>")
    # User inputs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        query = st.text_input("Enter search query:", "Tsunami Hazards")
    with col2: 
        start_year = st.text_input("Start Year:", "2021")
        start_date = start_year + "-01-01"
    with col3:
        end_year = st.text_input("End Year:", "2024")
        end_date = end_year + "-12-31"
    with col4:
        search = st.button("Search Filings",key="search",type="tertiary",use_container_width=True)

    
    
        # Run the command when the button is clicked
    if search:
        st.divider()
        unique_id = str(uuid.uuid4())
        output_file = f"results_{unique_id}.csv"
        command = [
            "edgar-tool", "text_search", f"'{query}'",
            "--start_date", start_date, "--end_date", end_date,
            "--output", output_file, "--single_forms", "['10-K']"
        ]
        #st.text(command)
        with st.spinner("Searching millions of filings, this might take awhile. If this is taking too long, make your search more specific 😊."):
            result = subprocess.run(command, capture_output=True, text=True)
            #st.text("Standard Output:")
            #st.text(result.stdout)
            #st.text("Standard Error:")
            #st.text(result.stderr)
            if result.returncode == 0:
                st.balloons()

                # Load output file
                try:
                    df = pd.read_csv(output_file)
                    #st.text(f"Number of filings found: {df.shape[0]}")
                    df["filing_year"] = df["filed_at"].str[:4]

                    # Extract year and count filings per year

                    filings_per_year = df["filing_year"].value_counts().sort_index().reset_index()
                    filings_per_year.columns = ["Year", "Count"]
                    with st.container():
                        altair_chart = alt.Chart(filings_per_year).mark_bar().encode(
                            x='Year:O',
                            y='Count:Q',
                            tooltip=['Year', 'Count']
                        ).properties(
                            title=f'SEC 10-K Filings by Year Containing "{query}"',
                        ).configure(background='#FFFFFF')

                        st.altair_chart(altair_chart, use_container_width=True, key="chart")

                    # Plot bar chart
                    #st.bar_chart(filings_per_year, use_container_width=True)

                    # Download button for CSV
                    csv_buffer = io.BytesIO()
                    df.to_csv(csv_buffer, index=False)
                    csv_buffer.seek(0)
                    col5, col6, col7 = st.columns(3)
                    with col7:
                        st.download_button(
                            label="Download Results CSV",
                            data=csv_buffer,
                            file_name=output_file,
                            mime="text/csv",
                            on_click="ignore",
                            type="tertiary",
                            icon=":material/download:",
                            key="download"
                            
                        )

                except Exception as e:
                    st.error(f"Failed to process output file: {e}")

            else:
                st.error(f"Error executing command: {result.stderr}")
    st.text(" ")
    st.html("<p style='text-align: center; color: grey;'>Made with Streamlit 🎈 by <a href='https://github.com/mtworth' style='color: grey;'>@mtworth</a></p>") 
