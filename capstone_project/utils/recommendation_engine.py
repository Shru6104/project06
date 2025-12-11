import pandas as pd
import re

# -----------------------------------------
# Load dataset
# -----------------------------------------
df_rec = pd.read_csv("data/recommendation_dataset.csv")

# Clean column names
df_rec.columns = (
    df_rec.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.replace("(INR)", "INR")
)

# -----------------------------------------
# Extract CustomerID
# -----------------------------------------
def extract_customer_id(text):
    match = re.search(r"C\d{7}", text)
    if match:
        return match.group(0)
    return None

# -----------------------------------------
# Detect category
# -----------------------------------------
def detect_recommendation_type(text):
    text = text.lower()

    if "loan" in text:
        return "Loan_type", "loan"
    elif "savings" in text:
        return "savings_plan_type", "savings"
    elif "investment" in text:
        return "investment_type", "investment"
    elif "credit" in text:
        return "credit_cardtype", "credit card"
    else:
        return None, None

# -----------------------------------------
# Main Recommendation Function
# -----------------------------------------
def get_recommendation(user_text):
    column, label = detect_recommendation_type(user_text)

    # Category not detected
    if not column:
        return "Please specify: loan, savings, investment, or credit card."

    # Extract CustomerID
    customer_id = extract_customer_id(user_text)
    if not customer_id:
        return "Please provide a valid Customer ID (Example: C1234567)."

    # Filter record
    record = df_rec[df_rec["CustomerID"] == customer_id]

    if record.empty:
        return f"No customer found with ID {customer_id}"

    # Get value
    value = record[column].values[0]

    if pd.isna(value) or value == "":
        return f"No {label} information available for {customer_id}"

    # Convert "Loan1, Loan2, Loan3" → list
    items = [x.strip() for x in value.split(",")]

    # Build final response exactly as your example
    return (
        f"Customer ID : {customer_id}\n"
        f"For your {label} we suggest : {', '.join(items)}"
    )
