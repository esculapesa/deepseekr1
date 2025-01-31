from typing import List, Dict
import os

class ProfileManager:
    def __init__(self):
        """Initialize profiles with local dictionary"""
        self.profiles = {}
        self.current_profile = None

    def _save_profiles(self):
        """No longer needed with local dictionary storage"""
        pass

    def create_profile(self, name: str):
        """Create a new profile"""
        if name not in self.profiles:
            self.profiles[name] = {"pdfs": []}
            self.current_profile = name

    def delete_profile(self, name: str):
        """Delete a profile and its PDFs"""
        if name in self.profiles:
            del self.profiles[name]
            if self.current_profile == name:
                self.current_profile = None

    def add_pdf_to_profile(self, profile: str, pdf_path: str, pdf_name: str):
        """Add a PDF to a profile"""
        if profile in self.profiles:
            if pdf_name not in self.profiles[profile]["pdfs"]:
                self.profiles[profile]["pdfs"].append(pdf_name)

    def get_profile_pdfs(self, profile: str) -> List[str]:
        """Get list of PDFs in a profile"""
        return self.profiles.get(profile, {}).get("pdfs", [])

    def load_pdf_from_profile(self, profile: str, pdf_name: str) -> str:
        """Load a PDF from a profile and return its local path"""
        if profile in self.profiles and pdf_name in self.profiles[profile]["pdfs"]:
            return pdf_path #Note: This line assumes pdf_path is available in the scope.  It might need adjustment based on how pdf_path is intended to be used.
        return None

    def get_all_profiles(self) -> List[str]:
        """Get list of all profiles"""
        return list(self.profiles.keys())