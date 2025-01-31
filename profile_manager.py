
from replit.object_storage import Client
import json
from typing import List, Dict
import os

class ProfileManager:
    def __init__(self):
        self.client = Client()
        self.current_profile = None
        self._load_profiles()

    def _load_profiles(self):
        """Load or initialize profiles metadata"""
        try:
            profiles_data = self.client.download_from_text("profiles.json")
            self.profiles = json.loads(profiles_data)
        except:
            self.profiles = {}
            self._save_profiles()

    def _save_profiles(self):
        """Save profiles metadata"""
        self.client.upload_from_text("profiles.json", json.dumps(self.profiles))

    def create_profile(self, name: str):
        """Create a new profile"""
        if name not in self.profiles:
            self.profiles[name] = {"pdfs": []}
            self._save_profiles()
            self.current_profile = name

    def delete_profile(self, name: str):
        """Delete a profile and its PDFs"""
        if name in self.profiles:
            for pdf in self.profiles[name]["pdfs"]:
                try:
                    self.client.delete(f"{name}/{pdf}")
                except:
                    pass
            del self.profiles[name]
            self._save_profiles()
            if self.current_profile == name:
                self.current_profile = None

    def add_pdf_to_profile(self, profile: str, pdf_path: str, pdf_name: str):
        """Add a PDF to a profile"""
        if profile in self.profiles:
            object_path = f"{profile}/{pdf_name}"
            with open(pdf_path, 'rb') as f:
                self.client.upload_from_file(object_path, f)
            if pdf_name not in self.profiles[profile]["pdfs"]:
                self.profiles[profile]["pdfs"].append(pdf_name)
                self._save_profiles()

    def get_profile_pdfs(self, profile: str) -> List[str]:
        """Get list of PDFs in a profile"""
        return self.profiles.get(profile, {}).get("pdfs", [])

    def load_pdf_from_profile(self, profile: str, pdf_name: str) -> str:
        """Load a PDF from a profile and return its local path"""
        if profile in self.profiles and pdf_name in self.profiles[profile]["pdfs"]:
            local_path = f"temp_{pdf_name}"
            with open(local_path, 'wb') as f:
                self.client.download_to_file(f"{profile}/{pdf_name}", f)
            return local_path
        return None

    def get_all_profiles(self) -> List[str]:
        """Get list of all profiles"""
        return list(self.profiles.keys())
