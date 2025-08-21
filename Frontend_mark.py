import streamlit as st
import pandas as pd
from backend_mark import DatabaseManager
from datetime import datetime

# Initialize database manager (replace with your actual credentials)
db = DatabaseManager(
    dbname="your_db_name",
    user="your_db_user",
    password="your_db_password",
    host="your_db_host"
)

def main():
    st.title("Marketing Dashboard")

    if not db.connect():
        st.error("Could not connect to the database. Please check your credentials.")
        return

    st.sidebar.header("Navigation")
    menu = ["Dashboard", "Campaigns", "Leads", "Portfolio"]
    choice = st.sidebar.selectbox("Select an option:", menu)
    
    if choice == "Dashboard":
        st.subheader("Business Insights Dashboard")
        
        insights = db.get_marketing_insights()
        if insights:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Leads Generated", insights['total_leads'])
            with col2:
                st.metric("Total Revenue", f"${insights['total_revenue']:.2f}")
            with col3:
                st.metric("Average Campaign Budget", f"${insights['avg_budget']:.2f}")
            
            st.markdown("---")
            st.write(f"**Max Recorded Market Size:** ${insights['max_market_size']:,}")
            st.write(f"**First Lead Generated On:** {insights['min_lead_date']}")

        else:
            st.info("No data available for insights.")
            
    elif choice == "Campaigns":
        st.subheader("Campaign Management")
        with st.form("campaign_form"):
            campaign_name = st.text_input("Campaign Name")
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            budget = st.number_input("Budget ($)", min_value=0.0)
            target_audience = st.text_area("Target Audience Description")
            submitted = st.form_submit_button("Create Campaign")
            if submitted:
                if campaign_name:
                    campaign_id = db.create_campaign(campaign_name, start_date, end_date, budget, target_audience)
                    if campaign_id:
                        st.success(f"Campaign '{campaign_name}' created successfully with ID: {campaign_id}")
                    else:
                        st.error("Failed to create campaign.")
                else:
                    st.warning("Campaign Name is required.")
        
        st.markdown("---")
        st.subheader("Existing Campaigns")
        campaigns = db.get_campaigns()
        if campaigns:
            df_campaigns = pd.DataFrame(campaigns, columns=['ID', 'Name'])
            st.dataframe(df_campaigns)
        else:
            st.info("No campaigns found.")

    elif choice == "Leads":
        st.subheader("Lead Generation")
        
        campaigns = db.get_campaigns()
        if not campaigns:
            st.warning("Please create a campaign first to add leads.")
            return

        campaign_options = {c[1]: c[0] for c in campaigns}
        selected_campaign_name = st.selectbox("Select a Campaign:", list(campaign_options.keys()))
        selected_campaign_id = campaign_options[selected_campaign_name]

        with st.form("lead_form"):
            lead_name = st.text_input("Lead Name")
            lead_email = st.text_input("Lead Email")
            submitted = st.form_submit_button("Add Lead")
            if submitted:
                if lead_name and lead_email:
                    lead_id = db.add_lead(selected_campaign_id, lead_name, lead_email)
                    if lead_id:
                        st.success(f"Lead '{lead_name}' added successfully!")
                    else:
                        st.error("Failed to add lead.")
                else:
                    st.warning("Name and Email are required.")

        st.markdown("---")
        st.subheader(f"Leads for '{selected_campaign_name}'")
        leads = db.get_leads_by_campaign(selected_campaign_id)
        if leads:
            df_leads = pd.DataFrame(leads, columns=['Name', 'Email', 'Status', 'Generated Date'])
            st.dataframe(df_leads)
        else:
            st.info("No leads generated for this campaign yet.")

    elif choice == "Portfolio":
        st.subheader("Company Portfolio")
        with st.form("company_form"):
            company_name = st.text_input("Company Name")
            industry = st.text_input("Industry")
            website = st.text_input("Website")
            description = st.text_area("Description")
            submitted = st.form_submit_button("Add Company")
            if submitted:
                if company_name:
                    company_id = db.create_company(company_name, industry, website, description)
                    if company_id:
                        st.success(f"Company '{company_name}' added successfully!")
                    else:
                        st.error("Failed to add company. It might already exist.")
                else:
                    st.warning("Company Name is required.")

        st.markdown("---")
        st.subheader("All Companies in Portfolio")
        companies = db.get_companies()
        if companies:
            df_companies = pd.DataFrame(companies, columns=['ID', 'Name', 'Industry', 'Website', 'Description'])
            st.dataframe(df_companies)
        else:
            st.info("No companies in your portfolio yet.")

    db.disconnect()

if __name__ == '__main__':
    main()
