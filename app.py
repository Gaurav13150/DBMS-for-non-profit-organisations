import streamlit as st
from supabase import create_client
from datetime import date
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="DevatmaShakti Ashram | Event Management",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================================================
       GLOBAL FONT & TEXT COLORS
       ========================================================= */

    .stApp {
        background-color: #f7f8fa;
        color: #111827;
    }

    /* Main application text */
    .main,
    .main * {
        color: #111827;
    }

    /* Streamlit headings */
    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
        font-weight: 600 !important;
    }

    /* Markdown text */
    .stMarkdown,
    .stMarkdown p,
    .stMarkdown span,
    .stMarkdown div {
        color: #111827 !important;
    }

    /* Labels */
    label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p {
        color: #111827 !important;
    }

    /* Input text */
    input,
    textarea,
    select {
        color: #111827 !important;
    }

    /* Selectbox text */
    div[data-baseweb="select"] * {
        color: #111827 !important;
    }

    /* Dataframe text */
    [data-testid="stDataFrame"] * {
        color: #111827 !important;
    }


    /* =========================================================
       SIDEBAR
       ========================================================= */

    section[data-testid="stSidebar"] {
        background-color: #172033;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #ffffff !important;
        padding: 8px 5px;
        font-size: 14px;
    }
# ============================================================
# SUPABASE CONNECTION
# ============================================================

try:
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

except Exception as e:
    st.error("Unable to connect to the Supabase database.")
    st.info(
        "Check that SUPABASE_URL and SUPABASE_KEY are correctly "
        "configured in Streamlit Secrets."
    )
    st.stop()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_events():
    response = (
        supabase
        .table("events")
        .select("*")
        .order("event_date", desc=True)
        .execute()
    )
    return response.data or []


def get_people():
    response = (
        supabase
        .table("volunteers_staff")
        .select("*")
        .order("name")
        .execute()
    )
    return response.data or []


def get_expenses():
    response = (
        supabase
        .table("expenses")
        .select("*")
        .order("expense_date", desc=True)
        .execute()
    )
    return response.data or []


def get_resources():
    response = (
        supabase
        .table("resources")
        .select("*")
        .order("resource_id", desc=True)
        .execute()
    )
    return response.data or []


def format_currency(value):
    return f"₹{value:,.2f}"


