import streamlit as st
import requests
import pandas as pd
from datetime import datetime, date

# ===========================
# CONFIG
# ===========================
API_BASE_URL = "https://expense-tracker-68vh.onrender.com/api/v1"


# ===========================
# SESSION STATE HELPERS
# ===========================
if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "current_user" not in st.session_state:
    st.session_state.current_user = None


def get_auth_headers():
    if st.session_state.access_token:
        return {"Authorization": f"Bearer {st.session_state.access_token}"}
    return {}


# ===========================
# AUTH API CALLS
# ===========================
def api_register(email: str, password: str):
    url = f"{API_BASE_URL}/auth/register"
    payload = {"email": email, "password": password}
    resp = requests.post(url, json=payload)
    return resp


def api_login(email: str, password: str):
    url = f"{API_BASE_URL}/auth/login"
    # FastAPI OAuth2PasswordRequestForm expects form-encoded fields: username, password
    data = {"username": email, "password": password}
    resp = requests.post(url, data=data)
    return resp


def api_get_me():
    url = f"{API_BASE_URL}/users/me"
    resp = requests.get(url, headers=get_auth_headers())
    return resp


# ===========================
# CATEGORY API CALLS
# ===========================
def api_list_categories():
    url = f"{API_BASE_URL}/categories/"
    resp = requests.get(url, headers=get_auth_headers())
    return resp


def api_create_category(name: str, type_: str):
    url = f"{API_BASE_URL}/categories/"
    payload = {"name": name, "type": type_}
    resp = requests.post(url, json=payload, headers=get_auth_headers())
    return resp


def api_update_category(category_id: int, name: str | None, type_: str | None):
    url = f"{API_BASE_URL}/categories/{category_id}"
    payload = {}
    if name:
        payload["name"] = name
    if type_:
        payload["type"] = type_
    resp = requests.put(url, json=payload, headers=get_auth_headers())
    return resp


def api_delete_category(category_id: int):
    url = f"{API_BASE_URL}/categories/{category_id}"
    resp = requests.delete(url, headers=get_auth_headers())
    return resp


# ===========================
# TRANSACTION API CALLS
# ===========================
def api_list_transactions(filters: dict | None = None):
    url = f"{API_BASE_URL}/transactions/"
    params = filters or {}
    resp = requests.get(url, headers=get_auth_headers(), params=params)
    return resp


def api_create_transaction(amount: float, type_: str, description: str | None,
                           date_value: datetime, category_id: int | None):
    url = f"{API_BASE_URL}/transactions/"
    payload = {
        "amount": amount,
        "type": type_,
        "description": description,
        "date": date_value.isoformat(),
        "category_id": category_id,
    }
    resp = requests.post(url, json=payload, headers=get_auth_headers())
    return resp


def api_update_transaction(transaction_id: int, data: dict):
    url = f"{API_BASE_URL}/transactions/{transaction_id}"
    resp = requests.put(url, json=data, headers=get_auth_headers())
    return resp


def api_delete_transaction(transaction_id: int):
    url = f"{API_BASE_URL}/transactions/{transaction_id}"
    resp = requests.delete(url, headers=get_auth_headers())
    return resp


# ===========================
# REPORT API CALL
# ===========================
def api_get_summary(date_from: datetime | None = None,
                    date_to: datetime | None = None):
    url = f"{API_BASE_URL}/reports/summary"
    params = {}
    if date_from:
        params["date_from"] = date_from.isoformat()
    if date_to:
        params["date_to"] = date_to.isoformat()
    resp = requests.get(url, headers=get_auth_headers(), params=params)
    return resp


# ===========================
# UI: AUTH (LOGIN / REGISTER)
# ===========================
def page_auth():
    st.title("🔐 Expense Tracker - Authentication")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        st.subheader("Login")
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", type="primary"):
            if not login_email or not login_password:
                st.warning("Please enter email and password")
            else:
                resp = api_login(login_email, login_password)
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.access_token = data["access_token"]

                    # Fetch current user info
                    me_resp = api_get_me()
                    if me_resp.status_code == 200:
                        st.session_state.current_user = me_resp.json()
                        st.success("Logged in successfully!")
                    else:
                        st.error("Login succeeded but failed to fetch user info.")
                else:
                    st.error(f"Login failed: {resp.status_code} - {resp.text}")

    with tab_register:
        st.subheader("Register")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")

        if st.button("Register"):
            if not reg_email or not reg_password:
                st.warning("Please enter email and password")
            else:
                resp = api_register(reg_email, reg_password)
                if resp.status_code == 200 or resp.status_code == 201:
                    st.success("User registered successfully! Now login.")
                else:
                    st.error(f"Registration failed: {resp.status_code} - {resp.text}")


