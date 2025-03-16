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
    st.html("<p style='font-size: 32px; text-align: center; font-weight: bold;'>SEC Filings Search Tool</p>")
    # User inputs
    col1, col2, col3 = st.columns(3)

    with col1:
        query = st.text_input("Enter search query:", "Tsunami Hazards")
    with col2: 
        start_date = st.text_input("Start date (YYYY-MM-DD):", "2021-01-01")
    with col3:
        end_date = st.text_input("End date (YYYY-MM-DD):", "2021-12-31")

    # Output file
    output_file = "results.csv"

    # Run the command when the button is clicked
    if st.button("Run EDGAR Tool"):
        command = [
            "edgar-tool", "text_search", query,
            "--start_date", start_date, "--end_date", end_date,
            "--output", output_file
        ]
        
        with st.spinner("Running EDGAR Tool..."):
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                st.success("Command executed successfully!")

                # Load output file
                try:
                    df = pd.read_csv(output_file)

                    # Ensure the 'filing_date' column is in datetime format
                    df["filing_date"] = pd.to_datetime(df["filing_date"])

                    # Extract year and count filings per year
                    filings_per_year = df["filing_date"].dt.year.value_counts().sort_index()

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