def safe_float(value):
    try:
        return float(value)
    except:
        return 0.0


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("""
    """
    <div style="padding: 10px 0 25px 0;">
        <div style="
            font-size:20px;
            font-weight:650;
            color:white;
        ">
            DevatmaShakti Ashram
        </div>

        <div style="
            font-size:12px;
            color:#b8c0cc;
            margin-top:4px;
        ">
            Event Management System
        </div>
    </div>
    """,
   """, unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Events",
        "Volunteers & Staff",
        "Expenses",
        "Resources",
        "Reports & Analytics"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption("Database: Supabase PostgreSQL")
st.sidebar.caption("Application: Streamlit")


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    f"""
    <div class="app-header">
        <div class="app-title">{page}</div>
        <div class="app-subtitle">
            DevatmaShakti Ashram Event Management System
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "Dashboard":

    events = get_events()
    people = get_people()
    expenses = get_expenses()
    resources = get_resources()

    total_events = len(events)
    total_people = len(people)

    volunteer_count = len(
        [p for p in people if p.get("type") == "Volunteer"]
    )

    staff_count = len(
        [p for p in people if p.get("type") == "Staff"]
    )

    total_expenses = sum(
        safe_float(e.get("amount"))
        for e in expenses
    )

    total_resources = len(resources)

    today = date.today().isoformat()

    upcoming_events = [
        e for e in events
        if e.get("event_date") and e["event_date"] >= today
    ]

    # ---------- Metrics ----------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Events</div>
                <div class="metric-value">{total_events}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Volunteers</div>
                <div class="metric-value">{volunteer_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Staff Members</div>
                <div class="metric-value">{staff_count}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Total Expenses</div>
                <div class="metric-value">
                    {format_currency(total_expenses)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- Upcoming Events ----------

    st.markdown(
        '<div class="section-title">Upcoming Events</div>',
        unsafe_allow_html=True
    )

    if upcoming_events:

        upcoming_df = pd.DataFrame(upcoming_events)

        columns = [
            "event_name",
            "event_date",
            "category",
            "location",
            "status"
        ]

        available_columns = [
            col for col in columns
            if col in upcoming_df.columns
        ]

        display_df = upcoming_df[available_columns].copy()

        rename_map = {
            "event_name": "Event",
            "event_date": "Date",
            "category": "Category",
            "location": "Location",
            "status": "Status"
        }

        display_df.rename(
            columns=rename_map,
            inplace=True
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No upcoming events have been registered.")

    # ---------- Statistics ----------

    st.markdown(
        '<div class="section-title">Event Statistics</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    if events:

        event_df = pd.DataFrame(events)

        with col1:

            if "category" in event_df.columns:

                category_data = (
                    event_df["category"]
                    .value_counts()
                )

                st.markdown("**Events by Category**")

                st.bar_chart(category_data)

        with col2:

            if "status" in event_df.columns:

                status_data = (
                    event_df["status"]
                    .value_counts()
                )

                st.markdown("**Events by Status**")

                st.bar_chart(status_data)

    else:
        st.info("Statistics will appear after events are registered.")


# ============================================================
# EVENTS
# ============================================================

elif page == "Events":

    st.markdown(
        '<div class="section-title">Register New Event</div>',
        unsafe_allow_html=True
    )

    with st.form("event_form"):

        col1, col2 = st.columns(2)

        with col1:

            event_name = st.text_input(
                "Event Name *"
            )

            event_date = st.date_input(
                "Event Date",
                value=date.today()
            )

            start_time = st.time_input(
                "Start Time"
            )

            category = st.selectbox(
                "Category",
                [
                    "Spiritual",
                    "Educational",
                    "Community Service",
                    "Health",
                    "Cultural",
                    "Environmental",
                    "Fundraising",
                    "Other"
                ]
            )

        with col2:

            location = st.text_input(
                "Location"
            )

            end_time = st.time_input(
                "End Time"
            )

            status = st.selectbox(
                "Status",
                [
                    "Planned",
                    "Ongoing",
                    "Completed",
                    "Cancelled"
                ]
            )

        description = st.text_area(
            "Description"
        )

        submit_event = st.form_submit_button(
            "Register Event"
        )

        if submit_event:

            if not event_name.strip():
                st.error("Event name is required.")

            elif end_time <= start_time:
                st.error(
                    "End time must be later than start time."
                )

            else:

                try:

                    supabase.table("events").insert(
                        {
                            "event_name": event_name.strip(),
                            "event_date": str(event_date),
                            "start_time": str(start_time),
                            "end_time": str(end_time),
                            "category": category,
                            "location": location.strip(),
                            "description": description.strip(),
                            "status": status
                        }
                    ).execute()

                    st.success(
                        "Event registered successfully."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Unable to register event: {e}"
                    )

    st.markdown("---")

    st.markdown(
        '<div class="section-title">Manage Events</div>',
        unsafe_allow_html=True
    )

    events = get_events()

    if events:

        event_df = pd.DataFrame(events)

        search = st.text_input(
            "Search Events",
            placeholder="Search by event name, category or location"
        )

        if search:

            search_lower = search.lower()

            mask = (
                event_df.astype(str)
                .apply(
                    lambda row:
                    row.str.lower()
                    .str.contains(
                        search_lower,
                        na=False
                    )
                    .any(),
                    axis=1
                )
            )

            event_df = event_df[mask]

        display_columns = [
            "event_id",
            "event_name",
            "event_date",
            "start_time",
            "end_time",
            "category",
            "location",
            "status"
        ]

        available = [
            c for c in display_columns
            if c in event_df.columns
        ]

        display_df = event_df[available].copy()

        display_df.rename(
            columns={
                "event_id": "ID",
                "event_name": "Event",
                "event_date": "Date",
                "start_time": "Start",
                "end_time": "End",
                "category": "Category",
                "location": "Location",
                "status": "Status"
            },
            inplace=True
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Delete Event")

        event_options = {
            f'{e["event_id"]} — {e["event_name"]}':
            e["event_id"]
            for e in events
        }

        selected_event = st.selectbox(
            "Select event",
            list(event_options.keys())
        )

        if st.button(
            "Delete Selected Event",
            type="secondary"
        ):

            event_id = event_options[selected_event]

            try:

                supabase.table("events").delete().eq(
                    "event_id",
                    event_id
                ).execute()

                st.success(
                    "Event deleted successfully."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Unable to delete event: {e}"
                )

    else:

        st.info(
            "No events have been registered yet."
        )


# ============================================================
# VOLUNTEERS & STAFF
# ============================================================

elif page == "Volunteers & Staff":

    st.markdown(
        '<div class="section-title">Add Volunteer or Staff Member</div>',
        unsafe_allow_html=True
    )

    with st.form("people_form"):

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "Full Name *"
            )

            role = st.text_input(
                "Role"
            )

            phone = st.text_input(
                "Phone"
            )

        with col2:

            email = st.text_input(
                "Email"
            )

            person_type = st.selectbox(
                "Type",
                [
                    "Volunteer",
                    "Staff"
                ]
            )

        submit_person = st.form_submit_button(
            "Add Person"
        )

        if submit_person:

            if not name.strip():

                st.error(
                    "Name is required."
                )

            else:

                try:

                    supabase.table(
                        "volunteers_staff"
                    ).insert(
                        {
                            "name": name.strip(),
                            "role": role.strip(),
                            "phone": phone.strip(),
                            "email": email.strip(),
                            "type": person_type
                        }
                    ).execute()

                    st.success(
                        "Record added successfully."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Unable to add record: {e}"
                    )

    st.markdown("---")

    people = get_people()

    if people:

        people_df = pd.DataFrame(people)

        filter_type = st.selectbox(
            "Filter by Type",
            [
                "All",
                "Volunteer",
                "Staff"
            ]
        )

        if filter_type != "All":

            people_df = people_df[
                people_df["type"] == filter_type
            ]

        display_columns = [
            "person_id",
            "name",
            "role",
            "phone",
            "email",
            "type"
        ]

        available = [
            c for c in display_columns
            if c in people_df.columns
        ]

        display_df = people_df[available].copy()

        display_df.rename(
            columns={
                "person_id": "ID",
                "name": "Name",
                "role": "Role",
                "phone": "Phone",
                "email": "Email",
                "type": "Type"
            },
            inplace=True
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No volunteer or staff records have been added."
        )


# ============================================================
# EXPENSES
# ============================================================

elif page == "Expenses":

    events = get_events()

    st.markdown(
        '<div class="section-title">Record Expense</div>',
        unsafe_allow_html=True
    )

    if not events:

        st.warning(
            "Register an event before recording an expense."
        )

    else:

        event_options = {
            f'{e["event_id"]} — {e["event_name"]}':
            e["event_id"]
            for e in events
        }

        with st.form("expense_form"):

            selected_event = st.selectbox(
                "Event",
                list(event_options.keys())
            )

            col1, col2 = st.columns(2)

            with col1:

                expense_date = st.date_input(
                    "Expense Date",
                    value=date.today()
                )

                expense_category = st.selectbox(
                    "Expense Category",
                    [
                        "Food",
                        "Transportation",
                        "Supplies",
                        "Equipment",
                        "Medical",
                        "Utilities",
                        "Venue",
                        "Other"
                    ]
                )

            with col2:

                amount = st.number_input(
                    "Amount (₹)",
                    min_value=0.0,
                    step=100.0
                )

                description = st.text_input(
                    "Description"
                )

            submit_expense = st.form_submit_button(
                "Record Expense"
            )

            if submit_expense:

                if amount <= 0:

                    st.error(
                        "Expense amount must be greater than zero."
                    )

                else:

                    try:

                        supabase.table(
                            "expenses"
                        ).insert(
                            {
                                "event_id":
                                    event_options[selected_event],

                                "expense_date":
                                    str(expense_date),

                                "category":
                                    expense_category,

                                "description":
                                    description.strip(),

                                "amount":
                                    amount
                            }
                        ).execute()

                        st.success(
                            "Expense recorded successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Unable to record expense: {e}"
                        )

    st.markdown("---")

    expenses = get_expenses()

    if expenses:

        expense_df = pd.DataFrame(expenses)

        total = expense_df["amount"].sum()

        st.metric(
            "Total Recorded Expenses",
            format_currency(total)
        )

        display_columns = [
            "expense_id",
            "event_id",
            "expense_date",
            "category",
            "description",
            "amount"
        ]

        available = [
            c for c in display_columns
            if c in expense_df.columns
        ]

        display_df = expense_df[available].copy()

        display_df.rename(
            columns={
                "expense_id": "ID",
                "event_id": "Event ID",
                "expense_date": "Date",
                "category": "Category",
                "description": "Description",
                "amount": "Amount"
            },
            inplace=True
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No expenses have been recorded."
        )


# ============================================================
# RESOURCES
# ============================================================

elif page == "Resources":

    events = get_events()

    st.markdown(
        '<div class="section-title">Record Resource</div>',
        unsafe_allow_html=True
    )

    if not events:

        st.warning(
            "Register an event before adding resources."
        )

    else:

        event_options = {
            f'{e["event_id"]} — {e["event_name"]}':
            e["event_id"]
            for e in events
        }

        with st.form("resource_form"):

            selected_event = st.selectbox(
                "Event",
                list(event_options.keys())
            )

            col1, col2 = st.columns(2)

            with col1:

                resource_name = st.text_input(
                    "Resource Name *"
                )

                quantity = st.number_input(
                    "Quantity",
                    min_value=0.0,
                    step=1.0
                )

            with col2:

                unit = st.text_input(
                    "Unit",
                    placeholder="e.g. pieces, litres, kg"
                )

                description = st.text_input(
                    "Description"
                )

            submit_resource = st.form_submit_button(
                "Add Resource"
            )

            if submit_resource:

                if not resource_name.strip():

                    st.error(
                        "Resource name is required."
                    )

                elif quantity <= 0:

                    st.error(
                        "Quantity must be greater than zero."
                    )

                else:

                    try:

                        supabase.table(
                            "resources"
                        ).insert(
                            {
                                "event_id":
                                    event_options[selected_event],

                                "resource_name":
                                    resource_name.strip(),

                                "quantity":
                                    quantity,

                                "unit":
                                    unit.strip(),

                                "description":
                                    description.strip()
                            }
                        ).execute()

                        st.success(
                            "Resource added successfully."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Unable to add resource: {e}"
                        )

    st.markdown("---")

    resources = get_resources()

    if resources:

        resource_df = pd.DataFrame(resources)

        display_columns = [
            "resource_id",
            "event_id",
            "resource_name",
            "quantity",
            "unit",
            "description"
        ]

        available = [
            c for c in display_columns
            if c in resource_df.columns
        ]

        display_df = resource_df[available].copy()

        display_df.rename(
            columns={
                "resource_id": "ID",
                "event_id": "Event ID",
                "resource_name": "Resource",
                "quantity": "Quantity",
                "unit": "Unit",
                "description": "Description"
            },
            inplace=True
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No resources have been recorded."
        )


# ============================================================
# REPORTS & ANALYTICS
# ============================================================

elif page == "Reports & Analytics":

    events = get_events()
    expenses = get_expenses()
    people = get_people()
    resources = get_resources()

    st.markdown(
        '<div class="section-title">Organizational Statistics</div>',
        unsafe_allow_html=True
    )

    # ---------- Summary ----------

    total_expense = sum(
        safe_float(e.get("amount"))
        for e in expenses
    )

    total_events = len(events)

    total_volunteers = len(
        [
            p for p in people
            if p.get("type") == "Volunteer"
        ]
    )

    total_staff = len(
        [
            p for p in people
            if p.get("type") == "Staff"
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Events",
            total_events
        )

    with c2:
        st.metric(
            "Volunteers",
            total_volunteers
        )

    with c3:
        st.metric(
            "Staff",
            total_staff
        )

    with c4:
        st.metric(
            "Total Expenses",
            format_currency(total_expense)
        )

    st.markdown("---")

    # ---------- Event Analysis ----------

    if events:

        event_df = pd.DataFrame(events)

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Events by Category")

            category_counts = (
                event_df["category"]
                .value_counts()
            )

            st.bar_chart(
                category_counts
            )

        with col2:

            st.markdown("### Events by Status")

            status_counts = (
                event_df["status"]
                .value_counts()
            )

            st.bar_chart(
                status_counts
            )

    # ---------- Expense Analysis ----------

    if expenses:

        st.markdown("---")

        st.markdown(
            "### Expense Analysis"
        )

        expense_df = pd.DataFrame(expenses)

        expense_category = (
            expense_df
            .groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(
            expense_category
        )

        st.markdown(
            "**Expense Summary**"
        )

        expense_summary = (
            expense_df
            .groupby("category")["amount"]
            .sum()
            .reset_index()
        )

        expense_summary.rename(
            columns={
                "category": "Category",
                "amount": "Total Amount"
            },
            inplace=True
        )

        expense_summary["Total Amount"] = (
            expense_summary["Total Amount"]
            .apply(format_currency)
        )

        st.dataframe(
            expense_summary,
            use_container_width=True,
            hide_index=True
        )

    # ---------- Resources ----------

    if resources:

        st.markdown("---")

        st.markdown(
            "### Resource Summary"
        )

        resource_df = pd.DataFrame(resources)

        resource_summary = (
            resource_df
            .groupby(
                ["resource_name", "unit"],
                dropna=False
            )["quantity"]
            .sum()
            .reset_index()
        )

        resource_summary.rename(
            columns={
                "resource_name": "Resource",
                "unit": "Unit",
                "quantity": "Total Quantity"
            },
            inplace=True
        )

        st.dataframe(
            resource_summary,
            use_container_width=True,
            hide_index=True
        )

    # ---------- Export ----------

    st.markdown("---")

    st.markdown(
        "### Export Data"
    )

    if events:

        event_export = pd.DataFrame(events)

        csv = event_export.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "Download Event Report",
            data=csv,
            file_name="devatmashakti_event_report.csv",
            mime="text/csv"
        )

    else:

        st.info(
            "There is no event data available for export."
        )
