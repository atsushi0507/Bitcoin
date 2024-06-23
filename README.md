# Bitcoin Price Data Collection and Visualization App

This web application collects and visualizes Bitcoin price data. It fetches 1-minute candlestick data from the CryptoCompare API, stores the data in Google BigQuery, and displays interactive trend graphs using Plotly on a Streamlit frontend.

## System Overview

### Bitcoin Price Information
- **Data Source**: CryptoCompare API
- **Data Type**: 1-minute candlestick data
- **Data Fields**: Timestamp, High, Low, Open, Close, Volume

### Data Storage
- **Database**: Google BigQuery
- **Stored Data Fields**: Timestamp, High, Low, Open, Close, Volume
- **Data Addition Condition**: Only add new data if there is no existing record with the same timestamp
- **Processing**: Query issued to handle data during retrieval

### Web Application
- **Frontend Technology**: Streamlit
- **Features**:
  - Button to fetch and store price data
  - Retrieve price data from BigQuery
  - Display trend information with interactive graphs created using Plotly

## System Architecture


# How to Run the Application
1. Clone the Repository:
```sh
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

2. Install Packages:
```sh
pip install -r requirements.txt
```

3. Setup Environment Variables
You need to create a "CryptoCompare" account and "Google Cloud Platform" account, and obtain the service account in order to execute at the deploy environment.  
You can find the detail [here](https://cloud.google.com/apigee/docs/hybrid/v1.8/precog-gcpaccount?hl=ja "GCP Official")

4. Run the Streamlit Application:
```sh
streamlit run app.py
```

# LICENSE
This project is licensed under the MIT License. See the **LICENSE** file for details.

# Contributing
1. Fork the repository
2. Create a new branch (git checkout -b feature/your-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin feature/your-feature)
5. Create a new Pull Request

# Acknowledgements
[CryptoCompare](https://www.cryptocompare.com) for the Bitcoin price data API  
[Google BigQuery](https://cloud.google.com/free/?hnv=true&e=0&utm_source=google&utm_medium=cpc&utm_campaign=japac-JP-all-ja-dr-BKWS-all-core-trial-EXA-dr-1605216&utm_content=text-ad-none-none-DEV_c-CRE_602341359562-ADGP_Hybrid+%7C+BKWS+-+EXA+%7C+Txt+-GCP-General-core+brand-main-KWID_43700080198428345-aud-970366092687:kwd-87853815&userloc_1009314-network_g&utm_term=KW_gcp&gad_source=1&gclid=CjwKCAjw7NmzBhBLEiwAxrHQ-cP9g5tYuXpWRrj89OE0MxUd2E6xehjgsErT7zVz5J60YytDH678MhoCGnEQAvD_BwE&gclsrc=aw.ds&hl=ja) for the data storage solution   
[Streamlit](https://cloud.google.com/s/results?q&_gl=1*183jm2h*_up*MQ..&gclid=CjwKCAjw7NmzBhBLEiwAxrHQ-cP9g5tYuXpWRrj89OE0MxUd2E6xehjgsErT7zVz5J60YytDH678MhoCGnEQAvD_BwE&gclsrc=aw.ds) for the frontend framework  
[Plotly](https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Heatmap.html) for the interactive graphs  
