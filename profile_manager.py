from typing import List
import os

class ProfileManager:
    def __init__(self):
        """Initialize profiles from knowledge directory"""
        self.base_dir = "knowledge"
        self.current_profile = None
        os.makedirs(self.base_dir, exist_ok=True)

    def get_all_profiles(self) -> List[str]:
        """Get list of all profiles (folders)"""
        if not os.path.exists(self.base_dir):
            return []
        return [d for d in os.listdir(self.base_dir) 
                if os.path.isdir(os.path.join(self.base_dir, d))]

    def create_profile(self, name: str):
        """Create a new profile directory"""
        profile_path = os.path.join(self.base_dir, name)
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
            self.current_profile = name

    def get_profile_pdfs(self, profile: str) -> List[str]:
        """Get list of PDFs in a profile directory"""
        profile_path = os.path.join(self.base_dir, profile)
        if not os.path.exists(profile_path):
            return []
        return [f for f in os.listdir(profile_path) 
                if f.lower().endswith('.pdf')]

    def get_pdf_path(self, profile: str, pdf_name: str) -> str:
        """Get full path for a PDF in a profile"""
        return os.path.join(self.base_dir, profile, pdf_name)

    def load_profile_pdfs(self, profile: str) -> List[str]:
        """Get full paths of all PDFs in a profile"""
        profile_path = os.path.join(self.base_dir, profile)
        if not os.path.exists(profile_path):
            return []
        return [os.path.join(profile_path, f) 
                for f in os.listdir(profile_path) 
                if f.lower().endswith('.pdf')]

    def add_pdf_to_profile(self, profile: str, pdf_path: str, pdf_name: str):
        """Add a PDF to a profile"""
        profile_path = os.path.join(self.base_dir, profile)
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
        destination_path = os.path.join(profile_path, pdf_name)
        
        # Copy the PDF file
        with open(pdf_path, 'rb') as src:
            pdf_content = src.read()
        with open(destination_path, 'wb') as dst:
            dst.write(pdf_content)

    def delete_profile(self, name: str):
        """Delete a profile directory and its contents"""
        profile_path = os.path.join(self.base_dir, name)
        if os.path.exists(profile_path):
            import shutil
            shutil.rmtree(profile_path)
            if self.current_profile == name:
                self.current_profile = None

    def load_pdf_from_profile(self, profile: str, pdf_name: str) -> str:
        """Load a PDF from a profile and return its local path"""
        return self.get_pdf_path(profile, pdf_name)