"""
Player data and scoring system definitions.
"""

from typing import Dict, Any, List

# Define the points system
points_system: Dict[str, int] = {
    "Ballon d'Or Win": 5,
    "Ballon d'Or 2nd Place": 3,    
    "Ballon d'Or 3rd Place": 1,
    "La Liga Title": 1,             
    "Champions League Win": 5,      
    "La Liga Best Player Award": 4,
    "La Liga Breakthrough Player": 1,
    "La Liga Golden Boot": 3,       
    "20+ Goal La Liga Season": 2,   
    "Most Assists in La Liga Season": 2,
    "10+ Assist La Liga Season": 1,
    "Cup Final Winner": 1,
    "Other Trophies": 1,
    "200+ La Liga Goals": 5,        
    "100+ La Liga Goals": 2,        
    "CL Top Scorer": 5,             
    "Most Assists in CL Season": 2
}


# Player data with comprehensive stats
players: Dict[str, Dict[str, Any]] = {
    "Lionel Messi": {
        "career_goals": 474,  # Total La Liga goals
        "seasons": [
            {
                "season": "2011/2012",
                "goals": 50,  # Actual: 50 goals in La Liga
                "assists": 15,
                "awards": [
                    "Ballon d'Or Win",
                    "La Liga Best Player Award",
                    "La Liga Golden Boot"
                ],
                "team_achievements": ["La Liga Title", "Copa del Rey"],
                "cup_final_winner": True,
                "cl_achievements": [
                    "CL Top Scorer"
                ]
            },
            {
                "season": "2014/2015",
                "goals": 43,  # Actual: 43 goals in La Liga
                "assists": 18,
                "awards": [
                    "La Liga Best Player Award"
                ],
                "team_achievements": ["La Liga Title", "Champions League Win", "Copa del Rey"],
                "cup_final_winner": True,
                "cl_achievements": []
            },
            {
                "season": "2009/2010",
                "goals": 34,  # Actual: 34 goals in La Liga
                "assists": 11,
                "awards": [
                    "Ballon d'Or Win",
                    "La Liga Best Player Award",
                    "La Liga Golden Boot"
                ],
                "team_achievements": ["La Liga Title"],
                "cup_final_winner": False,
                "cl_achievements": []
            }
        ],
        "career_awards": ["Ballon d'Or Win"] * 4,  # 4 Ballon d'Or wins during La Liga career
        "total_la_liga_titles": 10,
        "total_champions_league_titles": 4
    },
    "Cristiano Ronaldo": {
        "career_goals": 311,  # Total La Liga goals
        "seasons": [
            {
                "season": "2013/2014",
                "goals": 31,  # Actual: 31 goals in La Liga
                "assists": 11,
                "awards": [
                    "Ballon d'Or Win"
                ],
                "team_achievements": ["Champions League Win", "Copa del Rey"],
                "cup_final_winner": True,
                "cl_achievements": ["CL Top Scorer"]
            },
            {
                "season": "2015/2016",
                "goals": 35,  # Actual: 35 goals in La Liga
                "assists": 11,
                "awards": [
                    "Ballon d'Or Win"
                ],
                "team_achievements": ["Champions League Win"],
                "cup_final_winner": False,
                "cl_achievements": ["CL Top Scorer"]
            },
            {
                "season": "2011/2012",
                "goals": 46,  # Actual: 46 goals in La Liga
                "assists": 12,
                "awards": [
                    "La Liga Golden Boot"
                ],
                "team_achievements": ["La Liga Title"],
                "cup_final_winner": False,
                "cl_achievements": []
            }
        ],
        "career_awards": ["Ballon d'Or Win"] * 4,  # 4 Ballon d'Or wins during Real Madrid career
        "total_la_liga_titles": 2,
        "total_champions_league_titles": 4
    },
    "Luis Suárez": {
        "career_goals": 147,  # Total La Liga goals with Barcelona
        "seasons": [
            {
                "season": "2015/2016",
                "goals": 40,  # Actual: 40 goals in La Liga
                "assists": 16,
                "awards": [
                    "La Liga Golden Boot"
                ],
                "team_achievements": ["La Liga Title", "Copa del Rey"],
                "cup_final_winner": True,
                "cl_achievements": []
            },
            {
                "season": "2016/2017",
                "goals": 29,  # Actual: 29 goals in La Liga
                "assists": 13,
                "awards": [],
                "team_achievements": ["Copa del Rey"],
                "cup_final_winner": True,
                "cl_achievements": []
            },
            {
                "season": "2017/2018",
                "goals": 25,  # Actual: 25 goals in La Liga
                "assists": 12,
                "awards": [],
                "team_achievements": ["La Liga Title", "Copa del Rey"],
                "cup_final_winner": True,
                "cl_achievements": []
            }
        ],
        "career_awards": [],  # No Ballon d'Or wins during La Liga career
        "total_la_liga_titles": 4,
        "total_champions_league_titles": 1
    },
    "Karim Benzema": {
        "career_goals": 238,  # Total La Liga goals
        "seasons": [
            {
                "season": "2021/2022",
                "goals": 27,  # Actual: 27 goals in La Liga
                "assists": 12,
                "awards": [
                    "Ballon d'Or Win",
                    "La Liga Best Player Award"
                ],
                "team_achievements": ["La Liga Title", "Champions League Win", "Supercopa de España"],
                "cup_final_winner": True,
                "cl_achievements": [
                    "CL Top Scorer"
                ]
            },
            {
                "season": "2015/2016",
                "goals": 24,  # Actual: 24 goals in La Liga
                "assists": 7,
                "awards": [],
                "team_achievements": ["Champions League Win"],
                "cup_final_winner": False,
                "cl_achievements": []
            },
            {
                "season": "2019/2020",
                "goals": 21,  # Actual: 21 goals in La Liga
                "assists": 8,
                "awards": [],
                "team_achievements": ["La Liga Title"],
                "cup_final_winner": False,
                "cl_achievements": []
            }
        ],
        "career_awards": ["Ballon d'Or Win"],  # 1 Ballon d'Or win (2022)
        "total_la_liga_titles": 5,  # Updated: 5 La Liga titles with Real Madrid
        "total_champions_league_titles": 5
    },
    "Neymar Jr.": {
        "career_goals": 68,
        "seasons": [
            {
                "season": "2015/2016",
                "goals": 24,
                "assists": 12,
                "awards": [],
                "team_achievements": ["La Liga Title", "Copa del Rey"],
                "cup_final_winner": True,
                "cl_achievements": []
            },
            {
                "season": "2014/2015",
                "goals": 22,
                "assists": 7,
                "awards": [],
                "team_achievements": ["La Liga Title", "Champions League Win", "Copa del Rey"],
                "cup_final_winner": True,
                "cl_achievements": []
            },
            {
                "season": "2016/2017",
                "goals": 13,
                "assists": 11,
                "awards": ["Most Assists in La Liga Season"],
                "team_achievements": ["Copa del Rey"],
                "cup_final_winner": True,
                "cl_achievements": []
            }
        ],
        "career_awards": [],
        "total_la_liga_titles": 2,
        "total_champions_league_titles": 1
    },
    "Gareth Bale": {
        "career_goals": 81,
        "seasons": [
            {
                "season": "2013/2014",
                "goals": 15,
                "assists": 12,
                "awards": ["La Liga Breakthrough Player"],
                "team_achievements": ["Champions League Win", "Copa del Rey"],
                "cup_final_winner": True,
                "cl_achievements": []
            },
            {
                "season": "2015/2016",
                "goals": 19,
                "assists": 10,
                "awards": [],
                "team_achievements": ["Champions League Win"],
                "cup_final_winner": False,
                "cl_achievements": []
            },
            {
                "season": "2017/2018",
                "goals": 16,
                "assists": 2,
                "awards": [],
                "team_achievements": ["Champions League Win"],
                "cup_final_winner": True,  # Scored in UCL final
                "cl_achievements": []
            }
        ],
        "career_awards": [],
        "total_la_liga_titles": 3,
        "total_champions_league_titles": 5
    },
    "Raúl González": {
        "career_goals": 228,
        "seasons": [
            {
                "season": "1998/1999",
                "goals": 25,
                "assists": 5,
                "awards": ["La Liga Golden Boot"],
                "team_achievements": [],
                "cup_final_winner": False,
                "cl_achievements": []
            },
            {
                "season": "2000/2001",
                "goals": 24,
                "assists": 6,
                "awards": ["Ballon d'Or 2nd Place"],
                "team_achievements": ["La Liga Title"],
                "cup_final_winner": False,
                "cl_achievements": ["CL Top Scorer"]
            },
            {
                "season": "1999/2000",
                "goals": 17,
                "assists": 9,
                "awards": [],
                "team_achievements": ["Champions League Win"],
                "cup_final_winner": False,
                "cl_achievements": ["CL Top Scorer"]
            }
        ],
        "career_awards": [],
        "total_la_liga_titles": 6,
        "total_champions_league_titles": 3
    }
}
