# st2195_assignment_6

This repository contains the source scripts for processing European Central Bank (ECB) speeches alongside the daily EUR/USD reference exchange rate data. 

Following the assignment guidelines, the raw datasets are **not** committed to this repository. Instructions for recreating the environment and downloading the data are detailed below.

---

## Dataset Setup Instructions

To run the analysis scripts, you must download the source files from the **ECB Data Portal / Statistical Data Warehouse (SDW)** and format them exactly as follows:

1. **ECB Speeches Dataset**
   - **Source:** Download the official historical dataset of speeches given by ECB officials.
   - **Formatting:** Keep only the `date` and `contents` columns. 
   - **Filename:** Save this file strictly as `speeches.csv` in the root folder of this repository.

2. **EUR/USD Reference Exchange Rate**
   - **Source:** Download the daily EUR/USD reference exchange rate data series.
   - **Filename:** Save this file strictly as `fx.csv` in the root folder of this repository.

*Note: Ensure both CSV files are located in the same directory as the execution scripts before running them.*

---

## Repository Contents

* `assignment6.py`: The complete data processing pipeline written in Python.
* `assignment6.R`: The complete data processing pipeline written in R.
* `good_indicators.csv`: Saved output table containing the 20 most common words associated with positive exchange rate returns (>0.5%).
* `bad_indicators.csv`: Saved output table containing the 20 most common words associated with negative exchange rate returns (<-0.5%).

---

## Data Pipeline Steps Performed

Both the Python and R scripts execute identical logic sequentially:
1. **Load & Merge:** Merges the datasets on the `date` field, preserving all information matching the days available in `fx.csv`.
2. **Outlier Filtering:** Scrubs obvious mistakes or invalid/negative data rows.
3. **Missing Value Handling:** Forwards-fills missing exchange rate values using the latest available price point. Any entries that cannot be resolved are dropped.
4. **Return Calculation:** Calculates the daily percentage return of the exchange rate, generating dummy variables for `good_news` (return > 0.5%) and `bad_news` (return < -0.5%).
5. **Text Frequency Analysis:** Cleans the text by dropping `NA` text observations, filtering out standard english stop words (articles, prepositions, connectors), and outputting the top 20 terms for both market conditions to separate CSV files.

---

## Text Analysis Observations

When reviewing `good_indicators.csv` and `bad_indicators.csv`, there is a significant overlap in the top 20 most frequent words. 

Both lists are dominated by structural, institutional vocabulary standard to central banking (e.g., *inflation, policy, euro, stability, growth, price*). This reveals that basic word frequency analysis alone is usually insufficient to capture market sentiment or direction, as the underlying institutional context remains highly stable regardless of daily exchange rate volatility.