# ===========================
# UI: DASHBOARD
# ===========================
def page_dashboard():
    st.title("📊 Dashboard")

    if not st.session_state.current_user:
        st.info("You are not logged in.")
        return

    user = st.session_state.current_user
    st.write(f"**Logged in as:** `{user['email']}`")
    st.write(f"**User ID:** `{user['id']}`")
    st.write(f"**Active:** `{user['is_active']}`")
    st.write("---")

    st.subheader("Quick Summary (This Month)")

    today = date.today()
    first_day = date(today.year, today.month, 1)
    date_from = datetime.combine(first_day, datetime.min.time())
    date_to = datetime.combine(today, datetime.max.time())

    resp = api_get_summary(date_from=date_from, date_to=date_to)
    if resp.status_code == 200:
        summary = resp.json()
        st.write(f"**Total Income:** {summary['total_income']}")
        st.write(f"**Total Expense:** {summary['total_expense']}")
        st.write(f"**Net:** {summary['net']}")

        # Show category breakdown
        if summary["by_category"]:
            df = pd.DataFrame(summary["by_category"])
            st.markdown("**Breakdown by Category**")
            st.dataframe(df)

            # Simple bar chart for expenses vs income by category
            try:
                st.bar_chart(
                    df.set_index("category_name")[["total_amount"]]
                )
            except Exception:
                pass
    else:
        st.error(f"Failed to load summary: {resp.status_code} - {resp.text}")


# ===========================
# UI: CATEGORIES
# ===========================
def page_categories():
    st.title("🏷 Categories")

    if not st.session_state.current_user:
        st.info("You are not logged in.")
        return

    st.subheader("Create Category")
    col1, col2 = st.columns(2)
    with col1:
        cat_name = st.text_input("Category Name")
    with col2:
        cat_type = st.selectbox("Type", ["income", "expense"])

    if st.button("Add Category"):
        if not cat_name:
            st.warning("Please enter a name")
        else:
            resp = api_create_category(cat_name, cat_type)
            if resp.status_code in (200, 201):
                st.success("Category created successfully")
            else:
                st.error(f"Failed to create category: {resp.status_code} - {resp.text}")

    st.markdown("---")
    st.subheader("Existing Categories")

    resp = api_list_categories()
    if resp.status_code == 200:
        cats = resp.json()
        if not cats:
            st.info("No categories yet.")
        else:
            df = pd.DataFrame(cats)
            st.dataframe(df)

            # Simple inline editor for delete/update
            with st.expander("Edit / Delete Category"):
                cat_ids = [c["id"] for c in cats]
                selected_id = st.selectbox("Select Category ID", cat_ids) if cat_ids else None
                if selected_id is not None:
                    selected_cat = next((c for c in cats if c["id"] == selected_id), None)
                    if selected_cat:
                        new_name = st.text_input("New Name", value=selected_cat["name"])
                        new_type = st.selectbox(
                            "New Type",
                            ["income", "expense"],
                            index=0 if selected_cat["type"] == "income" else 1,
                        )

                        col_a, col_b = st.columns(2)
                        with col_a:
                            if st.button("Update Category"):
                                resp_u = api_update_category(selected_id, new_name, new_type)
                                if resp_u.status_code == 200:
                                    st.success("Updated successfully. Refresh page.")
                                else:
                                    st.error(
                                        f"Update failed: {resp_u.status_code} - {resp_u.text}"
                                    )
                        with col_b:
                            if st.button("Delete Category"):
                                resp_d = api_delete_category(selected_id)
                                if resp_d.status_code == 204:
                                    st.success("Deleted successfully. Refresh page.")
                                else:
                                    st.error(
                                        f"Delete failed: {resp_d.status_code} - {resp_d.text}"
                                    )
    else:
        st.error(f"Failed to fetch categories: {resp.status_code} - {resp.text}")


