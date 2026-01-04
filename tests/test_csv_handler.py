"""
Tests for the CSV handler module.
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src'))

from handlers.csv_handler import (
    create_csv_template,
    create_simple_template,
    validate_csv_format,
    detect_csv_format,
    process_uploaded_data,
    create_sample_csv_content,
)


class TestCSVTemplates:
    """Test CSV template creation functions."""
    
    def test_create_csv_template_returns_string(self):
        """Test that create_csv_template returns a non-empty string."""
        template = create_csv_template()
        assert isinstance(template, str)
        assert len(template) > 0
    
    def test_create_csv_template_has_required_columns(self):
        """Test that CSV template contains required columns."""
        template = create_csv_template()
        assert 'player_name' in template
        assert 'career_goals' in template
        assert 'total_la_liga_titles' in template
        assert 'total_champions_league_titles' in template
    
    def test_create_simple_template_returns_string(self):
        """Test that create_simple_template returns a non-empty string."""
        template = create_simple_template()
        assert isinstance(template, str)
        assert len(template) > 0


class TestCSVValidation:
    """Test CSV validation functions."""
    
    def test_validate_custom_template_format_valid(self):
        """Test validation of valid custom template CSV."""
        df = pd.DataFrame({
            'player_name': ['Test Player'],
            'career_goals': [100],
            'total_la_liga_titles': [2],
            'total_champions_league_titles': [1]
        })
        
        is_valid, message = validate_csv_format(df)
        assert is_valid is True
        assert '✅' in message
    
    def test_validate_custom_template_format_missing_columns(self):
        """Test validation fails when required columns missing."""
        df = pd.DataFrame({
            'player_name': ['Test Player'],
            'career_goals': [100]
            # Missing total_la_liga_titles and total_champions_league_titles
        })
        
        is_valid, message = validate_csv_format(df)
        assert is_valid is False
        assert 'Missing' in message or 'required' in message.lower()
    
    def test_detect_csv_format_custom_template(self):
        """Test detection of custom template format."""
        df = pd.DataFrame({
            'player_name': ['Test Player'],
            'career_goals': [100],
            'total_la_liga_titles': [2],
            'total_champions_league_titles': [1]
        })
        
        format_type = detect_csv_format(df)
        assert format_type == 'custom_template'
    
    def test_detect_csv_format_football_stats(self):
        """Test detection of football stats format."""
        df = pd.DataFrame({
            'Player': ['Test Player'],
            'Squad': ['Test FC'],
            'Goals': [20],
            'Assists': [10],
            'Pos': ['FW'],
            'Comp': ['La Liga']
        })
        
        format_type = detect_csv_format(df)
        assert format_type == 'football_stats'


class TestDataProcessing:
    """Test data processing functions."""
    
    def test_process_uploaded_data_custom_template(self):
        """Test processing of custom template data."""
        df = pd.DataFrame({
            'player_name': ['Test Player'],
            'career_goals': [100],
            'total_la_liga_titles': [2],
            'total_champions_league_titles': [1],
            'ballon_dor_wins': [0]
        })
        
        processed = process_uploaded_data(df)
        assert 'Test Player' in processed
        assert processed['Test Player']['career_goals'] == 100
        assert processed['Test Player']['total_la_liga_titles'] == 2
    
    def test_create_sample_csv_content(self):
        """Test sample CSV content creation."""
        sample = create_sample_csv_content()
        assert isinstance(sample, str)
        assert 'Lionel Messi' in sample
        assert 'Cristiano Ronaldo' in sample


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
