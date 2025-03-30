# Illinoi-Datathon

This was RM. It's submission for the Datathon 2025.


# Preliminary Spending Forecast Report

This repository contains a preliminary report analyzing and forecasting Q4 (October–December 2025) account-level spending, based on data from July 2024 to March 2025. The analysis was conducted by Moe Toyoda on March 30, 2025.

## Objective

- Forecast account-level spending for 2025 Q4.
- Compare two approaches:
  - Step-wise prediction: Q2 → Q3 → Q4
  - Direct Q4 prediction using the most recent months
- Build a model that combines machine learning (LightGBM) with time-series features and account attributes.

## Methods

- Time range used: July 2024 – March 2025
- Forecast target: Spending in Q4 (Oct–Dec 2025)
- Step-wise prediction using:
  - Past 6 months’ features
  - Predicted Q2 results to forecast Q3
  - Predicted Q3 results to forecast Q4
- Feature engineering:
  - Rolling statistics (mean, max, etc.)
  - Seasonality and trends
  - Demographics and behavioral features

## Models

- Linear Regression (baseline)
- LightGBM (main model)
- Combination of time series and machine learning

## File List

- `Prelim.html` – Main HTML report
- `README.md` – This file
- (Optional) `final_data.csv` – Feature data used for modeling

## How to View

Open `Prelim.html` in your browser to view the full report.



# Q4 Spending Forecast – Stepwise Prediction (Step 2 & 3)

This report is a continuation of the preliminary analysis and focuses on Step 2 and Step 3 of the **step-wise Q4 (Oct–Dec 2025) spending prediction**.

## Purpose

To predict account-level spending in Q4 2025 by:

1. Predicting Q3 (Jul–Sep 2025) spending using Q2 (Apr–Jun 2025) predicted values  
2. Predicting Q4 using both predicted Q2 and Q3 values

## Methods

- Training data:
  - Step 2: July 2024 – March 2025 → target: Q3 (2025/07–09)
  - Step 3: Same period features + predicted Q2/Q3 → target: Q4 (2025/10–12)

- Features:
  - Aggregated monthly behavior (rolling stats, change rates, etc.)
  - Customer attributes
  - Predictions from previous steps

- Models:
  - LightGBM
  - Evaluation via cross-validation
  - Feature importance analysis included

## Key Findings

- Q3 prediction shows moderate accuracy when using predicted Q2 as input  
- Q4 prediction improves by stacking Q2 and Q3 predicted values  
- Certain customer segments (e.g., high-frequency spenders) had lower prediction errors

## Files

- `pred2.html` – Main report (view in browser)
- `README.md` – This file
- (Optional) CSVs or models used can be added if needed

## How to View

Simply open `pred2.html` in a browser to explore the full step-by-step results and visualizations.
