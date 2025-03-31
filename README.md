# Q4 Spending Forecast – Stepwise Modeling

This repository contains the output of our submission for the Q4 spending prediction task. All analysis and code execution results are documented in the following two HTML files:

- `Prelim.html`: Step 1 – Predicting Q2 (2025/4–6) spending using data from July 2024 to March 2025  
- `pred2.html`: Step 2 and 3 – Predicting Q3 (2025/7–9) and Q4 (2025/10–12) based on predicted Q2 and Q3 values  

## Contents

### 1. `Prelim.html`

- Data used:  
  Monthly data from **2024-07 to 2025-03**
- Purpose:  
  Predict total spending in **2025 Q2** per account
- Key processes:
  - Feature engineering using past spending behavior
  - Account-level aggregation
  - LightGBM training and prediction
  - Evaluation (metrics, error analysis, feature importance)

### 2. `pred2.html`

- Purpose:  
  Step 2: Predict **Q3** spending using predicted Q2  
  Step 3: Predict **Q4** spending using predicted Q2 and Q3
- Structure:
  - Input: predicted Q2 values + features  
  - Models: LightGBM  
  - Evaluation for each step  
  - Final Q4 spending estimates

## How to Reproduce

1. Prepare monthly-level data from **2024-07 to 2025-03**
2. Follow the same feature engineering steps as shown in `Prelim.html`
3. Train a LightGBM model to predict Q2 (Step 1)
4. Use the predicted Q2 values to generate inputs for Q3 prediction (Step 2)
5. Use both Q2 and Q3 predictions as input for Q4 prediction (Step 3)
6. See all steps and outputs in the HTML files

## Notes

- All predictions are made at the **account level**
- This report includes only the results; original code can be provided separately if needed

## Youtube link
https://youtu.be/O8qDMeFF7rU 
