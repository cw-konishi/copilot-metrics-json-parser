import json
from datetime import datetime

def parse_old_to_new(old_data):
    new_data = []
    for entry in old_data:
        new_entry = {
            "date": entry["day"],
            "total_active_users": entry["total_active_users"],
            "total_engaged_users": entry["total_active_users"],  # Assuming engaged users are the same as active users
            "copilot_ide_code_completions": {
                "total_engaged_users": entry["total_active_users"],
                "languages": [],
                "editors": []
            },
            "copilot_ide_chat": {
                "total_engaged_users": entry["total_active_chat_users"],
                "editors": []
            },
            "copilot_dotcom_chat": {
                "total_engaged_users": entry["total_active_chat_users"],
                "models": [
                    {
                        "name": "default",
                        "is_custom_model": False,
                        "custom_model_training_date": None,
                        "total_engaged_users": entry["total_active_chat_users"],
                        "total_chats": entry["total_chat_turns"]
                    }
                ]
            },
            "copilot_dotcom_pull_requests": {
                "total_engaged_users": 0,  # No data available in old format
                "repositories": []
            }
        }

        language_engaged_users = {}
        editor_engaged_users = {}

        for breakdown in entry["breakdown"]:
            language = breakdown["language"]
            editor = breakdown["editor"]

            if language not in language_engaged_users:
                language_engaged_users[language] = 0
            language_engaged_users[language] += breakdown["active_users"]

            if editor not in editor_engaged_users:
                editor_engaged_users[editor] = 0
            editor_engaged_users[editor] += breakdown["active_users"]

            new_entry["copilot_ide_code_completions"]["languages"].append({
                "name": language,
                "total_engaged_users": language_engaged_users[language]
            })

            new_entry["copilot_ide_code_completions"]["editors"].append({
                "name": editor,
                "total_engaged_users": editor_engaged_users[editor],
                "models": [
                    {
                        "name": "default",
                        "is_custom_model": False,
                        "custom_model_training_date": None,
                        "total_engaged_users": editor_engaged_users[editor],
                        "languages": [
                            {
                                "name": language,
                                "total_engaged_users": breakdown["active_users"],
                                "total_code_suggestions": breakdown["suggestions_count"],
                                "total_code_acceptances": breakdown["acceptances_count"],
                                "total_code_lines_suggested": breakdown["lines_suggested"],
                                "total_code_lines_accepted": breakdown["lines_accepted"]
                            }
                        ]
                    }
                ]
            })

            new_entry["copilot_ide_chat"]["editors"].append({
                "name": editor,
                "total_engaged_users": entry["total_active_chat_users"],
                "models": [
                    {
                        "name": "default",
                        "is_custom_model": False,
                        "custom_model_training_date": None,
                        "total_engaged_users": entry["total_active_chat_users"],
                        "total_chats": entry["total_chat_turns"],
                        "total_chat_insertion_events": 0,  # No data available in old format
                        "total_chat_copy_events": 0  # No data available in old format
                    }
                ]
            })

        new_data.append(new_entry)
    return new_data

if __name__ == "__main__":
    with open('/c:/Users/chiru/copilot-metrics-json-parser/sample-json/old.json', 'r') as f:
        old_data = json.load(f)

    new_data = parse_old_to_new(old_data)

    with open('/c:/Users/chiru/copilot-metrics-json-parser/sample-json/new.json', 'w') as f:
        json.dump(new_data, f, indent=2)
