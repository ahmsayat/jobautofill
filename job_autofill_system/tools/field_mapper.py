#!/usr/bin/env python3
"""
Job Autofill System - Field Mapper
Maps form fields to profile data and handles field detection
"""

import json
import re
import argparse
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
from difflib import SequenceMatcher


class FormFieldMapper:
    """Maps job application form fields to profile data"""
    
    def __init__(self):
        self.field_mappings = {
            # Personal Information Mappings
            'firstName': [
                'first_name', 'firstname', 'fname', 'given_name', 'forename',
                'first-name', 'name_first', 'applicant_first_name', 'user_firstname',
                'personal_first_name', 'candidate_first_name'
            ],
            'lastName': [
                'last_name', 'lastname', 'lname', 'surname', 'family_name',
                'last-name', 'name_last', 'applicant_last_name', 'user_lastname',
                'personal_last_name', 'candidate_last_name'
            ],
            'fullName': [
                'full_name', 'fullname', 'name', 'complete_name', 'applicant_name',
                'full-name', 'user_name', 'candidate_name', 'person_name'
            ],
            'email': [
                'email', 'email_address', 'e_mail', 'emailaddress', 'mail',
                'e-mail', 'contact_email', 'user_email', 'applicant_email',
                'personal_email', 'work_email', 'email_id'
            ],
            'phone': [
                'phone', 'phone_number', 'phonenumber', 'telephone', 'tel',
                'mobile', 'cell', 'contact_number', 'phone_no', 'tel_no',
                'mobile_number', 'cellphone', 'contact_phone'
            ],
            
            # Address Mappings
            'street': [
                'street', 'address', 'street_address', 'address_line_1',
                'address1', 'addr1', 'street_1', 'home_address', 'residential_address'
            ],
            'street2': [
                'street_2', 'address_line_2', 'address2', 'addr2', 'apartment',
                'apt', 'suite', 'unit', 'line2', 'address_2'
            ],
            'city': [
                'city', 'town', 'locality', 'municipality', 'address_city',
                'city_name', 'home_city', 'residence_city'
            ],
            'state': [
                'state', 'province', 'region', 'state_province', 'address_state',
                'state_name', 'prov', 'st'
            ],
            'zipCode': [
                'zip', 'zip_code', 'zipcode', 'postal_code', 'postalcode',
                'postcode', 'zip_postal', 'address_zip'
            ],
            'country': [
                'country', 'nation', 'country_name', 'address_country',
                'home_country', 'nationality_country'
            ],
            
            # Professional Information
            'linkedin': [
                'linkedin', 'linkedin_url', 'linkedin_profile', 'linkedin_link',
                'social_linkedin', 'li_url', 'linkedin_username'
            ],
            'website': [
                'website', 'personal_website', 'homepage', 'web_site',
                'portfolio_url', 'personal_url', 'website_url'
            ],
            'github': [
                'github', 'github_url', 'github_profile', 'github_username',
                'git_hub', 'github_link', 'code_repository'
            ],
            
            # Work Experience
            'currentCompany': [
                'current_company', 'employer', 'company', 'current_employer',
                'organization', 'workplace', 'company_name', 'current_job_company'
            ],
            'currentTitle': [
                'current_title', 'job_title', 'position', 'current_position',
                'title', 'role', 'current_role', 'job_position', 'occupation'
            ],
            'yearsExperience': [
                'years_experience', 'experience_years', 'total_experience',
                'work_experience', 'professional_experience', 'exp_years'
            ],
            'salary': [
                'salary', 'current_salary', 'expected_salary', 'salary_expectation',
                'compensation', 'wage', 'pay', 'salary_range', 'annual_salary'
            ],
            
            # Education
            'university': [
                'university', 'college', 'school', 'institution', 'alma_mater',
                'education_institution', 'university_name', 'college_name'
            ],
            'degree': [
                'degree', 'education_level', 'qualification', 'diploma',
                'certificate', 'academic_degree', 'highest_degree'
            ],
            'major': [
                'major', 'field_of_study', 'study_field', 'specialization',
                'concentration', 'subject', 'area_of_study', 'academic_major'
            ],
            'gpa': [
                'gpa', 'grade_point_average', 'grades', 'academic_performance',
                'cgpa', 'cumulative_gpa'
            ],
            'graduationYear': [
                'graduation_year', 'grad_year', 'year_graduated', 'completion_year',
                'graduation_date', 'degree_year'
            ],
            
            # Skills and Certifications
            'skills': [
                'skills', 'technical_skills', 'competencies', 'abilities',
                'skill_set', 'expertise', 'proficiencies', 'talents'
            ],
            'certifications': [
                'certifications', 'certificates', 'credentials', 'licenses',
                'professional_certifications', 'qualifications'
            ],
            'languages': [
                'languages', 'language_skills', 'spoken_languages', 'linguistics',
                'foreign_languages', 'multilingual'
            ],
            
            # Additional Fields
            'summary': [
                'summary', 'profile_summary', 'about', 'bio', 'biography',
                'professional_summary', 'overview', 'introduction', 'description'
            ],
            'objective': [
                'objective', 'career_objective', 'goal', 'career_goal',
                'professional_objective', 'job_objective'
            ],
            'coverLetter': [
                'cover_letter', 'covering_letter', 'motivation_letter',
                'personal_statement', 'introduction_letter', 'application_letter'
            ],
            'references': [
                'references', 'referees', 'recommendations', 'reference_contacts',
                'professional_references', 'character_references'
            ],
            'availability': [
                'availability', 'start_date', 'available_from', 'notice_period',
                'when_available', 'earliest_start', 'join_date'
            ],
            'workAuthorization': [
                'work_authorization', 'visa_status', 'eligibility', 'authorized_to_work',
                'work_permit', 'employment_eligibility', 'legal_status'
            ],
            'willingToRelocate': [
                'willing_to_relocate', 'relocate', 'relocation', 'move',
                'open_to_relocation', 'relocation_preference'
            ],
            'travelWillingness': [
                'travel', 'willing_to_travel', 'travel_percentage', 'business_travel',
                'travel_requirements', 'mobility'
            ]
        }
        
        self.field_patterns = {
            'email': re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'),
            'phone': re.compile(r'^[\+]?[1-9]?[\d\s\-\(\)\.]{7,15}$'),
            'url': re.compile(r'^https?://'),
            'zipCode': re.compile(r'^\d{5}(-\d{4})?$|^[A-Z]\d[A-Z]\s?\d[A-Z]\d$'),
            'year': re.compile(r'^\d{4}$'),
            'gpa': re.compile(r'^\d\.\d{1,2}$|^[0-4]\.\d{1,2}$'),
            'salary': re.compile(r'^\$?\d{1,3}(,\d{3})*(\.\d{2})?$')
        }

    def map_field_to_profile(self, field_name: str, field_attributes: Dict[str, Any] = None) -> Optional[str]:
        """
        Map a form field to a profile data field
        
        Args:
            field_name: The name/id/class of the form field
            field_attributes: Additional attributes like placeholder, label, etc.
            
        Returns:
            The corresponding profile field name or None if no match
        """
        field_name_clean = self._clean_field_name(field_name)
        
        # Direct mapping check
        for profile_field, variations in self.field_mappings.items():
            if field_name_clean in variations:
                return profile_field
        
        # Fuzzy matching for close matches
        best_match = self._fuzzy_match(field_name_clean)
        if best_match:
            return best_match
        
        # Check attributes for additional context
        if field_attributes:
            attr_match = self._match_by_attributes(field_attributes)
            if attr_match:
                return attr_match
        
        return None

    def _clean_field_name(self, field_name: str) -> str:
        """Clean and normalize field names"""
        if not field_name:
            return ""
        
        # Convert to lowercase
        cleaned = field_name.lower()
        
        # Remove common prefixes/suffixes
        prefixes = ['input_', 'field_', 'form_', 'user_', 'applicant_', 'candidate_']
        suffixes = ['_field', '_input', '_text', '_area', '_box']
        
        for prefix in prefixes:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):]
                break
        
        for suffix in suffixes:
            if cleaned.endswith(suffix):
                cleaned = cleaned[:-len(suffix)]
                break
        
        # Replace common separators with underscores
        cleaned = re.sub(r'[-\s\.]+', '_', cleaned)
        
        # Remove special characters except underscores
        cleaned = re.sub(r'[^\w]', '_', cleaned)
        
        # Remove multiple consecutive underscores
        cleaned = re.sub(r'_+', '_', cleaned)
        
        # Remove leading/trailing underscores
        cleaned = cleaned.strip('_')
        
        return cleaned

    def _fuzzy_match(self, field_name: str, threshold: float = 0.7) -> Optional[str]:
        """Perform fuzzy matching against known field variations"""
        best_match = None
        best_ratio = 0
        
        for profile_field, variations in self.field_mappings.items():
            for variation in variations:
                ratio = SequenceMatcher(None, field_name, variation).ratio()
                if ratio > best_ratio and ratio >= threshold:
                    best_ratio = ratio
                    best_match = profile_field
        
        return best_match

    def _match_by_attributes(self, attributes: Dict[str, Any]) -> Optional[str]:
        """Match field based on attributes like placeholder, label, etc."""
        for attr_name, attr_value in attributes.items():
            if isinstance(attr_value, str):
                cleaned_value = self._clean_field_name(attr_value)
                match = self.map_field_to_profile(cleaned_value)
                if match:
                    return match
        return None

    def analyze_form_fields(self, form_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze a list of form fields and suggest mappings
        
        Args:
            form_data: List of dictionaries containing field information
            
        Returns:
            Analysis results with suggested mappings
        """
        results = {
            'mapped_fields': {},
            'unmapped_fields': [],
            'confidence_scores': {},
            'suggestions': [],
            'statistics': defaultdict(int)
        }
        
        for field in form_data:
            field_name = field.get('name', field.get('id', ''))
            field_type = field.get('type', 'text')
            field_attributes = {
                'placeholder': field.get('placeholder', ''),
                'label': field.get('label', ''),
                'class': field.get('class', ''),
                'title': field.get('title', '')
            }
            
            # Attempt to map the field
            mapped_field = self.map_field_to_profile(field_name, field_attributes)
            
            if mapped_field:
                results['mapped_fields'][field_name] = mapped_field
                
                # Calculate confidence score
                confidence = self._calculate_confidence(field_name, mapped_field, field_attributes)
                results['confidence_scores'][field_name] = confidence
                
                results['statistics']['mapped'] += 1
            else:
                results['unmapped_fields'].append({
                    'name': field_name,
                    'type': field_type,
                    'attributes': field_attributes
                })
                results['statistics']['unmapped'] += 1
            
            results['statistics']['total'] += 1
        
        # Generate suggestions for improvements
        results['suggestions'] = self._generate_suggestions(results)
        
        return results

    def _calculate_confidence(self, field_name: str, mapped_field: str, 
                            attributes: Dict[str, Any]) -> float:
        """Calculate confidence score for a field mapping"""
        confidence = 0.0
        
        # Direct match gets highest confidence
        field_name_clean = self._clean_field_name(field_name)
        if field_name_clean in self.field_mappings.get(mapped_field, []):
            confidence += 0.8
        else:
            # Fuzzy match gets lower confidence
            best_ratio = 0
            for variation in self.field_mappings.get(mapped_field, []):
                ratio = SequenceMatcher(None, field_name_clean, variation).ratio()
                best_ratio = max(best_ratio, ratio)
            confidence += best_ratio * 0.6
        
        # Bonus for attribute matches
        for attr_value in attributes.values():
            if isinstance(attr_value, str) and attr_value:
                attr_clean = self._clean_field_name(attr_value)
                if attr_clean in self.field_mappings.get(mapped_field, []):
                    confidence += 0.2
                    break
        
        return min(confidence, 1.0)

    def _generate_suggestions(self, results: Dict[str, Any]) -> List[str]:
        """Generate suggestions for improving field mappings"""
        suggestions = []
        
        unmapped_count = results['statistics']['unmapped']
        total_count = results['statistics']['total']
        
        if unmapped_count > 0:
            suggestions.append(f"Found {unmapped_count} unmapped fields out of {total_count} total")
        
        # Low confidence mappings
        low_confidence = [
            field for field, confidence in results['confidence_scores'].items()
            if confidence < 0.7
        ]
        
        if low_confidence:
            suggestions.append(f"Review {len(low_confidence)} mappings with low confidence: {', '.join(low_confidence[:3])}")
        
        # Common unmapped field patterns
        unmapped_names = [field['name'] for field in results['unmapped_fields']]
        common_patterns = self._find_common_patterns(unmapped_names)
        
        if common_patterns:
            suggestions.append(f"Consider adding mappings for common patterns: {', '.join(common_patterns[:3])}")
        
        return suggestions

    def _find_common_patterns(self, field_names: List[str]) -> List[str]:
        """Find common patterns in unmapped field names"""
        patterns = defaultdict(int)
        
        for name in field_names:
            # Extract potential keywords
            words = re.findall(r'\w+', name.lower())
            for word in words:
                if len(word) > 2:  # Ignore very short words
                    patterns[word] += 1
        
        # Return patterns that appear more than once
        return [pattern for pattern, count in patterns.items() if count > 1]

    def create_custom_mapping(self, field_name: str, profile_field: str) -> bool:
        """
        Create a custom mapping for a field
        
        Args:
            field_name: The form field name
            profile_field: The profile field to map to
            
        Returns:
            True if mapping was created successfully
        """
        field_name_clean = self._clean_field_name(field_name)
        
        if profile_field in self.field_mappings:
            if field_name_clean not in self.field_mappings[profile_field]:
                self.field_mappings[profile_field].append(field_name_clean)
                return True
        else:
            self.field_mappings[profile_field] = [field_name_clean]
            return True
        
        return False

    def export_mappings(self, filename: str):
        """Export current field mappings to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.field_mappings, f, indent=2, ensure_ascii=False)

    def import_mappings(self, filename: str):
        """Import field mappings from JSON file"""
        with open(filename, 'r', encoding='utf-8') as f:
            imported_mappings = json.load(f)
            
        # Merge with existing mappings
        for profile_field, variations in imported_mappings.items():
            if profile_field in self.field_mappings:
                # Add new variations that don't exist
                for variation in variations:
                    if variation not in self.field_mappings[profile_field]:
                        self.field_mappings[profile_field].append(variation)
            else:
                self.field_mappings[profile_field] = variations

    def validate_field_value(self, field_name: str, value: str) -> Tuple[bool, str]:
        """
        Validate a field value against expected patterns
        
        Args:
            field_name: The profile field name
            value: The value to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not value or not value.strip():
            return True, ""  # Empty values are generally acceptable
        
        value = value.strip()
        
        # Email validation
        if field_name == 'email':
            if not self.field_patterns['email'].match(value):
                return False, "Invalid email format"
        
        # Phone validation
        elif field_name == 'phone':
            if not self.field_patterns['phone'].match(value):
                return False, "Invalid phone number format"
        
        # URL validation (for linkedin, website, github)
        elif field_name in ['linkedin', 'website', 'github']:
            if not self.field_patterns['url'].match(value):
                return False, "Invalid URL format"
        
        # ZIP code validation
        elif field_name == 'zipCode':
            if not self.field_patterns['zipCode'].match(value):
                return False, "Invalid ZIP/postal code format"
        
        # Year validation
        elif field_name in ['graduationYear', 'startYear', 'endYear']:
            if not self.field_patterns['year'].match(value):
                return False, "Invalid year format (should be 4 digits)"
        
        # GPA validation
        elif field_name == 'gpa':
            if not self.field_patterns['gpa'].match(value):
                return False, "Invalid GPA format (should be like 3.75)"
        
        return True, ""


def main():
    """Command-line interface for the field mapper"""
    parser = argparse.ArgumentParser(description='Map form fields to profile data')
    parser.add_argument('--analyze', '-a', help='Analyze form fields from JSON file')
    parser.add_argument('--map', '-m', nargs=2, metavar=('FIELD', 'PROFILE'),
                       help='Create custom mapping: field_name profile_field')
    parser.add_argument('--export', '-e', help='Export mappings to JSON file')
    parser.add_argument('--import', '-i', dest='import_file', help='Import mappings from JSON file')
    parser.add_argument('--validate', '-v', nargs=2, metavar=('FIELD', 'VALUE'),
                       help='Validate a field value')
    parser.add_argument('--test', '-t', help='Test mapping for a field name')
    
    args = parser.parse_args()
    
    mapper = FormFieldMapper()
    
    if args.analyze:
        # Analyze form fields
        with open(args.analyze, 'r', encoding='utf-8') as f:
            form_data = json.load(f)
        
        results = mapper.analyze_form_fields(form_data)
        
        print("=== Field Mapping Analysis ===")
        print(f"Total fields: {results['statistics']['total']}")
        print(f"Mapped fields: {results['statistics']['mapped']}")
        print(f"Unmapped fields: {results['statistics']['unmapped']}")
        print()
        
        if results['mapped_fields']:
            print("Mapped Fields:")
            for field, profile in results['mapped_fields'].items():
                confidence = results['confidence_scores'].get(field, 0)
                print(f"  {field} -> {profile} (confidence: {confidence:.2f})")
            print()
        
        if results['unmapped_fields']:
            print("Unmapped Fields:")
            for field in results['unmapped_fields']:
                print(f"  {field['name']} (type: {field['type']})")
            print()
        
        if results['suggestions']:
            print("Suggestions:")
            for suggestion in results['suggestions']:
                print(f"  - {suggestion}")
    
    elif args.map:
        # Create custom mapping
        field_name, profile_field = args.map
        success = mapper.create_custom_mapping(field_name, profile_field)
        if success:
            print(f"Created mapping: {field_name} -> {profile_field}")
        else:
            print(f"Mapping already exists: {field_name} -> {profile_field}")
    
    elif args.export:
        # Export mappings
        mapper.export_mappings(args.export)
        print(f"Mappings exported to: {args.export}")
    
    elif args.import_file:
        # Import mappings
        mapper.import_mappings(args.import_file)
        print(f"Mappings imported from: {args.import_file}")
    
    elif args.validate:
        # Validate field value
        field_name, value = args.validate
        is_valid, error = mapper.validate_field_value(field_name, value)
        if is_valid:
            print(f"✓ Value '{value}' is valid for field '{field_name}'")
        else:
            print(f"✗ Value '{value}' is invalid for field '{field_name}': {error}")
    
    elif args.test:
        # Test field mapping
        result = mapper.map_field_to_profile(args.test)
        if result:
            print(f"Field '{args.test}' maps to: {result}")
        else:
            print(f"No mapping found for field: {args.test}")
    
    else:
        print("No action specified. Use --help for available options.")


if __name__ == '__main__':
    main()