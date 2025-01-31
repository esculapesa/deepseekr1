from replit.database.database import ObservedDict
from replit import db
from typing import List, Dict
import os

class ProfileManager:
    def __init__(self):
        """Initialize profiles in Replit database"""
        if 'profiles' not in db:
            db['profiles'] = {}
        self.current_profile = None

    def _save_profiles(self):
        """No need to explicitly save with Replit db"""
        pass

    def create_profile(self, name: str):
        """Create a new profile"""
        if name not in db['profiles']:
            db['profiles'][name] = {"pdfs": []}
            self.current_profile = name

    def delete_profile(self, name: str):
        """Delete a profile and its PDFs"""
        if name in db['profiles']:
            # Just remove from database since files are handled separately
            del db['profiles'][name]
            if self.current_profile == name:
                self.current_profile = None

    def add_pdf_to_profile(self, profile: str, pdf_path: str, pdf_name: str):
        """Add a PDF to a profile"""
        if profile in db['profiles']:
            with open(pdf_path, 'rb') as f:
                pdf_content = f.read()
                db[f"pdf_{profile}_{pdf_name}"] = pdf_content
            if pdf_name not in db['profiles'][profile]["pdfs"]:
                db['profiles'][profile]["pdfs"].append(pdf_name)

    def get_profile_pdfs(self, profile: str) -> List[str]:
        """Get list of PDFs in a profile"""
        return db['profiles'].get(profile, {}).get("pdfs", [])

    def load_pdf_from_profile(self, profile: str, pdf_name: str) -> str:
        """Load a PDF from a profile and return its local path"""
        if profile in db['profiles'] and pdf_name in db['profiles'][profile]["pdfs"]:
            pdf_content = db.get(f"pdf_{profile}_{pdf_name}")
            if pdf_content:
                local_path = f"temp_{pdf_name}"
                with open(local_path, 'wb') as f:
                    f.write(pdf_content)
                return local_path
        return None

    def get_all_profiles(self) -> List[str]:
        """Get list of all profiles"""
        return list(db['profiles'].keys())