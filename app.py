import streamlit as st
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
import io

container_style = """
    <style>
        .st-key-container {
            background-color: #FFFFFF;
            padding: 20px;
            border: 3px solid #000000; /* Adjust the border color as needed */
            border-radius: 10px; /* Optional: for rounded corners */
            margin-bottom: 20px; /* Space below the container */
        }
    </style>
"""
st.markdown(container_style, unsafe_allow_html=True)


with st.container(border=False,key="container"):
    # Streamlit UI
    #st.title("EDGAR Tool Search")
    st.html("<p style='font-size: 32px; text-align: center; font-weight: bold;'>🔍 SEC Filings Text Analytics 📈</p>")
    st.html("<p style='font-size: 20px; text-align: keft;'>Search millions of SEC filings for keywords and generate graphs to visualize trends, all in one simple tool.</p>")
    # User inputs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        query = st.text_input("Enter search query:", "Tsunami Hazards")
    with col2: 
        st.text("Start date:")
        start_date = st.text_input("Start date:", "2021-01-01",label_visibility = "collapsed")
    with col3:
        end_date = st.text_input("End date:", "2021-12-31")
    with col4:
        st.text(" ")
        st.text(" ")
        st.text(" ")
        search = st.button("Search",key="search",type="primary",use_container_width=True)

    # Output file
    output_file = "results.csv"
    #col4, col5, col6 = st.columns(3)

    
        # Run the command when the button is clicked
    if search:
        command = [
            "edgar-tool", "text_search", query,
            "--start_date", start_date, "--end_date", end_date,
            "--output", output_file
        ]
        
        with st.spinner("Searching millions of filings..."):
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                st.success("Command executed successfully!")

                # Load output file
                try:
                    df = pd.read_csv(output_file)

                    # Ensure the 'filing_date' column is in datetime format
                    df["filing_year"] = df["filing_date"].str[:4]

                    # Extract year and count filings per year
                    filings_per_year = df["filing_date"].value_counts().sort_index()

                    # Plot bar chart
                    fig, ax = plt.subplots()
                    filings_per_year.plot(kind="bar", ax=ax, color="royalblue")
                    ax.set_xlabel("Year")
                    ax.set_ylabel("Count of Filings")
                    ax.set_title("Filings by Year")
                    st.pyplot(fig)

                    # Download button for CSV
                    csv_buffer = io.BytesIO()
                    df.to_csv(csv_buffer, index=False)
                    csv_buffer.seek(0)
                    st.download_button(
                        label="Download Results CSV",
                        data=csv_buffer,
                        file_name=output_file,
                        mime="text/csv"
                    )

                except Exception as e:
                    st.error(f"Failed to process output file: {e}")

            else:
                st.error(f"Error executing command: {result.stderr}")

