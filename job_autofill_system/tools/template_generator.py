#!/usr/bin/env python3
"""
Job Autofill System - Template Generator
Creates customized profile templates based on user requirements
"""

import json
import argparse
from typing import Dict, List, Any
from datetime import datetime


class ProfileTemplateGenerator:
    """Generates customized job profile templates"""
    
    def __init__(self):
        self.base_templates = {
            'minimal': {
                'personalInfo': {
                    'firstName': '',
                    'lastName': '',
                    'email': '',
                    'phone': ''
                },
                'workExperience': {
                    'positions': []
                }
            },
            'standard': {
                'personalInfo': {
                    'firstName': '',
                    'lastName': '',
                    'email': '',
                    'phone': '',
                    'address': {
                        'street': '',
                        'city': '',
                        'state': '',
                        'zipCode': '',
                        'country': ''
                    },
                    'linkedin': '',
                    'summary': ''
                },
                'workExperience': {
                    'positions': [{
                        'company': '',
                        'title': '',
                        'startDate': '',
                        'endDate': '',
                        'description': '',
                        'location': '',
                        'achievements': []
                    }]
                },
                'education': {
                    'schools': [{
                        'institution': '',
                        'degree': '',
                        'fieldOfStudy': '',
                        'graduationDate': '',
                        'gpa': '',
                        'location': ''
                    }]
                },
                'skills': {
                    'technical': [],
                    'languages': [],
                    'certifications': []
                }
            },
            'comprehensive': {
                'personalInfo': {
                    'firstName': '',
                    'lastName': '',
                    'email': '',
                    'phone': '',
                    'address': {
                        'street': '',
                        'line2': '',
                        'city': '',
                        'state': '',
                        'zipCode': '',
                        'country': ''
                    },
                    'linkedin': '',
                    'website': '',
                    'github': '',
                    'summary': '',
                    'objective': ''
                },
                'workExperience': {
                    'positions': [{
                        'company': '',
                        'title': '',
                        'startDate': '',
                        'endDate': '',
                        'description': '',
                        'location': '',
                        'achievements': [],
                        'responsibilities': [],
                        'technologies': [],
                        'salary': ''
                    }],
                    'totalYears': 0
                },
                'education': {
                    'schools': [{
                        'institution': '',
                        'degree': '',
                        'fieldOfStudy': '',
                        'graduationDate': '',
                        'gpa': '',
                        'location': '',
                        'achievements': [],
                        'coursework': [],
                        'honors': []
                    }]
                },
                'skills': {
                    'technical': [],
                    'languages': [{
                        'language': '',
                        'proficiency': ''
                    }],
                    'certifications': [{
                        'name': '',
                        'issuer': '',
                        'date': '',
                        'expirationDate': '',
                        'credentialId': ''
                    }],
                    'softSkills': []
                },
                'projects': [{
                    'name': '',
                    'description': '',
                    'technologies': [],
                    'url': '',
                    'startDate': '',
                    'endDate': ''
                }],
                'publications': [{
                    'title': '',
                    'publication': '',
                    'date': '',
                    'url': ''
                }],
                'awards': [{
                    'name': '',
                    'issuer': '',
                    'date': '',
                    'description': ''
                }],
                'volunteer': [{
                    'organization': '',
                    'role': '',
                    'startDate': '',
                    'endDate': '',
                    'description': ''
                }]
            }
        }
        
        self.industry_specific = {
            'software_engineering': {
                'skills': {
                    'technical': [
                        'Programming Languages (Python, JavaScript, Java, etc.)',
                        'Frameworks (React, Node.js, Django, etc.)',
                        'Databases (SQL, MongoDB, PostgreSQL)',
                        'Cloud Platforms (AWS, Azure, GCP)',
                        'DevOps (Docker, Kubernetes, CI/CD)',
                        'Version Control (Git, GitHub)',
                        'Testing Frameworks',
                        'Agile Methodologies'
                    ]
                },
                'projects': [{
                    'name': 'Project Name',
                    'description': 'Brief description of the project',
                    'technologies': ['Technology 1', 'Technology 2'],
                    'url': 'https://github.com/username/project',
                    'startDate': 'YYYY-MM-DD',
                    'endDate': 'YYYY-MM-DD'
                }]
            },
            'marketing': {
                'skills': {
                    'technical': [
                        'Google Analytics',
                        'Google Ads',
                        'Facebook Ads Manager',
                        'HubSpot',
                        'Salesforce',
                        'Mailchimp',
                        'Adobe Creative Suite',
                        'Canva',
                        'SEO/SEM',
                        'Social Media Management'
                    ]
                },
                'certifications': [{
                    'name': 'Google Analytics Certified',
                    'issuer': 'Google',
                    'date': 'YYYY-MM-DD',
                    'credentialId': ''
                }]
            },
            'finance': {
                'skills': {
                    'technical': [
                        'Financial Modeling',
                        'Excel/VBA',
                        'Bloomberg Terminal',
                        'SAP',
                        'QuickBooks',
                        'Financial Analysis',
                        'Risk Management',
                        'Portfolio Management'
                    ]
                },
                'certifications': [{
                    'name': 'CFA (Chartered Financial Analyst)',
                    'issuer': 'CFA Institute',
                    'date': 'YYYY-MM-DD',
                    'credentialId': ''
                }]
            },
            'healthcare': {
                'skills': {
                    'technical': [
                        'Electronic Health Records (EHR)',
                        'HIPAA Compliance',
                        'Medical Terminology',
                        'Patient Care',
                        'Clinical Documentation',
                        'Medical Software Systems'
                    ]
                },
                'certifications': [{
                    'name': 'BLS (Basic Life Support)',
                    'issuer': 'American Heart Association',
                    'date': 'YYYY-MM-DD',
                    'expirationDate': 'YYYY-MM-DD'
                }]
            },
            'education': {
                'skills': {
                    'technical': [
                        'Learning Management Systems (LMS)',
                        'Educational Technology',
                        'Curriculum Development',
                        'Assessment Design',
                        'Classroom Management',
                        'Online Teaching Platforms'
                    ]
                },
                'certifications': [{
                    'name': 'Teaching License',
                    'issuer': 'State Department of Education',
                    'date': 'YYYY-MM-DD',
                    'expirationDate': 'YYYY-MM-DD'
                }]
            }
        }

    def generate_template(self, template_type: str = 'standard', 
                         industry: str = None, 
                         include_examples: bool = False) -> Dict[str, Any]:
        """
        Generate a customized profile template
        
        Args:
            template_type: 'minimal', 'standard', or 'comprehensive'
            industry: Industry-specific customizations
            include_examples: Whether to include example data
            
        Returns:
            Dictionary containing the generated template
        """
        if template_type not in self.base_templates:
            raise ValueError(f"Unknown template type: {template_type}")
        
        # Start with base template
        template = json.loads(json.dumps(self.base_templates[template_type]))
        
        # Add industry-specific fields
        if industry and industry in self.industry_specific:
            industry_data = self.industry_specific[industry]
            template = self._merge_templates(template, industry_data)
        
        # Add examples if requested
        if include_examples:
            template = self._add_examples(template, industry)
        
        # Add metadata
        template['metadata'] = {
            'templateType': template_type,
            'industry': industry,
            'version': '1.0.0',
            'createdDate': datetime.now().isoformat(),
            'description': f'{template_type.title()} profile template' + 
                          (f' for {industry}' if industry else '')
        }
        
        return template

    def _merge_templates(self, base: Dict[str, Any], addition: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge two template dictionaries"""
        result = base.copy()
        
        for key, value in addition.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_templates(result[key], value)
            elif key in result and isinstance(result[key], list) and isinstance(value, list):
                # For lists, append unique items
                for item in value:
                    if item not in result[key]:
                        result[key].append(item)
            else:
                result[key] = value
        
        return result

    def _add_examples(self, template: Dict[str, Any], industry: str = None) -> Dict[str, Any]:
        """Add example data to template fields"""
        examples = template.copy()
        
        # Personal info examples
        if 'personalInfo' in examples:
            examples['personalInfo'].update({
                'firstName': 'John',
                'lastName': 'Doe',
                'email': 'john.doe@email.com',
                'phone': '+1 (555) 123-4567',
                'summary': 'Experienced professional with expertise in...'
            })
            
            if 'address' in examples['personalInfo']:
                examples['personalInfo']['address'].update({
                    'street': '123 Main Street',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'zipCode': '94102',
                    'country': 'United States'
                })
        
        # Work experience examples
        if 'workExperience' in examples and 'positions' in examples['workExperience']:
            if examples['workExperience']['positions']:
                position = examples['workExperience']['positions'][0]
                position.update({
                    'company': 'Tech Company Inc.',
                    'title': 'Software Engineer' if industry == 'software_engineering' else 'Professional',
                    'startDate': '2020-01-15',
                    'endDate': 'present',
                    'description': 'Responsible for developing and maintaining...',
                    'location': 'San Francisco, CA'
                })
                
                if 'achievements' in position:
                    position['achievements'] = [
                        'Increased team productivity by 25%',
                        'Led successful project delivery'
                    ]
        
        # Education examples
        if 'education' in examples and 'schools' in examples['education']:
            if examples['education']['schools']:
                school = examples['education']['schools'][0]
                school.update({
                    'institution': 'University of California',
                    'degree': 'Bachelor of Science',
                    'fieldOfStudy': 'Computer Science' if industry == 'software_engineering' else 'Business',
                    'graduationDate': '2019-05-15',
                    'gpa': '3.8',
                    'location': 'Berkeley, CA'
                })
        
        return examples

    def generate_multiple_templates(self, industries: List[str], 
                                  template_types: List[str] = None) -> Dict[str, Dict[str, Any]]:
        """Generate multiple templates for different industries"""
        if template_types is None:
            template_types = ['standard']
        
        templates = {}
        
        for industry in industries:
            for template_type in template_types:
                key = f"{industry}_{template_type}"
                templates[key] = self.generate_template(
                    template_type=template_type,
                    industry=industry,
                    include_examples=False
                )
        
        return templates

    def save_template(self, template: Dict[str, Any], filename: str):
        """Save template to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)

    def list_available_options(self) -> Dict[str, List[str]]:
        """List all available template types and industries"""
        return {
            'template_types': list(self.base_templates.keys()),
            'industries': list(self.industry_specific.keys())
        }


