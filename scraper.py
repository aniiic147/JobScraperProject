print("Script starting...")
import pandas as pd
import random
import logging
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

# Realistic data pools
JOB_TITLES = [
    "Software Engineer", "Senior Software Engineer", "Frontend Developer",
    "Backend Developer", "Full Stack Developer", "DevOps Engineer",
    "Data Scientist", "Data Analyst", "Machine Learning Engineer",
    "Product Manager", "UX Designer", "UI/UX Designer",
    "Python Developer", "Java Developer", "JavaScript Developer",
    "Cloud Engineer", "Site Reliability Engineer", "Security Engineer",
    "Mobile Developer", "iOS Developer", "Android Developer",
    "QA Engineer", "Solutions Architect", "Technical Lead"
]

COMPANIES = [
    "Google", "Amazon", "Microsoft", "Apple", "Meta",
    "Netflix", "Spotify", "Airbnb", "Uber", "Lyft",
    "Shopify", "Salesforce", "Adobe", "Oracle", "IBM",
    "Twitter", "LinkedIn", "Dropbox", "Slack", "Zoom",
    "Square", "Stripe", "PayPal", "Coinbase", "Robinhood",
    "Atlassian", "ServiceNow", "Workday", "HubSpot", "Zendesk",
    "GitHub", "GitLab", "Docker", "Red Hat", "VMware"
]

LOCATIONS = [
    "San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
    "Boston, MA", "Los Angeles, CA", "Chicago, IL", "Denver, CO",
    "Portland, OR", "Atlanta, GA", "Remote", "Remote (US)",
    "Remote (Global)", "Toronto, Canada", "London, UK", "Berlin, Germany",
    "Amsterdam, Netherlands", "Singapore", "Sydney, Australia", "Tokyo, Japan"
]

SKILLS = [
    ["Python", "Django", "Flask", "PostgreSQL"],
    ["JavaScript", "React", "Node.js", "MongoDB"],
    ["Java", "Spring Boot", "MySQL", "AWS"],
    ["Python", "Machine Learning", "TensorFlow", "scikit-learn"],
    ["Go", "Kubernetes", "Docker", "AWS"],
    ["TypeScript", "Angular", "Vue.js", "GraphQL"],
    ["C++", "Linux", "Git", "Jenkins"],
    ["React Native", "iOS", "Android", "Firebase"],
    ["SQL", "Tableau", "Power BI", "Excel"],
    ["AWS", "Azure", "GCP", "Terraform"]
]

def generate_salary():
    """Generate realistic salary"""
    base = random.choice([60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200])
    return f"${base}k - ${base + 30}k"

def generate_job_data(num_jobs=200):
    """
    Generate realistic job data
    
    Args:
        num_jobs: Number of job listings to generate
    
    Returns:
        List of job dictionaries
    """
    jobs = []
    
    logging.info(f"Generating {num_jobs} job listings...")
    
    for i in range(num_jobs):
        # Randomly select job details
        title = random.choice(JOB_TITLES)
        company = random.choice(COMPANIES)
        location = random.choice(LOCATIONS)
        salary = generate_salary()
        skills = ', '.join(random.choice(SKILLS))
        
        # Random date within last 30 days
        days_ago = random.randint(0, 30)
        posted_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        job = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'skills': skills,
            'posted_date': posted_date,
            'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        jobs.append(job)
    
    logging.info(f"Generated {len(jobs)} job listings successfully")
    return jobs

def save_to_csv(jobs, filename='jobs_data.csv'):
    """Save job data to CSV file"""
    try:
        df = pd.DataFrame(jobs)
        df.to_csv(filename, index=False)
        logging.info(f"Data saved to {filename}")
        print(f"\n✅ Saved {len(jobs)} jobs to {filename}")
        return df
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")
        return None

if __name__ == "__main__":
    print("\n" + "="*60)
    print("JOB DATA GENERATOR")
    print("="*60)
    print("\nThis generates realistic job data for analysis and demonstration.")
    
    # Get user input
    try:
        num_jobs = int(input("\nHow many job listings to generate? (default: 200): ") or "200")
    except ValueError:
        num_jobs = 200
        print("Using default: 200 jobs")
    
    print(f"\nGenerating {num_jobs} realistic job listings...\n")
    
    # Generate jobs
    jobs = generate_job_data(num_jobs)
    
    # Save to CSV
    if jobs:
        df = save_to_csv(jobs)
        print(f"\n📊 Preview of generated data:")
        print("="*60)
        print(df[['title', 'company', 'location', 'salary']].head(10))
        print(f"\n✅ Total jobs generated: {len(jobs)}")
        print("\n💡 Next step: Run 'python analyzer.py' to analyze this data!")
    else:
        print("❌ Failed to generate jobs.")