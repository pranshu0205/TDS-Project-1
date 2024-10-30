import pandas as pd
from datetime import datetime

# Load data from CSV files
user_data = pd.read_csv('users.csv')
repo_data = pd.read_csv('repositories.csv')

# Convert 'created_at' columns to datetime for easier manipulation
user_data['created_at'] = pd.to_datetime(user_data['created_at'])
repo_data['created_at'] = pd.to_datetime(repo_data['created_at'])

# Analysis and Answers to Queries

# Q1: Top 5 users with the most followers
top_followed_users = user_data.nlargest(5, 'followers')['login'].tolist()
answer_1 = ', '.join(top_followed_users)

# Q2: Find the earliest 5 users by creation date
earliest_users = user_data.nsmallest(5, 'created_at')['login'].tolist()
answer_2 = ', '.join(earliest_users)

# Q3: Top 3 license types by frequency in repositories
license_counts = repo_data['license_name'].value_counts()
top_licenses = license_counts[license_counts.index != ''].nlargest(3).index.tolist()
answer_3 = ', '.join(top_licenses)

# Q4: Most common company among users
most_common_company = user_data['company'].value_counts().idxmax() if not user_data['company'].isnull().all() else "No Company Data"
answer_4 = most_common_company

# Q5: Most frequently used language in repositories
most_common_language = repo_data['language'].mode()[0] if not repo_data['language'].isnull().all() else "No Language Data"
answer_5 = most_common_language

# Q6: Most common language in repos from users who joined after 2020
recent_users = user_data[user_data['created_at'] > '2020-01-01']['login']
recent_repos = repo_data[repo_data['login'].isin(recent_users)]
most_common_recent_language = recent_repos['language'].mode()[0] if not recent_repos['language'].isnull().all() else "No Language Data"
answer_6 = most_common_recent_language

# Print answers
print(f"Q1: {answer_1}")
print(f"Q2: {answer_2}")
print(f"Q3: {answer_3}")
print(f"Q4: {answer_4}")
print(f"Q5: {answer_5}")
print(f"Q6: {answer_6}")