def main():
    """Command-line interface for the template generator"""
    parser = argparse.ArgumentParser(description='Generate job profile templates')
    parser.add_argument('--type', '-t', choices=['minimal', 'standard', 'comprehensive'],
                       default='standard', help='Template type')
    parser.add_argument('--industry', '-i', 
                       choices=['software_engineering', 'marketing', 'finance', 'healthcare', 'education'],
                       help='Industry-specific customizations')
    parser.add_argument('--examples', '-e', action='store_true',
                       help='Include example data')
    parser.add_argument('--output', '-o', default='profile_template.json',
                       help='Output filename')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List available options')
    parser.add_argument('--batch', '-b', action='store_true',
                       help='Generate templates for all industries')
    
    args = parser.parse_args()
    
    generator = ProfileTemplateGenerator()
    
    if args.list:
        options = generator.list_available_options()
        print("Available template types:")
        for template_type in options['template_types']:
            print(f"  - {template_type}")
        print("\nAvailable industries:")
        for industry in options['industries']:
            print(f"  - {industry}")
        return
    
    if args.batch:
        # Generate templates for all industries and types
        templates = generator.generate_multiple_templates(
            industries=list(generator.industry_specific.keys()),
            template_types=['minimal', 'standard', 'comprehensive']
        )
        
        for name, template in templates.items():
            filename = f"template_{name}.json"
            generator.save_template(template, filename)
            print(f"Generated: {filename}")
    else:
        # Generate single template
        template = generator.generate_template(
            template_type=args.type,
            industry=args.industry,
            include_examples=args.examples
        )
        
        generator.save_template(template, args.output)
        print(f"Template generated: {args.output}")
        
        # Print summary
        metadata = template.get('metadata', {})
        print(f"Type: {metadata.get('templateType', 'Unknown')}")
        if metadata.get('industry'):
            print(f"Industry: {metadata.get('industry')}")
        if args.examples:
            print("Includes example data")


if __name__ == '__main__':
    main()