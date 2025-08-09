#!/usr/bin/env python3
"""
Test script for the enhanced CSV handler with football statistics data
"""

import pandas as pd
import sys
import os

# Add scripts directory to path
sys.path.append('scripts')

try:
    from csv_handler import validate_and_preview_data, process_uploaded_data
except ImportError as e:
    print(f"Error importing CSV handler: {e}")
    exit(1)

class MockFile:
    """Mock file object for testing"""
    def __init__(self, filepath):
        self.filepath = filepath
        self.position = 0
        
    def seek(self, pos):
        self.position = pos
        
    def read(self):
        with open(self.filepath, 'rb') as f:
            f.seek(self.position)
            return f.read()

def main():
    # Test with your football stats file
    csv_file = 'test_football_stats.csv'
    
    if not os.path.exists(csv_file):
        print(f"❌ File {csv_file} not found")
        return
    
    print('🔍 Testing Enhanced CSV Handler with Football Stats...')
    print()
    
    # Test validation and preview using a proper file object
    try:
        with open(csv_file, 'rb') as file_obj:
            success, df, message = validate_and_preview_data(file_obj)
            print('📊 Validation Result:')
            print(f'Success: {success}')
            print(f'Message: {message}')
            print()
            
            if success:
                print('📈 Processing player data...')
                processed_data = process_uploaded_data(df)
                
                print(f'✅ Processed {len(processed_data)} players')
                print()
                
                # Show sample of processed data
                print('📋 Sample processed players (first 3):')
                for i, (name, data) in enumerate(list(processed_data.items())[:3]):
                    print(f'{i+1}. {name}:')
                    print(f'   - Goals: {data["career_goals"]}')
                    print(f'   - Seasons: {len(data["seasons"])}')
                    if data['seasons']:
                        season = data['seasons'][0]
                        print(f'   - 2022/23: {season["goals"]} goals, {season["assists"]} assists ({season["squad"]})')
                    print()
                
                # Show statistics
                print('📊 Summary Statistics:')
                total_goals = sum(player["career_goals"] for player in processed_data.values())
                players_with_goals = sum(1 for player in processed_data.values() if player["career_goals"] > 0)
                players_with_seasons = sum(1 for player in processed_data.values() if player["seasons"])
                
                print(f'- Total goals across all players: {total_goals}')
                print(f'- Players with goals: {players_with_goals}')
                print(f'- Players with season data: {players_with_seasons}')
                
                # Top scorers
                if players_with_goals > 0:
                    top_scorers = sorted(processed_data.items(), key=lambda x: x[1]["career_goals"], reverse=True)[:5]
                    print()
                    print('🎯 Top 5 Scorers:')
                    for i, (name, data) in enumerate(top_scorers):
                        squad = data['seasons'][0]['squad'] if data['seasons'] else 'Unknown'
                        print(f'{i+1}. {name}: {data["career_goals"]} goals ({squad})')
            else:
                print('❌ Validation failed')
                
    except Exception as e:
        print(f'❌ Error during processing: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
