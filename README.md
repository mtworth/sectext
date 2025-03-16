# SEC Filings Text Analytics

This Streamlit app allows users to search millions of SEC 10-K filings for keywords and visualize trends. The app provides an easy-to-use interface for querying the EDGAR database and displaying the results in a bar chart. Users can also download the search results as a CSV file.

## How to Use

1. Enter the search query in the "Enter search query" input box. The search will find exact matches of the word or phrase you put in (case insensitive). 
2. Specify the start year and end year for the search.
3. Click the "Search Filings" button to start the search.
4. The app will display a bar chart showing the number of filings per year containing the specified keywords.
5. Use the "Download Results CSV" button to download the search results as a CSV file.
6. Use the "Download Chart as PNG" button to download the chart as a PNG image using the menu in the top righthand corner of the chart. 

## Source Library

This app uses the [EDGAR](https://github.com/bellingcat/EDGAR) library to query the SEC EDGAR database. If you want to support this project, please support the authors of the original package.

## Made with Streamlit

This app is made with Streamlit 🎈 by [@mtworth](https://github.com/mtworth). 
