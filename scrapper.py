import requests
import pandas as pd
import time
from datetime import datetime
import os
from typing import List, Dict, Any
import logging
import sys

os.environ['GITHUB_TOKEN'] = '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'

class GitHubDataFetcher:
    def __init__(self, token: str):
        """Initialize with GitHub token and set up headers."""
        self.token = token.strip().strip("'").strip('"')
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = 'https://api.github.com'
        
        # Set up logging for status tracking
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('GitHubDataFetcher')
        self._validate_token()

    def _validate_token(self) -> bool:
        """Check if the provided GitHub token is valid."""
        response = requests.get(f'{self.base_url}/user', headers=self.headers)
        if response.status_code == 401:
            self.logger.error("GitHub token is invalid. Please verify your token.")
            return False
        self.logger.info("GitHub token validated successfully.")
        return True

    def get_user_info(self, username: str) -> Dict[str, Any]:
        """Fetch details for a given GitHub user."""
        url = f'{self.base_url}/users/{username}'
        response = requests.get(url, headers=self.headers)
        
        if response.ok:
            self.logger.info(f"Fetched data for user: {username}")
            return response.json()
        else:
            self.logger.warning(f"Failed to fetch data for user: {username}. Status code: {response.status_code}")
            return {}

    def get_repo_info(self, username: str) -> List[Dict[str, Any]]:
        """Retrieve repository data for a given user."""
        url = f'{self.base_url}/users/{username}/repos'
        response = requests.get(url, headers=self.headers)
        
        if response.ok:
            self.logger.info(f"Repositories fetched for user: {username}")
            return response.json()
        else:
            self.logger.warning(f"Failed to retrieve repositories for user: {username}. Status code: {response.status_code}")
            return []

    def save_to_csv(self, data: List[Dict[str, Any]], file_path: str) -> None:
        """Save fetched data to a CSV file."""
        if data:
            pd.DataFrame(data).to_csv(file_path, index=False)
            self.logger.info(f"Data saved at {file_path}")
        else:
            self.logger.warning("No data available to save.")

# Example usage
if __name__ == '__main__':
    token = os.getenv('GITHUB_TOKEN')
    fetcher = GitHubDataFetcher(token=token)
    user_info = fetcher.get_user_info('exampleuser')
    repo_info = fetcher.get_repo_info('exampleuser')
    fetcher.save_to_csv(repo_info, 'exampleuser_repos.csv')