import pandas as pd
import numpy as np
from pathlib import Path

data_path = Path("/Users/komanoritsuju/Downloads/tmp/datathon/data")

# Load data
account_dim = pd.read_csv(data_path / "account_dim_20250325.csv")
statement_fact = pd.read_csv(data_path / "statement_fact_20250325.csv")
transaction_fact = pd.read_csv(data_path / "transaction_fact_20250325.csv")
wrld_stor_tran_fact = pd.read_csv(data_path / "wrld_stor_tran_fact_20250325.csv")
rams_batch_cur = pd.read_csv(data_path / "rams_batch_cur_20250325.csv")
client_id = pd.read_csv(data_path / "syf_id_20250325.csv").iloc[:, [0, 1, 2]]
client_id.columns = ["client_id", "current_account_nbr", "confidence_lvl"]
fraud_claim_case = pd.read_csv(data_path / "fraud_claim_case_20250325.csv")
fraud_claim_tran = pd.read_csv(data_path / "fraud_claim_tran_20250325.csv")

# set up date variable 
transaction_fact["transaction_date"] = pd.to_datetime(transaction_fact["transaction_date"])
transaction_fact["posting_date"] = pd.to_datetime(transaction_fact["posting_date"])
wrld_stor_tran_fact["transaction_date"] = pd.to_datetime(wrld_stor_tran_fact["transaction_date"])
wrld_stor_tran_fact["posting_date"] = pd.to_datetime(wrld_stor_tran_fact["posting_date"])
account_dim["open_date"] = pd.to_datetime(account_dim["open_date"])

# empty/useless cols from transaction data
cols_to_remove = [
    'payment_type', 'product_amt', 'product_qty', 'us_equiv_amt',
    'fcr_amount', 'fcr_flag', 'fcr_rate_of_exchange', 'adj_orgn_tran_dt',
    'transaction_return_cnt', 'transaction_sale_cnt', 'curr_markup_fee',
    'invoice_nbr', 'first_purchase_ind'
]

### clean transaction_fact_20250325.csv ###
transaction_SALE = transaction_fact.drop(columns=cols_to_remove, errors='ignore')
transaction_SALE = transaction_SALE[transaction_SALE["transaction_type"] == "SALE"]
transaction_SALE["month"] = transaction_SALE["transaction_date"].dt.to_period("M").dt.to_timestamp()
transaction_SALE["quarter"] = transaction_SALE["transaction_date"].dt.to_period("Q").astype(str)
transaction_SALE["transaction_vs_world"] = 1

### clean wrld_stor_tran_fact_20250325.csv ###
wrld_stor_tran_SALE = wrld_stor_tran_fact.drop(columns=cols_to_remove, errors='ignore')
wrld_stor_tran_SALE = wrld_stor_tran_SALE[wrld_stor_tran_SALE["transaction_type"] == "SALE"]
wrld_stor_tran_SALE["month"] = wrld_stor_tran_SALE["transaction_date"].dt.to_period("M").dt.to_timestamp()
wrld_stor_tran_SALE["quarter"] = wrld_stor_tran_SALE["transaction_date"].dt.to_period("Q").astype(str)
wrld_stor_tran_SALE["transaction_vs_world"] = 0

### clean account_dim_20250325.csv ###
error_codes = [5, 13, 20, 22, 23, 28, 29, 35, 43, 45, 46, 48, 62, 80, 83, 96] # identify the error codes from external_status_reason_code
account_map = account_dim.copy()
account_map["external_risk_flag_ind"] = account_map["external_status_reason_code"].astype(float).isin(error_codes).astype(int)
account_map = account_map[[
    "current_account_nbr", "client_id", "open_date", "employee_code",
    "external_risk_flag_ind", "pscc_ind", "account_card_type"
]]

# rbind the transaction data
transactions_all = pd.concat([transaction_SALE, wrld_stor_tran_SALE], ignore_index=True)
transactions_all = transactions_all.merge(account_map, on="current_account_nbr", how="left")
transactions_all = transactions_all[
    (transactions_all["month"] >= "2024-04-01") & (transactions_all["month"] <= "2025-03-01")
]