# ===========================
# UI: TRANSACTIONS
# ===========================
def page_transactions():
    st.title("💸 Transactions")

    if not st.session_state.current_user:
        st.info("You are not logged in.")
        return

    # Fetch categories for dropdown
    cat_resp = api_list_categories()
    categories = cat_resp.json() if cat_resp.status_code == 200 else []

    st.subheader("Add Transaction")
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        tx_type = st.selectbox("Type", ["income", "expense"])
        tx_date = st.date_input("Date", value=date.today())
    with col2:
        description = st.text_input("Description", "")
        cat_options = ["(None)"] + [f"{c['id']} - {c['name']}" for c in categories]
        cat_choice = st.selectbox("Category", cat_options)

    category_id = None
    if cat_choice != "(None)":
        category_id = int(cat_choice.split(" - ")[0])

    if st.button("Add Transaction"):
        dt = datetime.combine(tx_date, datetime.min.time())
        resp = api_create_transaction(
            amount=amount,
            type_=tx_type,
            description=description or None,
            date_value=dt,
            category_id=category_id,
        )
        if resp.status_code in (200, 201):
            st.success("Transaction added successfully")
        else:
            st.error(f"Failed to add transaction: {resp.status_code} - {resp.text}")

    st.markdown("---")
    st.subheader("Filter & View Transactions")

    with st.expander("Filters"):
        f_type = st.selectbox("Type filter", ["All", "income", "expense"])
        f_cat = st.selectbox("Category filter", ["All"] + cat_options[1:])
        f_from = st.date_input("From", value=None, key="tx_filter_from")
        f_to = st.date_input("To", value=None, key="tx_filter_to")

        filters = {}
        if f_type != "All":
            filters["type"] = f_type
        if f_cat != "All" and f_cat != "(None)":
            filters["category_id"] = int(f_cat.split(" - ")[0])
        if f_from:
            filters["date_from"] = datetime.combine(f_from, datetime.min.time()).isoformat()
        if f_to:
            filters["date_to"] = datetime.combine(f_to, datetime.max.time()).isoformat()

    list_resp = api_list_transactions(filters)
    if list_resp.status_code == 200:
        txs = list_resp.json()
        if not txs:
            st.info("No transactions found for selected filters.")
        else:
            df = pd.DataFrame(txs)
            st.dataframe(df)
    else:
        st.error(f"Failed to fetch transactions: {list_resp.status_code} - {list_resp.text}")


# ===========================
# UI: REPORTS
# ===========================
def page_reports():
    st.title("📈 Reports & Summary")

    if not st.session_state.current_user:
        st.info("You are not logged in.")
        return

    st.subheader("Date Range")
    col1, col2 = st.columns(2)
    with col1:
        d_from = st.date_input("From", value=None, key="rep_from")
    with col2:
        d_to = st.date_input("To", value=None, key="rep_to")

    date_from = datetime.combine(d_from, datetime.min.time()) if d_from else None
    date_to = datetime.combine(d_to, datetime.max.time()) if d_to else None

    if st.button("Load Summary"):
        resp = api_get_summary(date_from=date_from, date_to=date_to)
        if resp.status_code == 200:
            summary = resp.json()
            st.write(f"**Total Income:** {summary['total_income']}")
            st.write(f"**Total Expense:** {summary['total_expense']}")
            st.write(f"**Net:** {summary['net']}")

            if summary["by_category"]:
                df = pd.DataFrame(summary["by_category"])
                st.markdown("**By Category**")
                st.dataframe(df)
                try:
                    st.bar_chart(df.set_index("category_name")[["total_amount"]])
                except Exception:
                    pass
            else:
                st.info("No data for selected range.")
        else:
            st.error(f"Failed to load summary: {resp.status_code} - {resp.text}")


# ===========================
# MAIN APP LAYOUT
# ===========================
def main():
    st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

    st.sidebar.title("💰 Expense Tracker")
    if st.session_state.current_user:
        st.sidebar.success(f"Logged in as\n{st.session_state.current_user['email']}")
        if st.sidebar.button("Logout"):
            st.session_state.access_token = None
            st.session_state.current_user = None
            st.experimental_rerun()
    else:
        st.sidebar.info("Not logged in")

    menu = st.sidebar.radio(
        "Navigation",
        options=["Auth", "Dashboard", "Categories", "Transactions", "Reports"],
    )

    if menu == "Auth":
        page_auth()
    elif menu == "Dashboard":
        page_dashboard()
    elif menu == "Categories":
        page_categories()
    elif menu == "Transactions":
        page_transactions()
    elif menu == "Reports":
        page_reports()


if __name__ == "__main__":
    main()
