import psycopg2

class DatabaseManager:
    def __init__(self, dbname, user, password, host):
        self.conn = None
        self.cursor = None
        self.dbname = Marketing CRUD 30221 A5
        self.user = 
        self.password = Vaishnavi
        self.host = localhost

    def connect(self):
        """Establishes a connection to the PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host
            )
            self.cursor = self.conn.cursor()
            return True
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            return False

    def disconnect(self):
        """Closes the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    # --- Company Portfolio (CRUD) ---

    def create_company(self, name, industry, website, description):
        """Adds a new company to the portfolio."""
        try:
            query = "INSERT INTO companies (company_name, industry, website, description) VALUES (%s, %s, %s, %s) RETURNING company_id;"
            self.cursor.execute(query, (name, industry, website, description))
            company_id = self.cursor.fetchone()[0]
            self.conn.commit()
            return company_id
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error creating company: {e}")
            return None

    def get_companies(self):
        """Retrieves all companies from the portfolio."""
        try:
            query = "SELECT * FROM companies ORDER BY company_name;"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error getting companies: {e}")
            return None

    # --- Campaign Management (CRUD) ---

    def create_campaign(self, name, start_date, end_date, budget, target_audience):
        """Creates a new marketing campaign."""
        try:
            query = "INSERT INTO campaigns (campaign_name, start_date, end_date, budget, target_audience) VALUES (%s, %s, %s, %s, %s) RETURNING campaign_id;"
            self.cursor.execute(query, (name, start_date, end_date, budget, target_audience))
            campaign_id = self.cursor.fetchone()[0]
            self.conn.commit()
            return campaign_id
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error creating campaign: {e}")
            return None
    
    def get_campaigns(self):
        """Retrieves all marketing campaigns."""
        try:
            query = "SELECT campaign_id, campaign_name FROM campaigns ORDER BY start_date DESC;"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error getting campaigns: {e}")
            return None

    # --- Lead Management (CRUD) ---

    def add_lead(self, campaign_id, name, email):
        """Adds a new lead for a specific campaign."""
        try:
            query = "INSERT INTO leads (campaign_id, name, email) VALUES (%s, %s, %s) RETURNING lead_id;"
            self.cursor.execute(query, (campaign_id, name, email))
            lead_id = self.cursor.fetchone()[0]
            self.conn.commit()
            return lead_id
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Error adding lead: {e}")
            return None
    
    def get_leads_by_campaign(self, campaign_id):
        """Retrieves leads for a specific campaign."""
        try:
            query = "SELECT name, email, status, generated_date FROM leads WHERE campaign_id = %s ORDER BY generated_date DESC;"
            self.cursor.execute(query, (campaign_id,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error getting leads: {e}")
            return None
            
    # --- Business Insights ---

    def get_marketing_insights(self):
        """Provides key business insights using aggregate functions."""
        try:
            # Total leads generated (COUNT)
            query_leads = "SELECT COUNT(*) FROM leads;"
            self.cursor.execute(query_leads)
            total_leads = self.cursor.fetchone()[0]

            # Total revenue generated (SUM)
            query_revenue = "SELECT SUM(amount) FROM revenue;"
            self.cursor.execute(query_revenue)
            total_revenue = self.cursor.fetchone()[0] or 0

            # Average budget per campaign (AVG)
            query_avg_budget = "SELECT AVG(budget) FROM campaigns;"
            self.cursor.execute(query_avg_budget)
            avg_budget = self.cursor.fetchone()[0] or 0
            
            # Max market size (MAX)
            query_max_size = "SELECT MAX(market_size_usd) FROM market_data;"
            self.cursor.execute(query_max_size)
            max_market_size = self.cursor.fetchone()[0] or 0

            # Min lead generation date (MIN)
            query_min_date = "SELECT MIN(generated_date) FROM leads;"
            self.cursor.execute(query_min_date)
            min_lead_date = self.cursor.fetchone()[0]

            return {
                "total_leads": total_leads,
                "total_revenue": total_revenue,
                "avg_budget": avg_budget,
                "max_market_size": max_market_size,
                "min_lead_date": min_lead_date
            }
        except psycopg2.Error as e:
            print(f"Error getting marketing insights: {e}")
            return None
