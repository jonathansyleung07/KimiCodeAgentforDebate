"""
Parser for OBJECTIVE.md configuration file
"""

import os
import re
from typing import List, Dict, Any


class ObjectiveParser:
    """
    Parses the OBJECTIVE.md file to extract debate configuration.
    """
    
    def __init__(self, filepath: str = "OBJECTIVE.md"):
        """
        Initialize parser with path to OBJECTIVE.md.
        
        Args:
            filepath: Path to the OBJECTIVE.md file
        """
        self.filepath = filepath
        self.content = None
        
    def parse(self) -> Dict[str, Any]:
        """
        Parse the OBJECTIVE.md file and return configuration.
        
        Returns:
            Dictionary containing all debate configuration
        """
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"OBJECTIVE.md not found at {self.filepath}")
        
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        config = {
            'topic': self._extract_topic(),
            'debaters': self._extract_debaters(),
            'parameters': self._extract_parameters(),
        }
        
        return config
    
    def _extract_topic(self) -> str:
        """Extract the debate topic."""
        # Look for "## Debate Topic" section
        pattern = r'## Debate Topic\s*\n+([^#\n].*?)(?:\n\n|\n##|$)'
        match = re.search(pattern, self.content, re.DOTALL | re.IGNORECASE)
        
        if match:
            topic = match.group(1).strip()
            # Remove any markdown formatting
            topic = re.sub(r'\*\*', '', topic)
            topic = re.sub(r'- \*\*Topic\*\*:\s*', '', topic)
            return topic
        
        # Fallback: look for first header after "Debate Topic"
        lines = self.content.split('\n')
        in_topic_section = False
        for line in lines:
            if '## Debate Topic' in line:
                in_topic_section = True
                continue
            if in_topic_section and line.strip():
                if line.startswith('#'):
                    break
                cleaned = line.strip()
                if cleaned:
                    return re.sub(r'\*\*', '', cleaned)
        
        return "Unknown Topic"
    
    def _extract_debaters(self) -> List[Dict[str, str]]:
        """Extract debater configurations."""
        debaters = []
        
        # Pattern to match debater sections
        # Looks for "#### Debater X: Name" or similar headers
        pattern = r'####\s*Debater\s*\d+:\s*(.+?)\n((?:(?!####).)*)'
        matches = re.findall(pattern, self.content, re.DOTALL | re.IGNORECASE)
        
        for match in matches:
            alias = match[0].strip()
            section = match[1]
            
            debater = {
                'alias': alias,
                'model': self._extract_field(section, 'model'),
                'language': self._extract_field(section, 'language'),
                'role': self._extract_field(section, 'role'),
                'stance': self._extract_field(section, 'stance'),
            }
            
            debaters.append(debater)
        
        # Alternative pattern: look for debater subsections
        if not debaters:
            pattern = r'####\s*(.+?)\n((?:(?!####).)*)'
            matches = re.findall(pattern, self.content, re.DOTALL)
            
            for match in matches:
                header = match[0].strip()
                section = match[1]
                
                # Check if this looks like a debater section
                if any(keyword in section.lower() for keyword in ['model', 'alias', 'role', 'stance']):
                    alias = self._extract_field(section, 'alias') or header.replace('Debater:', '').strip()
                    
                    debater = {
                        'alias': alias,
                        'model': self._extract_field(section, 'model'),
                        'language': self._extract_field(section, 'language'),
                        'role': self._extract_field(section, 'role'),
                        'stance': self._extract_field(section, 'stance'),
                    }
                    
                    debaters.append(debater)
        
        return debaters
    
    def _extract_field(self, section: str, field_name: str) -> str:
        """Extract a field value from a section."""
        # Pattern: - **Field**: value
        pattern = rf'-?\s*\*?\*{field_name}\*?\*?\s*[:\-]\s*(.+?)(?:\n|$)'
        match = re.search(pattern, section, re.IGNORECASE)
        
        if match:
            value = match.group(1).strip()
            # Clean up markdown
            value = re.sub(r'\*\*', '', value)
            return value
        
        return ""
    
    def _extract_parameters(self) -> Dict[str, Any]:
        """Extract debate parameters."""
        params = {}
        
        # Extract number of rounds
        rounds_match = re.search(
            r'(?:\*\*)?Number of Rounds(?:\*\*)?\s*[:\-]?\s*(\d+)',
            self.content,
            re.IGNORECASE
        )
        params['num_rounds'] = int(rounds_match.group(1)) if rounds_match else 3
        
        # Extract words per speech
        words_match = re.search(
            r'(?:\*\*)?(?:Number of )?Words per Speech(?:\*\*)?\s*[:\-]?\s*(\d+)',
            self.content,
            re.IGNORECASE
        )
        params['words_per_speech'] = int(words_match.group(1)) if words_match else 1000
        
        # Extract research rounds
        research_match = re.search(
            r'(?:\*\*)?(?:Research Rounds|(?:Number of )?Research Rounds)(?:\*\*)?\s*[:\-]?\s*(\d+)',
            self.content,
            re.IGNORECASE
        )
        params['research_rounds'] = int(research_match.group(1)) if research_match else 2
        
        return params
