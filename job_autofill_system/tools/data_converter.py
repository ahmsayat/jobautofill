#!/usr/bin/env python3
"""
Job Autofill System - Data Converter
Converts between different data formats and standardizes profile data
"""

import json
import csv
import xml.etree.ElementTree as ET
import yaml
import argparse
from typing import Dict, List, Any, Optional
from datetime import datetime
import re


class ProfileDataConverter:
    """Converts profile data between different formats"""
    
    def __init__(self):
        self.supported_formats = ['json', 'csv', 'xml', 'yaml', 'txt']
        self.date_formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%Y/%m/%d',
            '%B %Y',
            '%b %Y',
            '%Y'
        ]

    def convert_format(self, input_file: str, output_file: str, 
                      input_format: str = None, output_format: str = None) -> bool:
        """
        Convert profile data from one format to another
        
        Args:
            input_file: Path to input file
            output_file: Path to output file
            input_format: Input format (auto-detected if None)
            output_format: Output format (auto-detected if None)
            
        Returns:
            True if conversion successful
        """
        # Auto-detect formats from file extensions
        if not input_format:
            input_format = self._detect_format(input_file)
        if not output_format:
            output_format = self._detect_format(output_file)
        
        if not input_format or not output_format:
            raise ValueError("Could not determine file formats")
        
        # Load data from input file
        data = self._load_data(input_file, input_format)
        
        # Convert and save to output file
        return self._save_data(data, output_file, output_format)

    def _detect_format(self, filename: str) -> Optional[str]:
        """Detect file format from extension"""
        extension = filename.lower().split('.')[-1]
        return extension if extension in self.supported_formats else None

    def _load_data(self, filename: str, format_type: str) -> Dict[str, Any]:
        """Load data from file based on format"""
        if format_type == 'json':
            return self._load_json(filename)
        elif format_type == 'csv':
            return self._load_csv(filename)
        elif format_type == 'xml':
            return self._load_xml(filename)
        elif format_type == 'yaml':
            return self._load_yaml(filename)
        elif format_type == 'txt':
            return self._load_txt(filename)
        else:
            raise ValueError(f"Unsupported format: {format_type}")

    def _save_data(self, data: Dict[str, Any], filename: str, format_type: str) -> bool:
        """Save data to file based on format"""
        try:
            if format_type == 'json':
                return self._save_json(data, filename)
            elif format_type == 'csv':
                return self._save_csv(data, filename)
            elif format_type == 'xml':
                return self._save_xml(data, filename)
            elif format_type == 'yaml':
                return self._save_yaml(data, filename)
            elif format_type == 'txt':
                return self._save_txt(data, filename)
            else:
                raise ValueError(f"Unsupported format: {format_type}")
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def _load_json(self, filename: str) -> Dict[str, Any]:
        """Load JSON data"""
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_json(self, data: Dict[str, Any], filename: str) -> bool:
        """Save JSON data"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True

    def _load_csv(self, filename: str) -> Dict[str, Any]:
        """Load CSV data and convert to profile format"""
        profile_data = {
            'personalInfo': {},
            'workExperience': {'positions': []},
            'education': {'schools': []},
            'skills': {'technical': [], 'certifications': []}
        }
        
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Determine row type based on content
                if any(key in row for key in ['firstName', 'lastName', 'email']):
                    # Personal info row
                    for key, value in row.items():
                        if value and key in ['firstName', 'lastName', 'email', 'phone']:
                            profile_data['personalInfo'][key] = value
                
                elif any(key in row for key in ['company', 'title', 'position']):
                    # Work experience row
                    position = {}
                    for key, value in row.items():
                        if value and key in ['company', 'title', 'startDate', 'endDate', 'description']:
                            position[key] = value
                    if position:
                        profile_data['workExperience']['positions'].append(position)
                
                elif any(key in row for key in ['institution', 'degree', 'university']):
                    # Education row
                    school = {}
                    for key, value in row.items():
                        if value and key in ['institution', 'degree', 'fieldOfStudy', 'graduationDate']:
                            school[key] = value
                    if school:
                        profile_data['education']['schools'].append(school)
        
        return profile_data

    def _save_csv(self, data: Dict[str, Any], filename: str) -> bool:
        """Save data as CSV"""
        rows = []
        
        # Personal info
        if 'personalInfo' in data:
            personal = data['personalInfo']
            personal['type'] = 'personal'
            rows.append(personal)
        
        # Work experience
        if 'workExperience' in data and 'positions' in data['workExperience']:
            for position in data['workExperience']['positions']:
                pos = position.copy()
                pos['type'] = 'work'
                rows.append(pos)
        
        # Education
        if 'education' in data and 'schools' in data['education']:
            for school in data['education']['schools']:
                edu = school.copy()
                edu['type'] = 'education'
                rows.append(edu)
        
        if not rows:
            return False
        
        # Get all unique field names
        fieldnames = set()
        for row in rows:
            fieldnames.update(row.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        return True

    def _load_xml(self, filename: str) -> Dict[str, Any]:
        """Load XML data"""
        tree = ET.parse(filename)
        root = tree.getroot()
        
        return self._xml_to_dict(root)

    def _xml_to_dict(self, element) -> Dict[str, Any]:
        """Convert XML element to dictionary"""
        result = {}
        
        # Handle attributes
        if element.attrib:
            result.update(element.attrib)
        
        # Handle children
        children = list(element)
        if children:
            child_dict = {}
            for child in children:
                child_data = self._xml_to_dict(child)
                if child.tag in child_dict:
                    # Multiple children with same tag - convert to list
                    if not isinstance(child_dict[child.tag], list):
                        child_dict[child.tag] = [child_dict[child.tag]]
                    child_dict[child.tag].append(child_data)
                else:
                    child_dict[child.tag] = child_data
            result.update(child_dict)
        elif element.text and element.text.strip():
            # Leaf node with text
            return element.text.strip()
        
        return result

    def _save_xml(self, data: Dict[str, Any], filename: str) -> bool:
        """Save data as XML"""
        root = ET.Element('profile')
        self._dict_to_xml(data, root)
        
        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        return True

    def _dict_to_xml(self, data: Any, parent: ET.Element):
        """Convert dictionary to XML elements"""
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(parent, str(key))
                self._dict_to_xml(value, child)
        elif isinstance(data, list):
            for item in data:
                item_elem = ET.SubElement(parent, 'item')
                self._dict_to_xml(item, item_elem)
        else:
            parent.text = str(data) if data is not None else ''

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML data"""
        try:
            import yaml
            with open(filename, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except ImportError:
            raise ImportError("PyYAML library required for YAML support")

    def _save_yaml(self, data: Dict[str, Any], filename: str) -> bool:
        """Save data as YAML"""
        try:
            import yaml
            with open(filename, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            return True
        except ImportError:
            raise ImportError("PyYAML library required for YAML support")

    def _load_txt(self, filename: str) -> Dict[str, Any]:
        """Load structured text data"""
        profile_data = {
            'personalInfo': {},
            'workExperience': {'positions': []},
            'education': {'schools': []},
            'skills': {'technical': []}
        }
        
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse sections
        sections = self._parse_text_sections(content)
        
        for section_name, section_content in sections.items():
            if 'personal' in section_name.lower():
                profile_data['personalInfo'].update(self._parse_personal_section(section_content))
            elif 'work' in section_name.lower() or 'experience' in section_name.lower():
                profile_data['workExperience']['positions'].extend(
                    self._parse_work_section(section_content)
                )
            elif 'education' in section_name.lower():
                profile_data['education']['schools'].extend(
                    self._parse_education_section(section_content)
                )
            elif 'skill' in section_name.lower():
                profile_data['skills']['technical'].extend(
                    self._parse_skills_section(section_content)
                )
        
        return profile_data

    def _parse_text_sections(self, content: str) -> Dict[str, str]:
        """Parse text content into sections"""
        sections = {}
        current_section = 'general'
        current_content = []
        
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Check if line is a section header
            if self._is_section_header(line):
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = line.strip(':').strip('#').strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections

    def _is_section_header(self, line: str) -> bool:
        """Check if line is a section header"""
        return (line.startswith('#') or 
                line.endswith(':') or 
                line.isupper() and len(line) > 3)

    def _parse_personal_section(self, content: str) -> Dict[str, str]:
        """Parse personal information from text"""
        personal = {}
        
        # Email pattern
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
        if email_match:
            personal['email'] = email_match.group()
        
        # Phone pattern
        phone_match = re.search(r'[\+]?[1-9]?[\d\s\-\(\)\.]{7,15}', content)
        if phone_match:
            personal['phone'] = phone_match.group().strip()
        
        # Name extraction (simple heuristic)
        lines = content.split('\n')
        for line in lines:
            if 'name' in line.lower():
                name_part = line.split(':')[-1].strip()
                if ' ' in name_part:
                    parts = name_part.split()
                    personal['firstName'] = parts[0]
                    personal['lastName'] = ' '.join(parts[1:])
        
        return personal

    def _parse_work_section(self, content: str) -> List[Dict[str, str]]:
        """Parse work experience from text"""
        positions = []
        
        # Split by job entries (simple heuristic)
        job_blocks = re.split(r'\n\s*\n', content)
        
        for block in job_blocks:
            if block.strip():
                position = {}
                lines = block.split('\n')
                
                # First line often contains company and title
                if lines:
                    first_line = lines[0].strip()
                    if ',' in first_line:
                        parts = first_line.split(',')
                        position['title'] = parts[0].strip()
                        position['company'] = parts[1].strip()
                    else:
                        position['company'] = first_line
                
                # Look for dates
                date_pattern = r'\b(19|20)\d{2}\b'
                dates = re.findall(date_pattern, block)
                if len(dates) >= 2:
                    position['startDate'] = dates[0]
                    position['endDate'] = dates[1]
                elif len(dates) == 1:
                    position['startDate'] = dates[0]
                    position['endDate'] = 'present'
                
                # Description is remaining text
                if len(lines) > 1:
                    position['description'] = '\n'.join(lines[1:]).strip()
                
                if position:
                    positions.append(position)
        
        return positions

    def _parse_education_section(self, content: str) -> List[Dict[str, str]]:
        """Parse education from text"""
        schools = []
        
        # Split by school entries
        school_blocks = re.split(r'\n\s*\n', content)
        
        for block in school_blocks:
            if block.strip():
                school = {}
                lines = block.split('\n')
                
                # First line often contains institution
                if lines:
                    school['institution'] = lines[0].strip()
                
                # Look for degree keywords
                degree_keywords = ['bachelor', 'master', 'phd', 'doctorate', 'associate', 'diploma']
                for line in lines:
                    for keyword in degree_keywords:
                        if keyword in line.lower():
                            school['degree'] = line.strip()
                            break
                
                # Look for graduation year
                date_pattern = r'\b(19|20)\d{2}\b'
                dates = re.findall(date_pattern, block)
                if dates:
                    school['graduationDate'] = dates[-1]  # Last date is likely graduation
                
                if school:
                    schools.append(school)
        
        return schools

    def _parse_skills_section(self, content: str) -> List[str]:
        """Parse skills from text"""
        skills = []
        
        # Split by commas, newlines, or bullets
        skill_text = re.sub(r'[•\-\*]', ',', content)
        potential_skills = re.split(r'[,\n]', skill_text)
        
        for skill in potential_skills:
            skill = skill.strip()
            if skill and len(skill) > 1:
                skills.append(skill)
        
        return skills

    def _save_txt(self, data: Dict[str, Any], filename: str) -> bool:
        """Save data as formatted text"""
        output = []
        
        # Personal Information
        if 'personalInfo' in data:
            output.append("PERSONAL INFORMATION")
            output.append("=" * 20)
            personal = data['personalInfo']
            
            if 'firstName' in personal and 'lastName' in personal:
                output.append(f"Name: {personal['firstName']} {personal['lastName']}")
            if 'email' in personal:
                output.append(f"Email: {personal['email']}")
            if 'phone' in personal:
                output.append(f"Phone: {personal['phone']}")
            if 'address' in personal:
                addr = personal['address']
                if isinstance(addr, dict):
                    address_parts = [addr.get('street', ''), addr.get('city', ''), 
                                   addr.get('state', ''), addr.get('zipCode', '')]
                    address_str = ', '.join(filter(None, address_parts))
                    if address_str:
                        output.append(f"Address: {address_str}")
            output.append("")
        
        # Work Experience
        if 'workExperience' in data and 'positions' in data['workExperience']:
            output.append("WORK EXPERIENCE")
            output.append("=" * 15)
            
            for position in data['workExperience']['positions']:
                if 'title' in position and 'company' in position:
                    output.append(f"{position['title']} at {position['company']}")
                elif 'company' in position:
                    output.append(f"{position['company']}")
                
                if 'startDate' in position or 'endDate' in position:
                    start = position.get('startDate', '')
                    end = position.get('endDate', 'present')
                    output.append(f"  {start} - {end}")
                
                if 'description' in position:
                    output.append(f"  {position['description']}")
                
                output.append("")
        
        # Education
        if 'education' in data and 'schools' in data['education']:
            output.append("EDUCATION")
            output.append("=" * 9)
            
            for school in data['education']['schools']:
                if 'degree' in school and 'institution' in school:
                    output.append(f"{school['degree']} - {school['institution']}")
                elif 'institution' in school:
                    output.append(f"{school['institution']}")
                
                if 'fieldOfStudy' in school:
                    output.append(f"  Field of Study: {school['fieldOfStudy']}")
                
                if 'graduationDate' in school:
                    output.append(f"  Graduated: {school['graduationDate']}")
                
                output.append("")
        
        # Skills
        if 'skills' in data:
            output.append("SKILLS")
            output.append("=" * 6)
            
            skills = data['skills']
            if 'technical' in skills and skills['technical']:
                output.append("Technical Skills:")
                for skill in skills['technical']:
                    output.append(f"  • {skill}")
                output.append("")
            
            if 'certifications' in skills and skills['certifications']:
                output.append("Certifications:")
                for cert in skills['certifications']:
                    if isinstance(cert, dict) and 'name' in cert:
                        output.append(f"  • {cert['name']}")
                    else:
                        output.append(f"  • {cert}")
                output.append("")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output))
        
        return True

    def standardize_dates(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize all dates in the profile to ISO format (YYYY-MM-DD)"""
        standardized = json.loads(json.dumps(data))  # Deep copy
        
        def standardize_date_recursive(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if 'date' in key.lower() and isinstance(value, str):
                        obj[key] = self._standardize_single_date(value)
                    else:
                        standardize_date_recursive(value)
            elif isinstance(obj, list):
                for item in obj:
                    standardize_date_recursive(item)
        
        standardize_date_recursive(standardized)
        return standardized

    def _standardize_single_date(self, date_str: str) -> str:
        """Convert a single date string to ISO format"""
        if not date_str or date_str.lower() in ['present', 'current', 'ongoing']:
            return date_str
        
        # Try to parse with different formats
        for fmt in self.date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # If no format matches, return original
        return date_str

    def validate_data_structure(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate profile data structure and return any issues"""
        issues = {
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        # Check for required top-level sections
        required_sections = ['personalInfo']
        for section in required_sections:
            if section not in data:
                issues['errors'].append(f"Missing required section: {section}")
        
        # Validate personal info
        if 'personalInfo' in data:
            personal = data['personalInfo']
            if not personal.get('email'):
                issues['warnings'].append("No email address provided")
            if not personal.get('firstName') and not personal.get('lastName'):
                issues['warnings'].append("No name provided")
        
        # Validate work experience
        if 'workExperience' in data and 'positions' in data['workExperience']:
            for i, position in enumerate(data['workExperience']['positions']):
                if not position.get('company'):
                    issues['warnings'].append(f"Position {i+1}: Missing company name")
                if not position.get('title'):
                    issues['warnings'].append(f"Position {i+1}: Missing job title")
        
        # Validate education
        if 'education' in data and 'schools' in data['education']:
            for i, school in enumerate(data['education']['schools']):
                if not school.get('institution'):
                    issues['warnings'].append(f"School {i+1}: Missing institution name")
        
        # Suggestions
        if 'skills' not in data or not data['skills'].get('technical'):
            issues['suggestions'].append("Consider adding technical skills")
        
        if 'workExperience' not in data or not data['workExperience'].get('positions'):
            issues['suggestions'].append("Consider adding work experience")
        
        return issues


def main():
    """Command-line interface for the data converter"""
    parser = argparse.ArgumentParser(description='Convert profile data between formats')
    parser.add_argument('input', help='Input file path')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('--input-format', '-if', choices=['json', 'csv', 'xml', 'yaml', 'txt'],
                       help='Input format (auto-detected if not specified)')
    parser.add_argument('--output-format', '-of', choices=['json', 'csv', 'xml', 'yaml', 'txt'],
                       help='Output format (auto-detected if not specified)')
    parser.add_argument('--standardize-dates', '-sd', action='store_true',
                       help='Standardize all dates to ISO format')
    parser.add_argument('--validate', '-v', action='store_true',
                       help='Validate data structure')
    
    args = parser.parse_args()
    
    converter = ProfileDataConverter()
    
    try:
        # Convert format
        success = converter.convert_format(
            args.input, 
            args.output,
            args.input_format,
            args.output_format
        )
        
        if success:
            print(f"Successfully converted {args.input} to {args.output}")
            
            # Post-processing options
            if args.standardize_dates:
                # Load converted data, standardize dates, and save again
                data = converter._load_data(args.output, 
                                          args.output_format or converter._detect_format(args.output))
                standardized = converter.standardize_dates(data)
                converter._save_data(standardized, args.output, 
                                   args.output_format or converter._detect_format(args.output))
                print("Dates standardized to ISO format")
            
            if args.validate:
                # Validate the converted data
                data = converter._load_data(args.output, 
                                          args.output_format or converter._detect_format(args.output))
                issues = converter.validate_data_structure(data)
                
                if issues['errors']:
                    print("Errors found:")
                    for error in issues['errors']:
                        print(f"  ✗ {error}")
                
                if issues['warnings']:
                    print("Warnings:")
                    for warning in issues['warnings']:
                        print(f"  ⚠ {warning}")
                
                if issues['suggestions']:
                    print("Suggestions:")
                    for suggestion in issues['suggestions']:
                        print(f"  💡 {suggestion}")
                
                if not any(issues.values()):
                    print("✓ Data structure validation passed")
        else:
            print("Conversion failed")
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()