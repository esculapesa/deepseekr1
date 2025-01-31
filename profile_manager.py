
from typing import List, Dict
import os
import json

class ProfileManager:
    def __init__(self):
        """Initialize profiles with local dictionary and load saved data"""
        self.profiles = {}
        self.current_profile = None
        self.storage_path = "profiles.json"
        self._load_profiles()

    def _load_profiles(self):
        """Load profiles from file"""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                self.profiles = data.get('profiles', {})
                self.current_profile = data.get('current_profile')

    def _save_profiles(self):
        """Save profiles to file"""
        data = {
            'profiles': self.profiles,
            'current_profile': self.current_profile
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f)

    def create_profile(self, name: str):
        """Create a new profile"""
        if name not in self.profiles:
            self.profiles[name] = {"pdfs": {}}  # Changed to store paths
            self.current_profile = name
            self._save_profiles()

    def delete_profile(self, name: str):
        """Delete a profile and its PDFs"""
        if name in self.profiles:
            del self.profiles[name]
            if self.current_profile == name:
                self.current_profile = None
            self._save_profiles()

    def add_pdf_to_profile(self, profile: str, pdf_path: str, pdf_name: str):
        """Add a PDF to a profile"""
        if profile in self.profiles:
            self.profiles[profile]["pdfs"][pdf_name] = pdf_path
            self._save_profiles()

    def get_profile_pdfs(self, profile: str) -> List[str]:
        """Get list of PDFs in a profile"""
        return list(self.profiles.get(profile, {}).get("pdfs", {}).keys())

    def load_pdf_from_profile(self, profile: str, pdf_name: str) -> str:
        """Load a PDF from a profile and return its local path"""
        if profile in self.profiles and pdf_name in self.profiles[profile]["pdfs"]:
            return self.profiles[profile]["pdfs"][pdf_name]
        return None

    def get_all_profiles(self) -> List[str]:
        """Get list of all profiles"""
        return list(self.profiles.keys())