# create new factors 
today = pd.to_datetime("2025-03-29")
transactions_all["open_date"] = pd.to_datetime(transactions_all["open_date"], utc=True).dt.tz_localize(None)
transactions_all["account_age_months"] = ((today - transactions_all["open_date"]) / np.timedelta64(1, 'M')).astype(int)
transactions_all["is_high_spender_flag"] = ((transactions_all["employee_code"] == "H") & (~transactions_all["employee_code"].isna())).astype(int)
transactions_all["card_type_dual_ind"] = (transactions_all["account_card_type"] == "DUAL CARD").astype(int)
transactions_all["days_until_posted"] = (transactions_all["posting_date"] - transactions_all["transaction_date"]).dt.days

# aggregate to monthly spending per account
monthly_spending_summary = transactions_all.groupby([
    "client_id", "current_account_nbr", "open_date", "account_age_months", "month"
]).agg(
    total_txns_count=("transaction_amt", "count"),
    total_spending=("transaction_amt", "sum"),
    avg_days_until_posted=("days_until_posted", "mean"),
    sale_reversal_count=("transaction_code", lambda x: (x == 256).sum()),
    count_PLCC_txns=("transaction_vs_world", lambda x: (x == 1).sum()),
    count_DUAL_txns=("transaction_vs_world", lambda x: (x == 0).sum()),
    high_spender_count=("is_high_spender_flag", "sum"),
    has_dual_card=("card_type_dual_ind", "max")
).reset_index()

### clean statement_fact_20250325.csv ###
statement_fact["billing_cycle_date"] = pd.to_datetime(statement_fact["billing_cycle_date"])
statement_fact["month"] = statement_fact["billing_cycle_date"].dt.to_period("M").dt.to_timestamp()

statement_summary = statement_fact.sort_values("billing_cycle_date").groupby([
    "current_account_nbr", "month"
]).agg(
    last_statement_date=("billing_cycle_date", "max"),
    last_prev_balance=("prev_balance", "last"),
    num_statements=("billing_cycle_date", "count")
).reset_index()

### clean rams_batch_cur_20250325.csv ###
rams_batch_cur["cu_processing_date"] = pd.to_datetime(rams_batch_cur["cu_processing_date"])
rams_batch_cur["month"] = rams_batch_cur["cu_processing_date"].dt.to_period("M").dt.to_timestamp()
rams_batch_cur["current_account_nbr"] = rams_batch_cur["cu_account_nbr"]

cols_to_drop = [
    "cu_account_nbr", "ca_cash_bal_pct_crd_line", "ca_cash_bal_pct_cash_line",
    "ca_avg_utilz_lst_6_mnths", "ca_max_dlq_lst_6_mnths", "ca_mnths_since_active",
    "cu_rnd_nbr", "rb_crd_gr_new_crd_gr", "mo_tot_sales_array_1", "mo_tot_sales_array_2",
    "mo_tot_sales_array_3", "mo_tot_sales_array_4", "mo_tot_sales_array_5",
    "mo_tot_sales_array_6", "ca_avg_utilz_lst_3_mnths"
]

accountlvl_feature = rams_batch_cur.drop(columns=cols_to_drop, errors="ignore")
accountlvl_feature = accountlvl_feature.sort_values("cu_processing_date").groupby([
    "current_account_nbr", "month"
]).tail(1).reset_index(drop=True)

# get number of accounts
client_id["num_accounts"] = client_id.groupby("client_id")["current_account_nbr"].transform("nunique")

# combine all
final_data = monthly_spending_summary.merge(statement_summary, on=["current_account_nbr", "month"], how="left")
final_data = final_data.merge(accountlvl_feature, on=["current_account_nbr", "month"], how="left")
final_data = final_data[final_data["account_age_months"] >= 8]

# save
output_dir = Path("/Users/komanoritsuju/Downloads/tmp/datathon/Data2")
output_dir.mkdir(parents=True, exist_ok=True)
final_data.to_csv(output_dir / "final_data.csv", index=False)
print("✅ 全処理完了！final_data.csv を保存しました。")
