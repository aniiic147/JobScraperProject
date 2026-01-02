import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO)

def load_data(filename='jobs_data.csv'):
    """Load job data from CSV"""
    try:
        df = pd.read_csv(filename)
        logging.info(f"Loaded {len(df)} jobs from {filename}")
        return df
    except FileNotFoundError:
        logging.error(f"File {filename} not found. Run scraper.py first!")
        return None
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None

def clean_salary(salary_str):
    """Extract numeric salary from string"""
    if pd.isna(salary_str) or salary_str == 'N/A':
        return None
    
    # Extract numbers from salary string
    numbers = re.findall(r'\d+', salary_str.replace(',', ''))
    if numbers:
        # If range, take average
        nums = [int(n) for n in numbers]
        return sum(nums) / len(nums)
    return None

def analyze_salaries(df):
    """Analyze salary data"""
    print("\n" + "="*50)
    print("SALARY ANALYSIS")
    print("="*50)
    
    # Clean salary column
    df['salary_numeric'] = df['salary'].apply(clean_salary)
    
    # Filter out N/A salaries
    salary_data = df[df['salary_numeric'].notna()]
    
    if len(salary_data) > 0:
        print(f"\nJobs with salary info: {len(salary_data)}")
        print(f"Average salary: ${salary_data['salary_numeric'].mean():,.0f}")
        print(f"Median salary: ${salary_data['salary_numeric'].median():,.0f}")
        print(f"Min salary: ${salary_data['salary_numeric'].min():,.0f}")
        print(f"Max salary: ${salary_data['salary_numeric'].max():,.0f}")
        
        # Plot salary distribution
        plt.figure(figsize=(10, 6))
        plt.hist(salary_data['salary_numeric'], bins=20, color='skyblue', edgecolor='black')
        plt.xlabel('Salary ($)')
        plt.ylabel('Frequency')
        plt.title('Salary Distribution')
        plt.tight_layout()
        plt.savefig('salary_distribution.png')
        logging.info("Saved salary_distribution.png")
        plt.close()
    else:
        print("\nNo salary information available in the data.")

def analyze_locations(df):
    """Analyze job locations"""
    print("\n" + "="*50)
    print("LOCATION ANALYSIS")
    print("="*50)
    
    location_counts = df['location'].value_counts().head(10)
    print("\nTop 10 locations:")
    print(location_counts)
    
    # Plot top locations
    plt.figure(figsize=(12, 6))
    location_counts.plot(kind='barh', color='coral')
    plt.xlabel('Number of Jobs')
    plt.ylabel('Location')
    plt.title('Top 10 Job Locations')
    plt.tight_layout()
    plt.savefig('top_locations.png')
    logging.info("Saved top_locations.png")
    plt.close()

def analyze_companies(df):
    """Analyze top hiring companies"""
    print("\n" + "="*50)
    print("COMPANY ANALYSIS")
    print("="*50)
    
    company_counts = df['company'].value_counts().head(10)
    print("\nTop 10 hiring companies:")
    print(company_counts)
    
    # Plot top companies
    plt.figure(figsize=(12, 6))
    company_counts.plot(kind='barh', color='lightgreen')
    plt.xlabel('Number of Job Postings')
    plt.ylabel('Company')
    plt.title('Top 10 Hiring Companies')
    plt.tight_layout()
    plt.savefig('top_companies.png')
    logging.info("Saved top_companies.png")
    plt.close()

def analyze_titles(df):
    """Analyze common words in job titles"""
    print("\n" + "="*50)
    print("JOB TITLE ANALYSIS")
    print("="*50)
    
    # Combine all titles
    all_titles = ' '.join(df['title'].astype(str)).lower()
    
    # Remove common words
    stop_words = {'and', 'or', 'the', 'a', 'an', 'in', 'at', 'to', 'for', 'of', 'on', '-', '/'}
    words = re.findall(r'\b\w+\b', all_titles)
    words = [w for w in words if w not in stop_words and len(w) > 2]
    
    # Count word frequency
    word_counts = Counter(words).most_common(15)
    
    print("\nMost common words in job titles:")
    for word, count in word_counts:
        print(f"{word}: {count}")
    
    # Plot word frequency
    words_list, counts_list = zip(*word_counts)
    
    plt.figure(figsize=(12, 6))
    plt.barh(words_list, counts_list, color='mediumpurple')
    plt.xlabel('Frequency')
    plt.ylabel('Word')
    plt.title('Most Common Words in Job Titles')
    plt.tight_layout()
    plt.savefig('title_keywords.png')
    logging.info("Saved title_keywords.png")
    plt.close()

def generate_summary(df):
    """Generate overall summary"""
    print("\n" + "="*50)
    print("SUMMARY REPORT")
    print("="*50)
    print(f"\nTotal jobs scraped: {len(df)}")
    print(f"Unique companies: {df['company'].nunique()}")
    print(f"Unique locations: {df['location'].nunique()}")
    print(f"Jobs with salary info: {df[df['salary'] != 'N/A'].shape[0]}")
    print(f"\nData saved in: jobs_data.csv")
    print(f"Visualizations saved as PNG files")

if __name__ == "__main__":
    # Load data
    df = load_data('jobs_data.csv')
    
    if df is not None:
        # Run all analyses
        analyze_salaries(df)
        analyze_locations(df)
        analyze_companies(df)
        analyze_titles(df)
        generate_summary(df)
        
        print("\n✅ Analysis complete! Check the PNG files for visualizations.")
    else:
        print("❌ Could not load data. Make sure to run scraper.py first!")