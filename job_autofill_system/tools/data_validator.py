#!/usr/bin/env python3
"""
Job Autofill System - Data Validator
Validates JSON profile data structure and content
"""

import json
import re
from typing import Dict, List, Any, Tuple
from datetime import datetime
import argparse


class ProfileDataValidator:
    """Validates job profile data structure and content"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        
        # Define required fields for each section
        self.required_fields = {
            'personalInfo': {
                'required': ['firstName', 'lastName', 'email'],
                'optional': ['phone', 'address', 'linkedin', 'website', 'summary']
            },
            'workExperience': {
                'required': ['positions'],
                'position_required': ['company', 'title', 'startDate'],
                'position_optional': ['endDate', 'description', 'location', 'achievements']
            },
            'education': {
                'required': ['schools'],
                'school_required': ['institution', 'degree', 'fieldOfStudy'],
                'school_optional': ['graduationDate', 'gpa', 'location', 'achievements']
            },
            'skills': {
                'required': [],
                'optional': ['technical', 'languages', 'certifications', 'softSkills']
            }
        }
        
        # Validation patterns
        self.patterns = {
            'email': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
            'phone': re.compile(r'^[\+]?[1-9][\d]{0,15}$'),
            'url': re.compile(r'^https?://[^\s/$.?#].[^\s]*$'),
            'date': re.compile(r'^\d{4}-\d{2}-\d{2}$|^present$|^current$', re.IGNORECASE)
        }

    def validate_profile(self, profile_data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        Validate complete profile data
        
        Args:
            profile_data: Dictionary containing profile information
            
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors.clear()
        self.warnings.clear()
        
        if not isinstance(profile_data, dict):
            self.errors.append("Profile data must be a dictionary")
            return False, self.errors, self.warnings
        
        # Validate each section
        self._validate_personal_info(profile_data.get('personalInfo', {}))
        self._validate_work_experience(profile_data.get('workExperience', {}))
        self._validate_education(profile_data.get('education', {}))
        self._validate_skills(profile_data.get('skills', {}))
        
        # Check for unknown sections
        known_sections = {'personalInfo', 'workExperience', 'education', 'skills', 'metadata'}
        unknown_sections = set(profile_data.keys()) - known_sections
        if unknown_sections:
            self.warnings.append(f"Unknown sections found: {', '.join(unknown_sections)}")
        
        return len(self.errors) == 0, self.errors, self.warnings

    def _validate_personal_info(self, personal_info: Dict[str, Any]):
        """Validate personal information section"""
        if not personal_info:
            self.errors.append("Personal information section is required")
            return
        
        # Check required fields
        for field in self.required_fields['personalInfo']['required']:
            if field not in personal_info or not personal_info[field]:
                self.errors.append(f"Personal info: {field} is required")
        
        # Validate email format
        email = personal_info.get('email', '')
        if email and not self.patterns['email'].match(email):
            self.errors.append(f"Personal info: Invalid email format: {email}")
        
        # Validate phone format
        phone = personal_info.get('phone', '')
        if phone:
            # Clean phone number for validation
            clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
            if not self.patterns['phone'].match(clean_phone):
                self.warnings.append(f"Personal info: Phone number format may be invalid: {phone}")
        
        # Validate URLs
        for url_field in ['linkedin', 'website']:
            url = personal_info.get(url_field, '')
            if url and not self.patterns['url'].match(url):
                self.errors.append(f"Personal info: Invalid {url_field} URL format: {url}")
        
        # Validate address structure
        address = personal_info.get('address', {})
        if address and isinstance(address, dict):
            if 'street' in address and not address['street']:
                self.warnings.append("Personal info: Address street is empty")

    def _validate_work_experience(self, work_experience: Dict[str, Any]):
        """Validate work experience section"""
        if not work_experience:
            self.warnings.append("Work experience section is empty")
            return
        
        positions = work_experience.get('positions', [])
        if not positions:
            self.warnings.append("No work positions found")
            return
        
        if not isinstance(positions, list):
            self.errors.append("Work experience positions must be a list")
            return
        
        for i, position in enumerate(positions):
            if not isinstance(position, dict):
                self.errors.append(f"Position {i+1}: Must be a dictionary")
                continue
            
            # Check required fields
            for field in self.required_fields['workExperience']['position_required']:
                if field not in position or not position[field]:
                    self.errors.append(f"Position {i+1}: {field} is required")
            
            # Validate dates
            start_date = position.get('startDate', '')
            end_date = position.get('endDate', '')
            
            if start_date and not self.patterns['date'].match(start_date):
                self.errors.append(f"Position {i+1}: Invalid start date format: {start_date}")
            
            if end_date and not self.patterns['date'].match(end_date):
                self.errors.append(f"Position {i+1}: Invalid end date format: {end_date}")
            
            # Check date logic
            if (start_date and end_date and 
                not end_date.lower() in ['present', 'current'] and
                start_date > end_date):
                self.warnings.append(f"Position {i+1}: Start date is after end date")

    def _validate_education(self, education: Dict[str, Any]):
        """Validate education section"""
        if not education:
            self.warnings.append("Education section is empty")
            return
        
        schools = education.get('schools', [])
        if not schools:
            self.warnings.append("No educational institutions found")
            return
        
        if not isinstance(schools, list):
            self.errors.append("Education schools must be a list")
            return
        
        for i, school in enumerate(schools):
            if not isinstance(school, dict):
                self.errors.append(f"School {i+1}: Must be a dictionary")
                continue
            
            # Check required fields
            for field in self.required_fields['education']['school_required']:
                if field not in school or not school[field]:
                    self.errors.append(f"School {i+1}: {field} is required")
            
            # Validate graduation date
            grad_date = school.get('graduationDate', '')
            if grad_date and not self.patterns['date'].match(grad_date):
                self.errors.append(f"School {i+1}: Invalid graduation date format: {grad_date}")
            
            # Validate GPA
            gpa = school.get('gpa', '')
            if gpa:
                try:
                    gpa_float = float(gpa)
                    if gpa_float < 0 or gpa_float > 4.0:
                        self.warnings.append(f"School {i+1}: GPA {gpa} seems unusual (expected 0-4.0)")
                except ValueError:
                    self.errors.append(f"School {i+1}: Invalid GPA format: {gpa}")

    def _validate_skills(self, skills: Dict[str, Any]):
        """Validate skills section"""
        if not skills:
            self.warnings.append("Skills section is empty")
            return
        
        # Check that skills contain at least one category
        skill_categories = ['technical', 'languages', 'certifications', 'softSkills']
        has_skills = any(skills.get(cat) for cat in skill_categories)
        
        if not has_skills:
            self.warnings.append("No skills found in any category")
        
        # Validate technical skills format
        technical = skills.get('technical', [])
        if technical and not isinstance(technical, list):
            self.errors.append("Technical skills must be a list")
        
        # Validate languages format
        languages = skills.get('languages', [])
        if languages:
            if not isinstance(languages, list):
                self.errors.append("Languages must be a list")
            else:
                for lang in languages:
                    if isinstance(lang, dict):
                        if 'language' not in lang:
                            self.warnings.append("Language entry missing 'language' field")

    def validate_file(self, file_path: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate profile data from JSON file
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self.validate_profile(data)
        except FileNotFoundError:
            return False, [f"File not found: {file_path}"], []
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON format: {e}"], []
        except Exception as e:
            return False, [f"Error reading file: {e}"], []

    def generate_report(self, is_valid: bool, errors: List[str], warnings: List[str]) -> str:
        """Generate a validation report"""
        report = []
        report.append("=" * 50)
        report.append("PROFILE DATA VALIDATION REPORT")
        report.append("=" * 50)
        
        if is_valid:
            report.append("✅ VALIDATION PASSED")
        else:
            report.append("❌ VALIDATION FAILED")
        
        if errors:
            report.append(f"\n🚨 ERRORS ({len(errors)}):")
            for i, error in enumerate(errors, 1):
                report.append(f"  {i}. {error}")
        
        if warnings:
            report.append(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for i, warning in enumerate(warnings, 1):
                report.append(f"  {i}. {warning}")
        
        if not errors and not warnings:
            report.append("\n🎉 No issues found! Profile data is perfect.")
        
        report.append("\n" + "=" * 50)
        return "\n".join(report)


def main():
    """Command-line interface for the validator"""
    parser = argparse.ArgumentParser(description='Validate job profile JSON data')
    parser.add_argument('file', help='Path to JSON profile file')
    parser.add_argument('--quiet', '-q', action='store_true', help='Only show errors and warnings')
    parser.add_argument('--json-output', action='store_true', help='Output results in JSON format')
    
    args = parser.parse_args()
    
    validator = ProfileDataValidator()
    is_valid, errors, warnings = validator.validate_file(args.file)
    
    if args.json_output:
        result = {
            'valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'file': args.file
        }
        print(json.dumps(result, indent=2))
    else:
        if not args.quiet:
            print(validator.generate_report(is_valid, errors, warnings))
        else:
            if errors:
                print("ERRORS:")
                for error in errors:
                    print(f"  {error}")
            if warnings:
                print("WARNINGS:")
                for warning in warnings:
                    print(f"  {warning}")
    
    # Exit with error code if validation failed
    exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()