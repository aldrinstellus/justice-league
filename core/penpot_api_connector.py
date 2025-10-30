"""
Penpot API Connector
Connects Aldo Vision to Penpot's live API for real-time design access
Python 3.9+ compatible custom implementation
"""

import requests
import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class PenpotAPIConnector:
    """
    Connect to Penpot API and fetch design data
    Works with self-hosted or cloud Penpot instances
    """

    def __init__(self, api_url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize Penpot API connector

        Args:
            api_url: Penpot API URL (default: from env or https://design.penpot.app)
            username: Penpot username (default: from env)
            password: Penpot password (default: from env)
        """
        self.api_url = api_url or os.getenv('PENPOT_API_URL', 'https://design.penpot.app')
        self.username = username or os.getenv('PENPOT_USERNAME')
        self.password = password or os.getenv('PENPOT_PASSWORD')
        self.token = None
        self.session = requests.Session()

        logger.info(f"Penpot API Connector initialized for: {self.api_url}")

    def authenticate(self) -> bool:
        """
        Authenticate with Penpot API

        Returns:
            bool: True if authentication successful
        """
        if not self.username or not self.password:
            logger.error("Username and password required for authentication")
            return False

        try:
            # Penpot authentication endpoint
            auth_url = f"{self.api_url}/api/rpc/command/login-with-password"

            payload = {
                "email": self.username,
                "password": self.password
            }

            response = self.session.post(auth_url, json=payload)
            response.raise_for_status()

            # Extract token from response
            try:
                auth_data = response.json()
                logger.info(f"Auth response type: {type(auth_data)}, content: {str(auth_data)[:500]}")
            except Exception as e:
                logger.error(f"Failed to parse JSON response: {str(e)}")
                auth_data = None

            # Handle different response formats
            if isinstance(auth_data, dict):
                self.token = auth_data.get('token') or auth_data.get('access-token')
            elif isinstance(auth_data, list) and len(auth_data) > 0:
                # Some Penpot versions return array
                first_item = auth_data[0]
                if isinstance(first_item, dict):
                    self.token = first_item.get('token') or first_item.get('access-token')
                elif isinstance(first_item, str):
                    # Token might be directly in the list
                    self.token = first_item
            else:
                self.token = None

            # Also try cookies
            if not self.token and 'auth-token' in response.cookies:
                self.token = response.cookies['auth-token']

            # Try all cookie variations
            if not self.token:
                for cookie_name in ['auth-token', 'penpot-auth', 'session', 'token']:
                    if cookie_name in response.cookies:
                        self.token = response.cookies[cookie_name]
                        logger.info(f"Found token in cookie: {cookie_name}")
                        break

            if self.token:
                # Set authorization header for future requests
                # IMPORTANT: Set Accept to application/json to avoid Transit format
                self.session.headers.update({
                    'Authorization': f'Token {self.token}',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                })
                logger.info("Successfully authenticated with Penpot API")
                return True
            else:
                logger.error(f"No token received from Penpot API. Response: {str(auth_data)[:200]}")
                # Even if no explicit token, session cookies might work
                if response.cookies:
                    logger.info("Using session cookies for authentication")
                    return True
                return False

        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication failed: {str(e)}")
            return False

    def list_projects(self, team_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all accessible projects

        Args:
            team_id: Optional team ID to filter projects

        Returns:
            List of project dictionaries
        """
        if not self.token:
            if not self.authenticate():
                return []

        try:
            url = f"{self.api_url}/api/rpc/command/get-projects"
            payload = {}
            if team_id:
                payload['team-id'] = team_id

            response = self.session.post(url, json=payload)
            response.raise_for_status()

            projects = response.json()
            logger.info(f"Found {len(projects)} projects")
            return projects

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to list projects: {str(e)}")
            return []

    def list_files(self, project_id: str) -> List[Dict[str, Any]]:
        """
        List all files in a project

        Args:
            project_id: Project ID

        Returns:
            List of file dictionaries
        """
        if not self.token:
            if not self.authenticate():
                return []

        try:
            url = f"{self.api_url}/api/rpc/command/get-project-files"
            payload = {'project-id': project_id}

            response = self.session.post(url, json=payload)
            response.raise_for_status()

            files = response.json()
            logger.info(f"Found {len(files)} files in project {project_id}")
            return files

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to list files: {str(e)}")
            return []

    def get_file_data(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        Get complete file data including all pages and objects

        Args:
            file_id: File ID

        Returns:
            File data dictionary or None
        """
        if not self.token:
            if not self.authenticate():
                return None

        try:
            url = f"{self.api_url}/api/rpc/command/get-file"
            payload = {'id': file_id}

            response = self.session.post(url, json=payload)
            response.raise_for_status()

            file_data = response.json()
            logger.info(f"Retrieved file data for {file_id}")
            return file_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get file data: {str(e)}")
            return None

    def get_page_data(self, file_id: str, page_id: str) -> Optional[Dict[str, Any]]:
        """
        Get page data including all objects

        Args:
            file_id: File ID
            page_id: Page ID

        Returns:
            Page data dictionary or None
        """
        if not self.token:
            if not self.authenticate():
                return None

        try:
            url = f"{self.api_url}/api/rpc/command/get-page"
            payload = {
                'file-id': file_id,
                'id': page_id
            }

            response = self.session.post(url, json=payload)
            response.raise_for_status()

            page_data = response.json()
            logger.info(f"Retrieved page data for {page_id}")
            return page_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get page data: {str(e)}")
            return None

    def download_file(self, file_id: str, output_path: str) -> bool:
        """
        Download Penpot file to local storage

        Args:
            file_id: File ID to download
            output_path: Path to save the .penpot file

        Returns:
            bool: True if download successful
        """
        if not self.token:
            if not self.authenticate():
                return False

        try:
            # Export file endpoint
            url = f"{self.api_url}/api/rpc/command/export-binfile"
            payload = {'id': file_id}

            response = self.session.post(url, json=payload, stream=True)
            response.raise_for_status()

            # Save to file
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            logger.info(f"Downloaded file to {output_path}")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download file: {str(e)}")
            return False

    def search_files(self, query: str, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for files by name

        Args:
            query: Search query string
            project_id: Optional project ID to limit search

        Returns:
            List of matching files
        """
        if not self.token:
            if not self.authenticate():
                return []

        try:
            # Get all files (search endpoint may vary by Penpot version)
            if project_id:
                files = self.list_files(project_id)
            else:
                # Get files from all projects
                files = []
                projects = self.list_projects()
                for project in projects:
                    files.extend(self.list_files(project['id']))

            # Filter by query
            matching_files = [
                f for f in files
                if query.lower() in f.get('name', '').lower()
            ]

            logger.info(f"Found {len(matching_files)} files matching '{query}'")
            return matching_files

        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return []

    def get_file_metadata(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        Get file metadata (name, created date, modified date, etc.)

        Args:
            file_id: File ID

        Returns:
            Metadata dictionary or None
        """
        file_data = self.get_file_data(file_id)
        if not file_data:
            return None

        return {
            'id': file_data.get('id'),
            'name': file_data.get('name'),
            'created_at': file_data.get('created-at'),
            'modified_at': file_data.get('modified-at'),
            'version': file_data.get('version'),
            'pages': len(file_data.get('data', {}).get('pages', [])),
            'objects_count': len(file_data.get('data', {}).get('objects', {}))
        }

    def export_to_aldo_format(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert Penpot API data to Aldo Vision format

        Args:
            file_data: Raw Penpot file data from API

        Returns:
            Data in Aldo Vision expected format
        """
        # Transform Penpot API format to match Aldo Vision's expected structure
        return {
            'file_id': file_data.get('id'),
            'file_name': file_data.get('name'),
            'version': file_data.get('version'),
            'pages': file_data.get('data', {}).get('pages', []),
            'objects': file_data.get('data', {}).get('objects', {}),
            'total_frames': len(file_data.get('data', {}).get('pages', [])),
            'metadata': {
                'created_at': file_data.get('created-at'),
                'modified_at': file_data.get('modified-at'),
                'source': 'penpot_api',
                'api_url': self.api_url
            }
        }


def connect_to_penpot(api_url: Optional[str] = None,
                     username: Optional[str] = None,
                     password: Optional[str] = None) -> Optional[PenpotAPIConnector]:
    """
    Helper function to create and authenticate Penpot connection

    Args:
        api_url: Penpot API URL
        username: Penpot username
        password: Penpot password

    Returns:
        Authenticated PenpotAPIConnector or None
    """
    connector = PenpotAPIConnector(api_url, username, password)

    if connector.authenticate():
        return connector
    else:
        logger.error("Failed to connect to Penpot API")
        return None


# Example usage
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Connect to Penpot
    connector = connect_to_penpot()

    if connector:
        # List projects
        projects = connector.list_projects()
        print(f"Found {len(projects)} projects")

        if projects:
            # Get files from first project
            files = connector.list_files(projects[0]['id'])
            print(f"Found {len(files)} files in first project")

            if files:
                # Get file data
                file_data = connector.get_file_data(files[0]['id'])
                if file_data:
                    # Convert to Aldo format
                    aldo_data = connector.export_to_aldo_format(file_data)
                    print(f"Converted file: {aldo_data['file_name']}")
