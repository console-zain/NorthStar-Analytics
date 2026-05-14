import pandas as pd

# Load data
customers = pd.read_csv('customers.csv')
orders = pd.read_csv('orders.csv')
deliveries = pd.read_csv('deliveries.csv')
complaints = pd.read_csv('complaints.csv')
incidents = pd.read_csv('incidents.csv')


# -----------------------------
# SAFE MISSING VALUE HANDLING
# -----------------------------
def fill_missing(df):
    for col in df.columns:

        # numeric columns → median
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())

        # datetime columns → leave as NaT (don’t fake values)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            pass

        # everything else → string fill
        else:
            df[col] = df[col].fillna("Unknown")

    return df


# -----------------------------
# APPLY CLEANING
# -----------------------------
customers = fill_missing(customers)
orders = fill_missing(orders)
deliveries = fill_missing(deliveries)


# -----------------------------
# DATE CONVERSION (IMPORTANT)
# -----------------------------
orders['order_created_at'] = pd.to_datetime(orders['order_created_at'], errors='coerce')
deliveries['dispatch_time'] = pd.to_datetime(deliveries['dispatch_time'], errors='coerce')
deliveries['delivery_completed_at'] = pd.to_datetime(
    deliveries['delivery_completed_at'],
    errors='coerce'
)


# -----------------------------
# DELIVERY TIME FEATURE
# -----------------------------
deliveries['delivery_time_hours'] = (
    deliveries['delivery_completed_at'] - deliveries['dispatch_time']
).dt.total_seconds() / 3600

# fix invalid / missing values
deliveries['delivery_time_hours'] = (
    deliveries['delivery_time_hours']
    .fillna(0)
    .clip(lower=0)
)


# -----------------------------
# MERGE ORDERS
# -----------------------------
merged = deliveries.merge(
    orders[['order_id', 'customer_id', 'promised_window_hours', 'pickup_zone', 'dropoff_zone']],
    on='order_id',
    how='left'
)


# -----------------------------
# DELAY FLAG
# -----------------------------
merged['delay_flag'] = (
    merged['delivery_time_hours'] > merged['promised_window_hours']
).fillna(False)


# -----------------------------
# COMPLAINT FLAG
# -----------------------------
complaints_flag = complaints[['order_id']].drop_duplicates()
complaints_flag['has_complaint'] = 1

merged = merged.merge(complaints_flag, on='order_id', how='left')
merged['has_complaint'] = merged['has_complaint'].fillna(0)


# -----------------------------
# INCIDENT FLAG
# -----------------------------
incident_flag = incidents[['delivery_id']].drop_duplicates()
incident_flag['has_incident'] = 1

merged = merged.merge(incident_flag, on='delivery_id', how='left')
merged['has_incident'] = merged['has_incident'].fillna(0)


# -----------------------------
# FINAL CLEANING
# -----------------------------
merged['delivery_time_hours'] = merged['delivery_time_hours'].round(2)

merged['pickup_zone'] = merged['pickup_zone'].astype(str).str.title()
merged['dropoff_zone'] = merged['dropoff_zone'].astype(str).str.title()


# -----------------------------
# SAVE OUTPUT
# -----------------------------
merged.to_csv('cleaned_main.csv', index=False)

print("✅ Cleaning completed successfully!")