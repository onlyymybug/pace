# W3 failure cases

A row is treated as a failure when `correct_under_deadline != true`. The primary taxonomy separates strict JSON parsing, function-call envelope, action selection, and argument errors. `action_valid` independently records whether the predicted call conforms to its declared action schema.

## 1. w3v2_006_always_max_b96_r1_d2000

- sample_id: `w3v2_006`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2261.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Reminder", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "Mon-Fri 08:00", "vibrate": false}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 14, "keyword": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_006_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=search_calendar, got=set_alarm"`

## 2. w3v2_006_always_max_b96_r1_d5000

- sample_id: `w3v2_006`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `2261.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Reminder", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "Mon-Fri 08:00", "vibrate": false}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 14, "keyword": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_006_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=search_calendar, got=set_alarm"`

## 3. w3v2_006_always_max_b96_r1_d10000

- sample_id: `w3v2_006`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `2261.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Reminder", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "Mon-Fri 08:00", "vibrate": false}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 14, "keyword": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_006_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=search_calendar, got=set_alarm"`

## 4. w3v2_007_always_max_b96_r1_d2000

- sample_id: `w3v2_007`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": "off"}`
- gold action: `search_web`
- gold arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_007_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'safe_search' must have type boolean"`

## 5. w3v2_007_always_max_b96_r1_d5000

- sample_id: `w3v2_007`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": "off"}`
- gold action: `search_web`
- gold arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_007_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'safe_search' must have type boolean"`

## 6. w3v2_007_always_max_b96_r1_d10000

- sample_id: `w3v2_007`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": "off"}`
- gold action: `search_web`
- gold arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_007_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'safe_search' must have type boolean"`

## 7. w3v2_008_always_max_b96_r1_d2000

- sample_id: `w3v2_008`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_contacts`
- predicted arguments: `{"favorites_only": "true", "name": "Robert Wang"}`
- gold action: `search_contacts`
- gold arguments: `{"favorites_only": true, "name": "Robert Wang"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_008_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'favorites_only' must have type boolean"`

## 8. w3v2_008_always_max_b96_r1_d5000

- sample_id: `w3v2_008`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_contacts`
- predicted arguments: `{"favorites_only": "true", "name": "Robert Wang"}`
- gold action: `search_contacts`
- gold arguments: `{"favorites_only": true, "name": "Robert Wang"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_008_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'favorites_only' must have type boolean"`

## 9. w3v2_008_always_max_b96_r1_d10000

- sample_id: `w3v2_008`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_contacts`
- predicted arguments: `{"favorites_only": "true", "name": "Robert Wang"}`
- gold action: `search_contacts`
- gold arguments: `{"favorites_only": true, "name": "Robert Wang"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_008_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'favorites_only' must have type boolean"`

## 10. w3v2_009_always_max_b96_r1_d2000

- sample_id: `w3v2_009`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_calendar`
- predicted arguments: `{"days_ahead": "30", "keyword": "dentist"}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 30, "keyword": "dentist"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_009_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'days_ahead' must have type integer"`

## 11. w3v2_009_always_max_b96_r1_d5000

- sample_id: `w3v2_009`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_calendar`
- predicted arguments: `{"days_ahead": "30", "keyword": "dentist"}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 30, "keyword": "dentist"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_009_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'days_ahead' must have type integer"`

## 12. w3v2_009_always_max_b96_r1_d10000

- sample_id: `w3v2_009`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_calendar`
- predicted arguments: `{"days_ahead": "30", "keyword": "dentist"}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 30, "keyword": "dentist"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_009_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'days_ahead' must have type integer"`

## 13. w3v2_012_always_max_b96_r1_d2000

- sample_id: `w3v2_012`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": 1, "element_id": "Continue", "visible_only": true}`
- gold action: `find_ui_element`
- gold arguments: `{"description": "Continue button", "visible_only": true}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_012_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=find_ui_element, got=click_element"`

## 14. w3v2_012_always_max_b96_r1_d5000

- sample_id: `w3v2_012`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": 1, "element_id": "Continue", "visible_only": true}`
- gold action: `find_ui_element`
- gold arguments: `{"description": "Continue button", "visible_only": true}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_012_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=find_ui_element, got=click_element"`

## 15. w3v2_012_always_max_b96_r1_d10000

- sample_id: `w3v2_012`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": 1, "element_id": "Continue", "visible_only": true}`
- gold action: `find_ui_element`
- gold arguments: `{"description": "Continue button", "visible_only": true}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_012_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=find_ui_element, got=click_element"`

## 16. w3v2_013_always_max_b96_r1_d2000

- sample_id: `w3v2_013`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": "2", "element_id": "result_42"}`
- gold action: `click_element`
- gold arguments: `{"click_count": 2, "element_id": "result_42"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_013_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'click_count' must have type integer"`

## 17. w3v2_013_always_max_b96_r1_d5000

- sample_id: `w3v2_013`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": "2", "element_id": "result_42"}`
- gold action: `click_element`
- gold arguments: `{"click_count": 2, "element_id": "result_42"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_013_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'click_count' must have type integer"`

## 18. w3v2_013_always_max_b96_r1_d10000

- sample_id: `w3v2_013`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": "2", "element_id": "result_42"}`
- gold action: `click_element`
- gold arguments: `{"click_count": 2, "element_id": "result_42"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_013_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'click_count' must have type integer"`

## 19. w3v2_015_always_max_b96_r1_d2000

- sample_id: `w3v2_015`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `1595.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": true, "text": "meeting moved to room 302."}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": true, "text": "meeting moved to room 302"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_015_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": true, \"text\": \"meeting moved to room 302\"}, got={\"replace_existing\": true, \"text\": \"meeting moved to room 302.\"}"`

## 20. w3v2_015_always_max_b96_r1_d5000

- sample_id: `w3v2_015`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `1595.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": true, "text": "meeting moved to room 302."}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": true, "text": "meeting moved to room 302"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_015_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": true, \"text\": \"meeting moved to room 302\"}, got={\"replace_existing\": true, \"text\": \"meeting moved to room 302.\"}"`

## 21. w3v2_015_always_max_b96_r1_d10000

- sample_id: `w3v2_015`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `1595.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": true, "text": "meeting moved to room 302."}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": true, "text": "meeting moved to room 302"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_015_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": true, \"text\": \"meeting moved to room 302\"}, got={\"replace_existing\": true, \"text\": \"meeting moved to room 302.\"}"`

## 22. w3v2_016_always_max_b96_r1_d2000

- sample_id: `w3v2_016`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `1292.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": false, "text": "shipping address"}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": false, "text": "billing address"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_016_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": false, \"text\": \"billing address\"}, got={\"replace_existing\": false, \"text\": \"shipping address\"}"`

## 23. w3v2_016_always_max_b96_r1_d5000

- sample_id: `w3v2_016`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `1292.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": false, "text": "shipping address"}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": false, "text": "billing address"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_016_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": false, \"text\": \"billing address\"}, got={\"replace_existing\": false, \"text\": \"shipping address\"}"`

## 24. w3v2_016_always_max_b96_r1_d10000

- sample_id: `w3v2_016`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `1292.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": false, "text": "shipping address"}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": false, "text": "billing address"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_016_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": false, \"text\": \"billing address\"}, got={\"replace_existing\": false, \"text\": \"shipping address\"}"`

## 25. w3v2_017_always_max_b96_r1_d2000

- sample_id: `w3v2_017`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2150.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Morning run", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "07:30", "vibrate": false}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Morning run", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "07:30", "vibrate": false}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_017_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 26. w3v2_018_always_max_b96_r1_d2000

- sample_id: `w3v2_018`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `1934.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "20:00", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "08:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_018_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"08:45\", \"vibrate\": true}, got={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"20:00\", \"vibrate\": true}"`

## 27. w3v2_018_always_max_b96_r1_d5000

- sample_id: `w3v2_018`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `1934.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "20:00", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "08:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_018_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"08:45\", \"vibrate\": true}, got={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"20:00\", \"vibrate\": true}"`

## 28. w3v2_018_always_max_b96_r1_d10000

- sample_id: `w3v2_018`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `1934.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "20:00", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "08:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_018_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"08:45\", \"vibrate\": true}, got={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"20:00\", \"vibrate\": true}"`

## 29. w3v2_019_always_max_b96_r1_d2000

- sample_id: `w3v2_019`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2434.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Airport", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "06:45", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Airport", "repeat_days": [], "time": "06:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_019_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Airport\", \"repeat_days\": [], \"time\": \"06:45\", \"vibrate\": true}, got={\"label\": \"Airport\", \"repeat_days\": [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", \"Sat\", \"Sun\"], \"time\": \"06:45\", \"vibrate\": true}"`

## 30. w3v2_019_always_max_b96_r1_d5000

- sample_id: `w3v2_019`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `2434.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Airport", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "06:45", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Airport", "repeat_days": [], "time": "06:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_019_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Airport\", \"repeat_days\": [], \"time\": \"06:45\", \"vibrate\": true}, got={\"label\": \"Airport\", \"repeat_days\": [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", \"Sat\", \"Sun\"], \"time\": \"06:45\", \"vibrate\": true}"`

## 31. w3v2_019_always_max_b96_r1_d10000

- sample_id: `w3v2_019`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `2434.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Airport", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "06:45", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Airport", "repeat_days": [], "time": "06:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_019_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Airport\", \"repeat_days\": [], \"time\": \"06:45\", \"vibrate\": true}, got={\"label\": \"Airport\", \"repeat_days\": [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", \"Sat\", \"Sun\"], \"time\": \"06:45\", \"vibrate\": true}"`

## 32. w3v2_020_always_max_b96_r1_d2000

- sample_id: `w3v2_020`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `1472.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 5, "label": "Kitchen tea", "sound": true}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 300, "label": "Kitchen tea", "sound": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_020_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 300, \"label\": \"Kitchen tea\", \"sound\": true}, got={\"duration_seconds\": 5, \"label\": \"Kitchen tea\", \"sound\": true}"`

## 33. w3v2_020_always_max_b96_r1_d5000

- sample_id: `w3v2_020`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `1472.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 5, "label": "Kitchen tea", "sound": true}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 300, "label": "Kitchen tea", "sound": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_020_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 300, \"label\": \"Kitchen tea\", \"sound\": true}, got={\"duration_seconds\": 5, \"label\": \"Kitchen tea\", \"sound\": true}"`

## 34. w3v2_020_always_max_b96_r1_d10000

- sample_id: `w3v2_020`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `1472.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 5, "label": "Kitchen tea", "sound": true}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 300, "label": "Kitchen tea", "sound": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_020_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 300, \"label\": \"Kitchen tea\", \"sound\": true}, got={\"duration_seconds\": 5, \"label\": \"Kitchen tea\", \"sound\": true}"`

## 35. w3v2_021_always_max_b96_r1_d2000

- sample_id: `w3v2_021`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `1608.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 120, "label": "Silent Stretch", "sound": false}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 120, "label": "Stretch", "sound": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_021_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 120, \"label\": \"Stretch\", \"sound\": false}, got={\"duration_seconds\": 120, \"label\": \"Silent Stretch\", \"sound\": false}"`

## 36. w3v2_021_always_max_b96_r1_d5000

- sample_id: `w3v2_021`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `1608.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 120, "label": "Silent Stretch", "sound": false}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 120, "label": "Stretch", "sound": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_021_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 120, \"label\": \"Stretch\", \"sound\": false}, got={\"duration_seconds\": 120, \"label\": \"Silent Stretch\", \"sound\": false}"`

## 37. w3v2_021_always_max_b96_r1_d10000

- sample_id: `w3v2_021`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `1608.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 120, "label": "Silent Stretch", "sound": false}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 120, "label": "Stretch", "sound": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_021_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 120, \"label\": \"Stretch\", \"sound\": false}, got={\"duration_seconds\": 120, \"label\": \"Silent Stretch\", \"sound\": false}"`

## 38. w3v2_022_always_max_b96_r1_d2000

- sample_id: `w3v2_022`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 1800}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-01 14:00", "title": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_022_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_timer"`

## 39. w3v2_022_always_max_b96_r1_d5000

- sample_id: `w3v2_022`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 1800}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-01 14:00", "title": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_022_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_timer"`

## 40. w3v2_022_always_max_b96_r1_d10000

- sample_id: `w3v2_022`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 1800}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-01 14:00", "title": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_022_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_timer"`

## 41. w3v2_023_always_max_b96_r1_d2000

- sample_id: `w3v2_023`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `3034.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Dentist Appointment", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "2026-08-03 09:15", "vibrate": false}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Dr. Lee"], "duration_minutes": 30, "online": false, "start_time": "2026-08-03 09:15", "title": "Dentist appointment"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_023_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_alarm"`

## 42. w3v2_023_always_max_b96_r1_d5000

- sample_id: `w3v2_023`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `3034.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Dentist Appointment", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "2026-08-03 09:15", "vibrate": false}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Dr. Lee"], "duration_minutes": 30, "online": false, "start_time": "2026-08-03 09:15", "title": "Dentist appointment"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_023_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_alarm"`

## 43. w3v2_023_always_max_b96_r1_d10000

- sample_id: `w3v2_023`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `3034.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Dentist Appointment", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "2026-08-03 09:15", "vibrate": false}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Dr. Lee"], "duration_minutes": 30, "online": false, "start_time": "2026-08-03 09:15", "title": "Dentist appointment"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_023_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_alarm"`

## 44. w3v2_024_always_max_b96_r1_d2000

- sample_id: `w3v2_024`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `NA`
- predicted arguments: `NA`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-10 14:30", "title": "Budget review"}`
- error_type: `parse_error`
- notes: `physical_run_id=w3v2_024_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="invalid JSON document: Extra data: line 2 column 1 (char 99)"`

## 45. w3v2_024_always_max_b96_r1_d5000

- sample_id: `w3v2_024`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `NA`
- predicted arguments: `NA`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-10 14:30", "title": "Budget review"}`
- error_type: `parse_error`
- notes: `physical_run_id=w3v2_024_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="invalid JSON document: Extra data: line 2 column 1 (char 99)"`

## 46. w3v2_024_always_max_b96_r1_d10000

- sample_id: `w3v2_024`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `NA`
- predicted arguments: `NA`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-10 14:30", "title": "Budget review"}`
- error_type: `parse_error`
- notes: `physical_run_id=w3v2_024_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="invalid JSON document: Extra data: line 2 column 1 (char 99)"`

## 47. w3v2_025_always_max_b96_r1_d2000

- sample_id: `w3v2_025`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `1493.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Alice", "text": "Server is back online.", "urgent": true}`
- gold action: `send_message`
- gold arguments: `{"contact": "Alice", "text": "Server is back online", "urgent": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_025_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Alice\", \"text\": \"Server is back online\", \"urgent\": true}, got={\"contact\": \"Alice\", \"text\": \"Server is back online.\", \"urgent\": true}"`

## 48. w3v2_025_always_max_b96_r1_d5000

- sample_id: `w3v2_025`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `1493.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Alice", "text": "Server is back online.", "urgent": true}`
- gold action: `send_message`
- gold arguments: `{"contact": "Alice", "text": "Server is back online", "urgent": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_025_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Alice\", \"text\": \"Server is back online\", \"urgent\": true}, got={\"contact\": \"Alice\", \"text\": \"Server is back online.\", \"urgent\": true}"`

## 49. w3v2_025_always_max_b96_r1_d10000

- sample_id: `w3v2_025`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `1493.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Alice", "text": "Server is back online.", "urgent": true}`
- gold action: `send_message`
- gold arguments: `{"contact": "Alice", "text": "Server is back online", "urgent": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_025_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Alice\", \"text\": \"Server is back online\", \"urgent\": true}, got={\"contact\": \"Alice\", \"text\": \"Server is back online.\", \"urgent\": true}"`

## 50. w3v2_026_always_max_b96_r1_d2000

- sample_id: `w3v2_026`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `1623.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Bob", "text": "I will arrive at seven. Sorry.", "urgent": false}`
- gold action: `send_message`
- gold arguments: `{"contact": "Bob", "text": "I will arrive at seven", "urgent": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_026_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Bob\", \"text\": \"I will arrive at seven\", \"urgent\": false}, got={\"contact\": \"Bob\", \"text\": \"I will arrive at seven. Sorry.\", \"urgent\": false}"`

## 51. w3v2_026_always_max_b96_r1_d5000

- sample_id: `w3v2_026`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `1623.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Bob", "text": "I will arrive at seven. Sorry.", "urgent": false}`
- gold action: `send_message`
- gold arguments: `{"contact": "Bob", "text": "I will arrive at seven", "urgent": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_026_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Bob\", \"text\": \"I will arrive at seven\", \"urgent\": false}, got={\"contact\": \"Bob\", \"text\": \"I will arrive at seven. Sorry.\", \"urgent\": false}"`

## 52. w3v2_026_always_max_b96_r1_d10000

- sample_id: `w3v2_026`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `1623.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Bob", "text": "I will arrive at seven. Sorry.", "urgent": false}`
- gold action: `send_message`
- gold arguments: `{"contact": "Bob", "text": "I will arrive at seven", "urgent": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_026_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Bob\", \"text\": \"I will arrive at seven\", \"urgent\": false}, got={\"contact\": \"Bob\", \"text\": \"I will arrive at seven. Sorry.\", \"urgent\": false}"`

## 53. w3v2_027_always_max_b96_r1_d2000

- sample_id: `w3v2_027`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `1862.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "The draft is attached.", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- gold action: `send_email`
- gold arguments: `{"body": "The draft is attached", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_027_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"body\": \"The draft is attached\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}, got={\"body\": \"The draft is attached.\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}"`

## 54. w3v2_027_always_max_b96_r1_d5000

- sample_id: `w3v2_027`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `1862.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "The draft is attached.", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- gold action: `send_email`
- gold arguments: `{"body": "The draft is attached", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_027_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"body\": \"The draft is attached\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}, got={\"body\": \"The draft is attached.\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}"`

## 55. w3v2_027_always_max_b96_r1_d10000

- sample_id: `w3v2_027`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `1862.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "The draft is attached.", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- gold action: `send_email`
- gold arguments: `{"body": "The draft is attached", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_027_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"body\": \"The draft is attached\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}, got={\"body\": \"The draft is attached.\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}"`

## 56. w3v2_028_always_max_b96_r1_d2000

- sample_id: `w3v2_028`
- performance_mode: `always_max`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "Meet in room 302", "body_replace": true, "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- gold action: `send_email`
- gold arguments: `{"body": "Meet in room 302", "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_028_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument keys mismatch for send_email; missing=[], extra=['body_replace']"`

## 57. w3v2_028_always_max_b96_r1_d5000

- sample_id: `w3v2_028`
- performance_mode: `always_max`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "Meet in room 302", "body_replace": true, "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- gold action: `send_email`
- gold arguments: `{"body": "Meet in room 302", "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_028_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument keys mismatch for send_email; missing=[], extra=['body_replace']"`

## 58. w3v2_028_always_max_b96_r1_d10000

- sample_id: `w3v2_028`
- performance_mode: `always_max`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "Meet in room 302", "body_replace": true, "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- gold action: `send_email`
- gold arguments: `{"body": "Meet in room 302", "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_028_always_max_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument keys mismatch for send_email; missing=[], extra=['body_replace']"`

## 59. w3v2_004_balanced_b96_r1_d2000

- sample_id: `w3v2_004`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2448.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "battery health tips", "result_limit": 5, "safe_search": true}`
- gold action: `search_web`
- gold arguments: `{"query": "battery health tips", "result_limit": 5, "safe_search": true}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_004_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 60. w3v2_005_balanced_b96_r1_d2000

- sample_id: `w3v2_005`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2041.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_contacts`
- predicted arguments: `{"favorites_only": false, "name": "Alice Chen"}`
- gold action: `search_contacts`
- gold arguments: `{"favorites_only": false, "name": "Alice Chen"}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_005_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 61. w3v2_006_balanced_b96_r1_d2000

- sample_id: `w3v2_006`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `3647.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Reminder", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "Mon-Fri 08:00", "vibrate": false}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 14, "keyword": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_006_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=search_calendar, got=set_alarm"`

## 62. w3v2_006_balanced_b96_r1_d5000

- sample_id: `w3v2_006`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `3647.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Reminder", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "Mon-Fri 08:00", "vibrate": false}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 14, "keyword": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_006_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=search_calendar, got=set_alarm"`

## 63. w3v2_006_balanced_b96_r1_d10000

- sample_id: `w3v2_006`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `3647.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Reminder", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "Mon-Fri 08:00", "vibrate": false}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 14, "keyword": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_006_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=search_calendar, got=set_alarm"`

## 64. w3v2_007_balanced_b96_r1_d2000

- sample_id: `w3v2_007`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": "off"}`
- gold action: `search_web`
- gold arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_007_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'safe_search' must have type boolean"`

## 65. w3v2_007_balanced_b96_r1_d5000

- sample_id: `w3v2_007`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": "off"}`
- gold action: `search_web`
- gold arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_007_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'safe_search' must have type boolean"`

## 66. w3v2_007_balanced_b96_r1_d10000

- sample_id: `w3v2_007`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": "off"}`
- gold action: `search_web`
- gold arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_007_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'safe_search' must have type boolean"`

## 67. w3v2_008_balanced_b96_r1_d2000

- sample_id: `w3v2_008`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_contacts`
- predicted arguments: `{"favorites_only": "true", "name": "Robert Wang"}`
- gold action: `search_contacts`
- gold arguments: `{"favorites_only": true, "name": "Robert Wang"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_008_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'favorites_only' must have type boolean"`

## 68. w3v2_008_balanced_b96_r1_d5000

- sample_id: `w3v2_008`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_contacts`
- predicted arguments: `{"favorites_only": "true", "name": "Robert Wang"}`
- gold action: `search_contacts`
- gold arguments: `{"favorites_only": true, "name": "Robert Wang"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_008_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'favorites_only' must have type boolean"`

## 69. w3v2_008_balanced_b96_r1_d10000

- sample_id: `w3v2_008`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_contacts`
- predicted arguments: `{"favorites_only": "true", "name": "Robert Wang"}`
- gold action: `search_contacts`
- gold arguments: `{"favorites_only": true, "name": "Robert Wang"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_008_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'favorites_only' must have type boolean"`

## 70. w3v2_009_balanced_b96_r1_d2000

- sample_id: `w3v2_009`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_calendar`
- predicted arguments: `{"days_ahead": "30", "keyword": "dentist"}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 30, "keyword": "dentist"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_009_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'days_ahead' must have type integer"`

## 71. w3v2_009_balanced_b96_r1_d5000

- sample_id: `w3v2_009`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_calendar`
- predicted arguments: `{"days_ahead": "30", "keyword": "dentist"}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 30, "keyword": "dentist"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_009_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'days_ahead' must have type integer"`

## 72. w3v2_009_balanced_b96_r1_d10000

- sample_id: `w3v2_009`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_calendar`
- predicted arguments: `{"days_ahead": "30", "keyword": "dentist"}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 30, "keyword": "dentist"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_009_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'days_ahead' must have type integer"`

## 73. w3v2_010_balanced_b96_r1_d2000

- sample_id: `w3v2_010`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2504.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_app_store`
- predicted arguments: `{"app_query": "photo editor", "free_only": true, "max_results": 6}`
- gold action: `search_app_store`
- gold arguments: `{"app_query": "photo editor", "free_only": true, "max_results": 6}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_010_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 74. w3v2_011_balanced_b96_r1_d2000

- sample_id: `w3v2_011`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2729.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_app_store`
- predicted arguments: `{"app_query": "radar weather", "free_only": false, "max_results": 4}`
- gold action: `search_app_store`
- gold arguments: `{"app_query": "radar weather", "free_only": false, "max_results": 4}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_011_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 75. w3v2_012_balanced_b96_r1_d2000

- sample_id: `w3v2_012`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": 1, "element_id": "Continue", "visible_only": true}`
- gold action: `find_ui_element`
- gold arguments: `{"description": "Continue button", "visible_only": true}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_012_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=find_ui_element, got=click_element"`

## 76. w3v2_012_balanced_b96_r1_d5000

- sample_id: `w3v2_012`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": 1, "element_id": "Continue", "visible_only": true}`
- gold action: `find_ui_element`
- gold arguments: `{"description": "Continue button", "visible_only": true}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_012_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=find_ui_element, got=click_element"`

## 77. w3v2_012_balanced_b96_r1_d10000

- sample_id: `w3v2_012`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": 1, "element_id": "Continue", "visible_only": true}`
- gold action: `find_ui_element`
- gold arguments: `{"description": "Continue button", "visible_only": true}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_012_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=find_ui_element, got=click_element"`

## 78. w3v2_013_balanced_b96_r1_d2000

- sample_id: `w3v2_013`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": "2", "element_id": "result_42"}`
- gold action: `click_element`
- gold arguments: `{"click_count": 2, "element_id": "result_42"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_013_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'click_count' must have type integer"`

## 79. w3v2_013_balanced_b96_r1_d5000

- sample_id: `w3v2_013`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": "2", "element_id": "result_42"}`
- gold action: `click_element`
- gold arguments: `{"click_count": 2, "element_id": "result_42"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_013_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'click_count' must have type integer"`

## 80. w3v2_013_balanced_b96_r1_d10000

- sample_id: `w3v2_013`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": "2", "element_id": "result_42"}`
- gold action: `click_element`
- gold arguments: `{"click_count": 2, "element_id": "result_42"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_013_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'click_count' must have type integer"`

## 81. w3v2_014_balanced_b96_r1_d2000

- sample_id: `w3v2_014`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2110.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": 1, "element_id": "confirm_new"}`
- gold action: `click_element`
- gold arguments: `{"click_count": 1, "element_id": "confirm_new"}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_014_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 82. w3v2_015_balanced_b96_r1_d2000

- sample_id: `w3v2_015`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2494.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": true, "text": "meeting moved to room 302."}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": true, "text": "meeting moved to room 302"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_015_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": true, \"text\": \"meeting moved to room 302\"}, got={\"replace_existing\": true, \"text\": \"meeting moved to room 302.\"}"`

## 83. w3v2_015_balanced_b96_r1_d5000

- sample_id: `w3v2_015`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `2494.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": true, "text": "meeting moved to room 302."}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": true, "text": "meeting moved to room 302"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_015_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": true, \"text\": \"meeting moved to room 302\"}, got={\"replace_existing\": true, \"text\": \"meeting moved to room 302.\"}"`

## 84. w3v2_015_balanced_b96_r1_d10000

- sample_id: `w3v2_015`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `2494.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": true, "text": "meeting moved to room 302."}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": true, "text": "meeting moved to room 302"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_015_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": true, \"text\": \"meeting moved to room 302\"}, got={\"replace_existing\": true, \"text\": \"meeting moved to room 302.\"}"`

## 85. w3v2_016_balanced_b96_r1_d2000

- sample_id: `w3v2_016`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2047.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": false, "text": "shipping address"}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": false, "text": "billing address"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_016_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": false, \"text\": \"billing address\"}, got={\"replace_existing\": false, \"text\": \"shipping address\"}"`

## 86. w3v2_016_balanced_b96_r1_d5000

- sample_id: `w3v2_016`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `2047.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": false, "text": "shipping address"}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": false, "text": "billing address"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_016_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": false, \"text\": \"billing address\"}, got={\"replace_existing\": false, \"text\": \"shipping address\"}"`

## 87. w3v2_016_balanced_b96_r1_d10000

- sample_id: `w3v2_016`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `2047.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": false, "text": "shipping address"}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": false, "text": "billing address"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_016_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": false, \"text\": \"billing address\"}, got={\"replace_existing\": false, \"text\": \"shipping address\"}"`

## 88. w3v2_017_balanced_b96_r1_d2000

- sample_id: `w3v2_017`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `3416.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Morning run", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "07:30", "vibrate": false}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Morning run", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "07:30", "vibrate": false}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_017_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 89. w3v2_018_balanced_b96_r1_d2000

- sample_id: `w3v2_018`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `3020.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "20:00", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "08:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_018_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"08:45\", \"vibrate\": true}, got={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"20:00\", \"vibrate\": true}"`

## 90. w3v2_018_balanced_b96_r1_d5000

- sample_id: `w3v2_018`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `3020.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "20:00", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "08:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_018_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"08:45\", \"vibrate\": true}, got={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"20:00\", \"vibrate\": true}"`

## 91. w3v2_018_balanced_b96_r1_d10000

- sample_id: `w3v2_018`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `3020.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "20:00", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "08:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_018_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"08:45\", \"vibrate\": true}, got={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"20:00\", \"vibrate\": true}"`

## 92. w3v2_019_balanced_b96_r1_d2000

- sample_id: `w3v2_019`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `3883.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Airport", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "06:45", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Airport", "repeat_days": [], "time": "06:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_019_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Airport\", \"repeat_days\": [], \"time\": \"06:45\", \"vibrate\": true}, got={\"label\": \"Airport\", \"repeat_days\": [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", \"Sat\", \"Sun\"], \"time\": \"06:45\", \"vibrate\": true}"`

## 93. w3v2_019_balanced_b96_r1_d5000

- sample_id: `w3v2_019`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `3883.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Airport", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "06:45", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Airport", "repeat_days": [], "time": "06:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_019_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Airport\", \"repeat_days\": [], \"time\": \"06:45\", \"vibrate\": true}, got={\"label\": \"Airport\", \"repeat_days\": [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", \"Sat\", \"Sun\"], \"time\": \"06:45\", \"vibrate\": true}"`

## 94. w3v2_019_balanced_b96_r1_d10000

- sample_id: `w3v2_019`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `3883.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Airport", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "06:45", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Airport", "repeat_days": [], "time": "06:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_019_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Airport\", \"repeat_days\": [], \"time\": \"06:45\", \"vibrate\": true}, got={\"label\": \"Airport\", \"repeat_days\": [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", \"Sat\", \"Sun\"], \"time\": \"06:45\", \"vibrate\": true}"`

## 95. w3v2_020_balanced_b96_r1_d2000

- sample_id: `w3v2_020`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2296.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 5, "label": "Kitchen tea", "sound": true}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 300, "label": "Kitchen tea", "sound": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_020_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 300, \"label\": \"Kitchen tea\", \"sound\": true}, got={\"duration_seconds\": 5, \"label\": \"Kitchen tea\", \"sound\": true}"`

## 96. w3v2_020_balanced_b96_r1_d5000

- sample_id: `w3v2_020`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `2296.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 5, "label": "Kitchen tea", "sound": true}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 300, "label": "Kitchen tea", "sound": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_020_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 300, \"label\": \"Kitchen tea\", \"sound\": true}, got={\"duration_seconds\": 5, \"label\": \"Kitchen tea\", \"sound\": true}"`

## 97. w3v2_020_balanced_b96_r1_d10000

- sample_id: `w3v2_020`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `2296.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 5, "label": "Kitchen tea", "sound": true}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 300, "label": "Kitchen tea", "sound": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_020_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 300, \"label\": \"Kitchen tea\", \"sound\": true}, got={\"duration_seconds\": 5, \"label\": \"Kitchen tea\", \"sound\": true}"`

## 98. w3v2_021_balanced_b96_r1_d2000

- sample_id: `w3v2_021`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2513.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 120, "label": "Silent Stretch", "sound": false}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 120, "label": "Stretch", "sound": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_021_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 120, \"label\": \"Stretch\", \"sound\": false}, got={\"duration_seconds\": 120, \"label\": \"Silent Stretch\", \"sound\": false}"`

## 99. w3v2_021_balanced_b96_r1_d5000

- sample_id: `w3v2_021`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `2513.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 120, "label": "Silent Stretch", "sound": false}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 120, "label": "Stretch", "sound": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_021_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 120, \"label\": \"Stretch\", \"sound\": false}, got={\"duration_seconds\": 120, \"label\": \"Silent Stretch\", \"sound\": false}"`

## 100. w3v2_021_balanced_b96_r1_d10000

- sample_id: `w3v2_021`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `2513.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 120, "label": "Silent Stretch", "sound": false}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 120, "label": "Stretch", "sound": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_021_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 120, \"label\": \"Stretch\", \"sound\": false}, got={\"duration_seconds\": 120, \"label\": \"Silent Stretch\", \"sound\": false}"`

## 101. w3v2_022_balanced_b96_r1_d2000

- sample_id: `w3v2_022`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 1800}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-01 14:00", "title": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_022_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_timer"`

## 102. w3v2_022_balanced_b96_r1_d5000

- sample_id: `w3v2_022`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 1800}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-01 14:00", "title": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_022_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_timer"`

## 103. w3v2_022_balanced_b96_r1_d10000

- sample_id: `w3v2_022`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 1800}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-01 14:00", "title": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_022_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_timer"`

## 104. w3v2_023_balanced_b96_r1_d2000

- sample_id: `w3v2_023`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `4830.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Dentist Appointment", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "2026-08-03 09:15", "vibrate": false}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Dr. Lee"], "duration_minutes": 30, "online": false, "start_time": "2026-08-03 09:15", "title": "Dentist appointment"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_023_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_alarm"`

## 105. w3v2_023_balanced_b96_r1_d5000

- sample_id: `w3v2_023`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `4830.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Dentist Appointment", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "2026-08-03 09:15", "vibrate": false}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Dr. Lee"], "duration_minutes": 30, "online": false, "start_time": "2026-08-03 09:15", "title": "Dentist appointment"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_023_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_alarm"`

## 106. w3v2_023_balanced_b96_r1_d10000

- sample_id: `w3v2_023`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `4830.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Dentist Appointment", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "2026-08-03 09:15", "vibrate": false}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Dr. Lee"], "duration_minutes": 30, "online": false, "start_time": "2026-08-03 09:15", "title": "Dentist appointment"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_023_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_alarm"`

## 107. w3v2_024_balanced_b96_r1_d2000

- sample_id: `w3v2_024`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `NA`
- predicted arguments: `NA`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-10 14:30", "title": "Budget review"}`
- error_type: `parse_error`
- notes: `physical_run_id=w3v2_024_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="invalid JSON document: Extra data: line 2 column 1 (char 99)"`

## 108. w3v2_024_balanced_b96_r1_d5000

- sample_id: `w3v2_024`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `NA`
- predicted arguments: `NA`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-10 14:30", "title": "Budget review"}`
- error_type: `parse_error`
- notes: `physical_run_id=w3v2_024_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="invalid JSON document: Extra data: line 2 column 1 (char 99)"`

## 109. w3v2_024_balanced_b96_r1_d10000

- sample_id: `w3v2_024`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `NA`
- predicted arguments: `NA`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-10 14:30", "title": "Budget review"}`
- error_type: `parse_error`
- notes: `physical_run_id=w3v2_024_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="invalid JSON document: Extra data: line 2 column 1 (char 99)"`

## 110. w3v2_025_balanced_b96_r1_d2000

- sample_id: `w3v2_025`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2378.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Alice", "text": "Server is back online.", "urgent": true}`
- gold action: `send_message`
- gold arguments: `{"contact": "Alice", "text": "Server is back online", "urgent": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_025_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Alice\", \"text\": \"Server is back online\", \"urgent\": true}, got={\"contact\": \"Alice\", \"text\": \"Server is back online.\", \"urgent\": true}"`

## 111. w3v2_025_balanced_b96_r1_d5000

- sample_id: `w3v2_025`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `2378.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Alice", "text": "Server is back online.", "urgent": true}`
- gold action: `send_message`
- gold arguments: `{"contact": "Alice", "text": "Server is back online", "urgent": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_025_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Alice\", \"text\": \"Server is back online\", \"urgent\": true}, got={\"contact\": \"Alice\", \"text\": \"Server is back online.\", \"urgent\": true}"`

## 112. w3v2_025_balanced_b96_r1_d10000

- sample_id: `w3v2_025`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `2378.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Alice", "text": "Server is back online.", "urgent": true}`
- gold action: `send_message`
- gold arguments: `{"contact": "Alice", "text": "Server is back online", "urgent": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_025_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Alice\", \"text\": \"Server is back online\", \"urgent\": true}, got={\"contact\": \"Alice\", \"text\": \"Server is back online.\", \"urgent\": true}"`

## 113. w3v2_026_balanced_b96_r1_d2000

- sample_id: `w3v2_026`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2582.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Bob", "text": "I will arrive at seven. Sorry.", "urgent": false}`
- gold action: `send_message`
- gold arguments: `{"contact": "Bob", "text": "I will arrive at seven", "urgent": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_026_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Bob\", \"text\": \"I will arrive at seven\", \"urgent\": false}, got={\"contact\": \"Bob\", \"text\": \"I will arrive at seven. Sorry.\", \"urgent\": false}"`

## 114. w3v2_026_balanced_b96_r1_d5000

- sample_id: `w3v2_026`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `2582.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Bob", "text": "I will arrive at seven. Sorry.", "urgent": false}`
- gold action: `send_message`
- gold arguments: `{"contact": "Bob", "text": "I will arrive at seven", "urgent": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_026_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Bob\", \"text\": \"I will arrive at seven\", \"urgent\": false}, got={\"contact\": \"Bob\", \"text\": \"I will arrive at seven. Sorry.\", \"urgent\": false}"`

## 115. w3v2_026_balanced_b96_r1_d10000

- sample_id: `w3v2_026`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `2582.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Bob", "text": "I will arrive at seven. Sorry.", "urgent": false}`
- gold action: `send_message`
- gold arguments: `{"contact": "Bob", "text": "I will arrive at seven", "urgent": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_026_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Bob\", \"text\": \"I will arrive at seven\", \"urgent\": false}, got={\"contact\": \"Bob\", \"text\": \"I will arrive at seven. Sorry.\", \"urgent\": false}"`

## 116. w3v2_027_balanced_b96_r1_d2000

- sample_id: `w3v2_027`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2921.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "The draft is attached.", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- gold action: `send_email`
- gold arguments: `{"body": "The draft is attached", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_027_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"body\": \"The draft is attached\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}, got={\"body\": \"The draft is attached.\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}"`

## 117. w3v2_027_balanced_b96_r1_d5000

- sample_id: `w3v2_027`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `2921.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "The draft is attached.", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- gold action: `send_email`
- gold arguments: `{"body": "The draft is attached", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_027_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"body\": \"The draft is attached\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}, got={\"body\": \"The draft is attached.\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}"`

## 118. w3v2_027_balanced_b96_r1_d10000

- sample_id: `w3v2_027`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `2921.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "The draft is attached.", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- gold action: `send_email`
- gold arguments: `{"body": "The draft is attached", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_027_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"body\": \"The draft is attached\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}, got={\"body\": \"The draft is attached.\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}"`

## 119. w3v2_028_balanced_b96_r1_d2000

- sample_id: `w3v2_028`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "Meet in room 302", "body_replace": true, "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- gold action: `send_email`
- gold arguments: `{"body": "Meet in room 302", "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_028_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument keys mismatch for send_email; missing=[], extra=['body_replace']"`

## 120. w3v2_028_balanced_b96_r1_d5000

- sample_id: `w3v2_028`
- performance_mode: `balanced`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "Meet in room 302", "body_replace": true, "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- gold action: `send_email`
- gold arguments: `{"body": "Meet in room 302", "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_028_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument keys mismatch for send_email; missing=[], extra=['body_replace']"`

## 121. w3v2_028_balanced_b96_r1_d10000

- sample_id: `w3v2_028`
- performance_mode: `balanced`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "Meet in room 302", "body_replace": true, "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- gold action: `send_email`
- gold arguments: `{"body": "Meet in room 302", "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_028_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument keys mismatch for send_email; missing=[], extra=['body_replace']"`

## 122. w3v2_029_balanced_b96_r1_d2000

- sample_id: `w3v2_029`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2445.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "nearest train station", "result_limit": 8, "safe_search": false}`
- gold action: `search_web`
- gold arguments: `{"query": "nearest train station", "result_limit": 8, "safe_search": false}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_029_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 123. w3v2_030_balanced_b96_r1_d2000

- sample_id: `w3v2_030`
- performance_mode: `balanced`
- deadline_ms: `2000`
- time_to_valid_action_ms: `2110.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `find_ui_element`
- predicted arguments: `{"description": "Settings icon", "visible_only": false}`
- gold action: `find_ui_element`
- gold arguments: `{"description": "Settings icon", "visible_only": false}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_030_balanced_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 124. w3v2_001_low_saver_b96_r1_d2000

- sample_id: `w3v2_001`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `3614.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `open_app`
- predicted arguments: `{"app_name": "Calculator"}`
- gold action: `open_app`
- gold arguments: `{"app_name": "Calculator"}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_001_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 125. w3v2_002_low_saver_b96_r1_d2000

- sample_id: `w3v2_002`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `4046.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `open_url`
- predicted arguments: `{"url": "https://weather.example.com"}`
- gold action: `open_url`
- gold arguments: `{"url": "https://weather.example.com"}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_002_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 126. w3v2_003_low_saver_b96_r1_d2000

- sample_id: `w3v2_003`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `3560.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `open_app`
- predicted arguments: `{"app_name": "Calculator"}`
- gold action: `open_app`
- gold arguments: `{"app_name": "Calculator"}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_003_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 127. w3v2_004_low_saver_b96_r1_d2000

- sample_id: `w3v2_004`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `5193.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "battery health tips", "result_limit": 5, "safe_search": true}`
- gold action: `search_web`
- gold arguments: `{"query": "battery health tips", "result_limit": 5, "safe_search": true}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_004_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 128. w3v2_004_low_saver_b96_r1_d5000

- sample_id: `w3v2_004`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `5193.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "battery health tips", "result_limit": 5, "safe_search": true}`
- gold action: `search_web`
- gold arguments: `{"query": "battery health tips", "result_limit": 5, "safe_search": true}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_004_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 129. w3v2_005_low_saver_b96_r1_d2000

- sample_id: `w3v2_005`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `4321.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_contacts`
- predicted arguments: `{"favorites_only": false, "name": "Alice Chen"}`
- gold action: `search_contacts`
- gold arguments: `{"favorites_only": false, "name": "Alice Chen"}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_005_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 130. w3v2_006_low_saver_b96_r1_d2000

- sample_id: `w3v2_006`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `7596.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Reminder", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "Mon-Fri 08:00", "vibrate": false}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 14, "keyword": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_006_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=search_calendar, got=set_alarm"`

## 131. w3v2_006_low_saver_b96_r1_d5000

- sample_id: `w3v2_006`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `7596.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Reminder", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "Mon-Fri 08:00", "vibrate": false}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 14, "keyword": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_006_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=search_calendar, got=set_alarm"`

## 132. w3v2_006_low_saver_b96_r1_d10000

- sample_id: `w3v2_006`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `7596.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Reminder", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "Mon-Fri 08:00", "vibrate": false}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 14, "keyword": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_006_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=search_calendar, got=set_alarm"`

## 133. w3v2_007_low_saver_b96_r1_d2000

- sample_id: `w3v2_007`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": "off"}`
- gold action: `search_web`
- gold arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_007_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'safe_search' must have type boolean"`

## 134. w3v2_007_low_saver_b96_r1_d5000

- sample_id: `w3v2_007`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": "off"}`
- gold action: `search_web`
- gold arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_007_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'safe_search' must have type boolean"`

## 135. w3v2_007_low_saver_b96_r1_d10000

- sample_id: `w3v2_007`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": "off"}`
- gold action: `search_web`
- gold arguments: `{"query": "Alice Chen biography", "result_limit": 3, "safe_search": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_007_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'safe_search' must have type boolean"`

## 136. w3v2_008_low_saver_b96_r1_d2000

- sample_id: `w3v2_008`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_contacts`
- predicted arguments: `{"favorites_only": "true", "name": "Robert Wang"}`
- gold action: `search_contacts`
- gold arguments: `{"favorites_only": true, "name": "Robert Wang"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_008_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'favorites_only' must have type boolean"`

## 137. w3v2_008_low_saver_b96_r1_d5000

- sample_id: `w3v2_008`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_contacts`
- predicted arguments: `{"favorites_only": "true", "name": "Robert Wang"}`
- gold action: `search_contacts`
- gold arguments: `{"favorites_only": true, "name": "Robert Wang"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_008_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'favorites_only' must have type boolean"`

## 138. w3v2_008_low_saver_b96_r1_d10000

- sample_id: `w3v2_008`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_contacts`
- predicted arguments: `{"favorites_only": "true", "name": "Robert Wang"}`
- gold action: `search_contacts`
- gold arguments: `{"favorites_only": true, "name": "Robert Wang"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_008_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'favorites_only' must have type boolean"`

## 139. w3v2_009_low_saver_b96_r1_d2000

- sample_id: `w3v2_009`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_calendar`
- predicted arguments: `{"days_ahead": "30", "keyword": "dentist"}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 30, "keyword": "dentist"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_009_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'days_ahead' must have type integer"`

## 140. w3v2_009_low_saver_b96_r1_d5000

- sample_id: `w3v2_009`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_calendar`
- predicted arguments: `{"days_ahead": "30", "keyword": "dentist"}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 30, "keyword": "dentist"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_009_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'days_ahead' must have type integer"`

## 141. w3v2_009_low_saver_b96_r1_d10000

- sample_id: `w3v2_009`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `search_calendar`
- predicted arguments: `{"days_ahead": "30", "keyword": "dentist"}`
- gold action: `search_calendar`
- gold arguments: `{"days_ahead": 30, "keyword": "dentist"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_009_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'days_ahead' must have type integer"`

## 142. w3v2_010_low_saver_b96_r1_d2000

- sample_id: `w3v2_010`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `5314.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_app_store`
- predicted arguments: `{"app_query": "photo editor", "free_only": true, "max_results": 6}`
- gold action: `search_app_store`
- gold arguments: `{"app_query": "photo editor", "free_only": true, "max_results": 6}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_010_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 143. w3v2_010_low_saver_b96_r1_d5000

- sample_id: `w3v2_010`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `5314.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_app_store`
- predicted arguments: `{"app_query": "photo editor", "free_only": true, "max_results": 6}`
- gold action: `search_app_store`
- gold arguments: `{"app_query": "photo editor", "free_only": true, "max_results": 6}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_010_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 144. w3v2_011_low_saver_b96_r1_d2000

- sample_id: `w3v2_011`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `5763.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_app_store`
- predicted arguments: `{"app_query": "radar weather", "free_only": false, "max_results": 4}`
- gold action: `search_app_store`
- gold arguments: `{"app_query": "radar weather", "free_only": false, "max_results": 4}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_011_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 145. w3v2_011_low_saver_b96_r1_d5000

- sample_id: `w3v2_011`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `5763.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_app_store`
- predicted arguments: `{"app_query": "radar weather", "free_only": false, "max_results": 4}`
- gold action: `search_app_store`
- gold arguments: `{"app_query": "radar weather", "free_only": false, "max_results": 4}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_011_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 146. w3v2_012_low_saver_b96_r1_d2000

- sample_id: `w3v2_012`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": 1, "element_id": "Continue", "visible_only": true}`
- gold action: `find_ui_element`
- gold arguments: `{"description": "Continue button", "visible_only": true}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_012_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=find_ui_element, got=click_element"`

## 147. w3v2_012_low_saver_b96_r1_d5000

- sample_id: `w3v2_012`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": 1, "element_id": "Continue", "visible_only": true}`
- gold action: `find_ui_element`
- gold arguments: `{"description": "Continue button", "visible_only": true}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_012_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=find_ui_element, got=click_element"`

## 148. w3v2_012_low_saver_b96_r1_d10000

- sample_id: `w3v2_012`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": 1, "element_id": "Continue", "visible_only": true}`
- gold action: `find_ui_element`
- gold arguments: `{"description": "Continue button", "visible_only": true}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_012_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=find_ui_element, got=click_element"`

## 149. w3v2_013_low_saver_b96_r1_d2000

- sample_id: `w3v2_013`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": "2", "element_id": "result_42"}`
- gold action: `click_element`
- gold arguments: `{"click_count": 2, "element_id": "result_42"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_013_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'click_count' must have type integer"`

## 150. w3v2_013_low_saver_b96_r1_d5000

- sample_id: `w3v2_013`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": "2", "element_id": "result_42"}`
- gold action: `click_element`
- gold arguments: `{"click_count": 2, "element_id": "result_42"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_013_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'click_count' must have type integer"`

## 151. w3v2_013_low_saver_b96_r1_d10000

- sample_id: `w3v2_013`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": "2", "element_id": "result_42"}`
- gold action: `click_element`
- gold arguments: `{"click_count": 2, "element_id": "result_42"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_013_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument 'click_count' must have type integer"`

## 152. w3v2_014_low_saver_b96_r1_d2000

- sample_id: `w3v2_014`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `4449.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `click_element`
- predicted arguments: `{"click_count": 1, "element_id": "confirm_new"}`
- gold action: `click_element`
- gold arguments: `{"click_count": 1, "element_id": "confirm_new"}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_014_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 153. w3v2_015_low_saver_b96_r1_d2000

- sample_id: `w3v2_015`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `5313.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": true, "text": "meeting moved to room 302."}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": true, "text": "meeting moved to room 302"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_015_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": true, \"text\": \"meeting moved to room 302\"}, got={\"replace_existing\": true, \"text\": \"meeting moved to room 302.\"}"`

## 154. w3v2_015_low_saver_b96_r1_d5000

- sample_id: `w3v2_015`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `5313.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": true, "text": "meeting moved to room 302."}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": true, "text": "meeting moved to room 302"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_015_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": true, \"text\": \"meeting moved to room 302\"}, got={\"replace_existing\": true, \"text\": \"meeting moved to room 302.\"}"`

## 155. w3v2_015_low_saver_b96_r1_d10000

- sample_id: `w3v2_015`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `5313.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": true, "text": "meeting moved to room 302."}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": true, "text": "meeting moved to room 302"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_015_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": true, \"text\": \"meeting moved to room 302\"}, got={\"replace_existing\": true, \"text\": \"meeting moved to room 302.\"}"`

## 156. w3v2_016_low_saver_b96_r1_d2000

- sample_id: `w3v2_016`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `4293.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": false, "text": "shipping address"}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": false, "text": "billing address"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_016_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": false, \"text\": \"billing address\"}, got={\"replace_existing\": false, \"text\": \"shipping address\"}"`

## 157. w3v2_016_low_saver_b96_r1_d5000

- sample_id: `w3v2_016`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `4293.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": false, "text": "shipping address"}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": false, "text": "billing address"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_016_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": false, \"text\": \"billing address\"}, got={\"replace_existing\": false, \"text\": \"shipping address\"}"`

## 158. w3v2_016_low_saver_b96_r1_d10000

- sample_id: `w3v2_016`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `4293.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `type_text`
- predicted arguments: `{"replace_existing": false, "text": "shipping address"}`
- gold action: `type_text`
- gold arguments: `{"replace_existing": false, "text": "billing address"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_016_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"replace_existing\": false, \"text\": \"billing address\"}, got={\"replace_existing\": false, \"text\": \"shipping address\"}"`

## 159. w3v2_017_low_saver_b96_r1_d2000

- sample_id: `w3v2_017`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `7234.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Morning run", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "07:30", "vibrate": false}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Morning run", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "07:30", "vibrate": false}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_017_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 160. w3v2_017_low_saver_b96_r1_d5000

- sample_id: `w3v2_017`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `7234.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Morning run", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "07:30", "vibrate": false}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Morning run", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri"], "time": "07:30", "vibrate": false}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_017_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 161. w3v2_018_low_saver_b96_r1_d2000

- sample_id: `w3v2_018`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `6301.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "20:00", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "08:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_018_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"08:45\", \"vibrate\": true}, got={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"20:00\", \"vibrate\": true}"`

## 162. w3v2_018_low_saver_b96_r1_d5000

- sample_id: `w3v2_018`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `6301.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "20:00", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "08:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_018_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"08:45\", \"vibrate\": true}, got={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"20:00\", \"vibrate\": true}"`

## 163. w3v2_018_low_saver_b96_r1_d10000

- sample_id: `w3v2_018`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `6301.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "20:00", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Yoga", "repeat_days": ["Sat", "Sun"], "time": "08:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_018_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"08:45\", \"vibrate\": true}, got={\"label\": \"Yoga\", \"repeat_days\": [\"Sat\", \"Sun\"], \"time\": \"20:00\", \"vibrate\": true}"`

## 164. w3v2_019_low_saver_b96_r1_d2000

- sample_id: `w3v2_019`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `8191.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Airport", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "06:45", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Airport", "repeat_days": [], "time": "06:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_019_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Airport\", \"repeat_days\": [], \"time\": \"06:45\", \"vibrate\": true}, got={\"label\": \"Airport\", \"repeat_days\": [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", \"Sat\", \"Sun\"], \"time\": \"06:45\", \"vibrate\": true}"`

## 165. w3v2_019_low_saver_b96_r1_d5000

- sample_id: `w3v2_019`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `8191.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Airport", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "06:45", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Airport", "repeat_days": [], "time": "06:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_019_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Airport\", \"repeat_days\": [], \"time\": \"06:45\", \"vibrate\": true}, got={\"label\": \"Airport\", \"repeat_days\": [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", \"Sat\", \"Sun\"], \"time\": \"06:45\", \"vibrate\": true}"`

## 166. w3v2_019_low_saver_b96_r1_d10000

- sample_id: `w3v2_019`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `8191.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Airport", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "06:45", "vibrate": true}`
- gold action: `set_alarm`
- gold arguments: `{"label": "Airport", "repeat_days": [], "time": "06:45", "vibrate": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_019_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"label\": \"Airport\", \"repeat_days\": [], \"time\": \"06:45\", \"vibrate\": true}, got={\"label\": \"Airport\", \"repeat_days\": [\"Mon\", \"Tue\", \"Wed\", \"Thu\", \"Fri\", \"Sat\", \"Sun\"], \"time\": \"06:45\", \"vibrate\": true}"`

## 167. w3v2_020_low_saver_b96_r1_d2000

- sample_id: `w3v2_020`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `4711.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 5, "label": "Kitchen tea", "sound": true}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 300, "label": "Kitchen tea", "sound": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_020_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 300, \"label\": \"Kitchen tea\", \"sound\": true}, got={\"duration_seconds\": 5, \"label\": \"Kitchen tea\", \"sound\": true}"`

## 168. w3v2_020_low_saver_b96_r1_d5000

- sample_id: `w3v2_020`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `4711.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 5, "label": "Kitchen tea", "sound": true}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 300, "label": "Kitchen tea", "sound": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_020_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 300, \"label\": \"Kitchen tea\", \"sound\": true}, got={\"duration_seconds\": 5, \"label\": \"Kitchen tea\", \"sound\": true}"`

## 169. w3v2_020_low_saver_b96_r1_d10000

- sample_id: `w3v2_020`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `4711.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 5, "label": "Kitchen tea", "sound": true}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 300, "label": "Kitchen tea", "sound": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_020_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 300, \"label\": \"Kitchen tea\", \"sound\": true}, got={\"duration_seconds\": 5, \"label\": \"Kitchen tea\", \"sound\": true}"`

## 170. w3v2_021_low_saver_b96_r1_d2000

- sample_id: `w3v2_021`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `5258.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 120, "label": "Silent Stretch", "sound": false}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 120, "label": "Stretch", "sound": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_021_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 120, \"label\": \"Stretch\", \"sound\": false}, got={\"duration_seconds\": 120, \"label\": \"Silent Stretch\", \"sound\": false}"`

## 171. w3v2_021_low_saver_b96_r1_d5000

- sample_id: `w3v2_021`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `5258.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 120, "label": "Silent Stretch", "sound": false}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 120, "label": "Stretch", "sound": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_021_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 120, \"label\": \"Stretch\", \"sound\": false}, got={\"duration_seconds\": 120, \"label\": \"Silent Stretch\", \"sound\": false}"`

## 172. w3v2_021_low_saver_b96_r1_d10000

- sample_id: `w3v2_021`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `5258.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 120, "label": "Silent Stretch", "sound": false}`
- gold action: `set_timer`
- gold arguments: `{"duration_seconds": 120, "label": "Stretch", "sound": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_021_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"duration_seconds\": 120, \"label\": \"Stretch\", \"sound\": false}, got={\"duration_seconds\": 120, \"label\": \"Silent Stretch\", \"sound\": false}"`

## 173. w3v2_022_low_saver_b96_r1_d2000

- sample_id: `w3v2_022`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 1800}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-01 14:00", "title": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_022_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_timer"`

## 174. w3v2_022_low_saver_b96_r1_d5000

- sample_id: `w3v2_022`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 1800}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-01 14:00", "title": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_022_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_timer"`

## 175. w3v2_022_low_saver_b96_r1_d10000

- sample_id: `w3v2_022`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_timer`
- predicted arguments: `{"duration_seconds": 1800}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-01 14:00", "title": "Project review"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_022_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_timer"`

## 176. w3v2_023_low_saver_b96_r1_d2000

- sample_id: `w3v2_023`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `10070.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Dentist Appointment", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "2026-08-03 09:15", "vibrate": false}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Dr. Lee"], "duration_minutes": 30, "online": false, "start_time": "2026-08-03 09:15", "title": "Dentist appointment"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_023_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_alarm"`

## 177. w3v2_023_low_saver_b96_r1_d5000

- sample_id: `w3v2_023`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `10070.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Dentist Appointment", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "2026-08-03 09:15", "vibrate": false}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Dr. Lee"], "duration_minutes": 30, "online": false, "start_time": "2026-08-03 09:15", "title": "Dentist appointment"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_023_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_alarm"`

## 178. w3v2_023_low_saver_b96_r1_d10000

- sample_id: `w3v2_023`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `10070.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `set_alarm`
- predicted arguments: `{"label": "Dentist Appointment", "repeat_days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "time": "2026-08-03 09:15", "vibrate": false}`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Dr. Lee"], "duration_minutes": 30, "online": false, "start_time": "2026-08-03 09:15", "title": "Dentist appointment"}`
- error_type: `wrong_action_type`
- notes: `physical_run_id=w3v2_023_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected action=add_calendar_event, got=set_alarm"`

## 179. w3v2_024_low_saver_b96_r1_d2000

- sample_id: `w3v2_024`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `NA`
- predicted arguments: `NA`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-10 14:30", "title": "Budget review"}`
- error_type: `parse_error`
- notes: `physical_run_id=w3v2_024_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="invalid JSON document: Extra data: line 2 column 1 (char 99)"`

## 180. w3v2_024_low_saver_b96_r1_d5000

- sample_id: `w3v2_024`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `NA`
- predicted arguments: `NA`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-10 14:30", "title": "Budget review"}`
- error_type: `parse_error`
- notes: `physical_run_id=w3v2_024_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="invalid JSON document: Extra data: line 2 column 1 (char 99)"`

## 181. w3v2_024_low_saver_b96_r1_d10000

- sample_id: `w3v2_024`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `NA`
- predicted arguments: `NA`
- gold action: `add_calendar_event`
- gold arguments: `{"attendees": ["Alice", "Bob"], "duration_minutes": 45, "online": true, "start_time": "2026-08-10 14:30", "title": "Budget review"}`
- error_type: `parse_error`
- notes: `physical_run_id=w3v2_024_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="invalid JSON document: Extra data: line 2 column 1 (char 99)"`

## 182. w3v2_025_low_saver_b96_r1_d2000

- sample_id: `w3v2_025`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `5027.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Alice", "text": "Server is back online.", "urgent": true}`
- gold action: `send_message`
- gold arguments: `{"contact": "Alice", "text": "Server is back online", "urgent": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_025_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Alice\", \"text\": \"Server is back online\", \"urgent\": true}, got={\"contact\": \"Alice\", \"text\": \"Server is back online.\", \"urgent\": true}"`

## 183. w3v2_025_low_saver_b96_r1_d5000

- sample_id: `w3v2_025`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `5027.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Alice", "text": "Server is back online.", "urgent": true}`
- gold action: `send_message`
- gold arguments: `{"contact": "Alice", "text": "Server is back online", "urgent": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_025_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Alice\", \"text\": \"Server is back online\", \"urgent\": true}, got={\"contact\": \"Alice\", \"text\": \"Server is back online.\", \"urgent\": true}"`

## 184. w3v2_025_low_saver_b96_r1_d10000

- sample_id: `w3v2_025`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `5027.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Alice", "text": "Server is back online.", "urgent": true}`
- gold action: `send_message`
- gold arguments: `{"contact": "Alice", "text": "Server is back online", "urgent": true}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_025_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Alice\", \"text\": \"Server is back online\", \"urgent\": true}, got={\"contact\": \"Alice\", \"text\": \"Server is back online.\", \"urgent\": true}"`

## 185. w3v2_026_low_saver_b96_r1_d2000

- sample_id: `w3v2_026`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `5424.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Bob", "text": "I will arrive at seven. Sorry.", "urgent": false}`
- gold action: `send_message`
- gold arguments: `{"contact": "Bob", "text": "I will arrive at seven", "urgent": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_026_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Bob\", \"text\": \"I will arrive at seven\", \"urgent\": false}, got={\"contact\": \"Bob\", \"text\": \"I will arrive at seven. Sorry.\", \"urgent\": false}"`

## 186. w3v2_026_low_saver_b96_r1_d5000

- sample_id: `w3v2_026`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `5424.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Bob", "text": "I will arrive at seven. Sorry.", "urgent": false}`
- gold action: `send_message`
- gold arguments: `{"contact": "Bob", "text": "I will arrive at seven", "urgent": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_026_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Bob\", \"text\": \"I will arrive at seven\", \"urgent\": false}, got={\"contact\": \"Bob\", \"text\": \"I will arrive at seven. Sorry.\", \"urgent\": false}"`

## 187. w3v2_026_low_saver_b96_r1_d10000

- sample_id: `w3v2_026`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `5424.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_message`
- predicted arguments: `{"contact": "Bob", "text": "I will arrive at seven. Sorry.", "urgent": false}`
- gold action: `send_message`
- gold arguments: `{"contact": "Bob", "text": "I will arrive at seven", "urgent": false}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_026_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"contact\": \"Bob\", \"text\": \"I will arrive at seven\", \"urgent\": false}, got={\"contact\": \"Bob\", \"text\": \"I will arrive at seven. Sorry.\", \"urgent\": false}"`

## 188. w3v2_027_low_saver_b96_r1_d2000

- sample_id: `w3v2_027`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `6137.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "The draft is attached.", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- gold action: `send_email`
- gold arguments: `{"body": "The draft is attached", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_027_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"body\": \"The draft is attached\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}, got={\"body\": \"The draft is attached.\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}"`

## 189. w3v2_027_low_saver_b96_r1_d5000

- sample_id: `w3v2_027`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `6137.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "The draft is attached.", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- gold action: `send_email`
- gold arguments: `{"body": "The draft is attached", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_027_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"body\": \"The draft is attached\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}, got={\"body\": \"The draft is attached.\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}"`

## 190. w3v2_027_low_saver_b96_r1_d10000

- sample_id: `w3v2_027`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `6137.0`
- action_valid: `true`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "The draft is attached.", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- gold action: `send_email`
- gold arguments: `{"body": "The draft is attached", "high_priority": true, "recipient": "report@example.com", "subject": "Weekly report"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_027_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="expected arguments={\"body\": \"The draft is attached\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}, got={\"body\": \"The draft is attached.\", \"high_priority\": true, \"recipient\": \"report@example.com\", \"subject\": \"Weekly report\"}"`

## 191. w3v2_028_low_saver_b96_r1_d2000

- sample_id: `w3v2_028`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "Meet in room 302", "body_replace": true, "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- gold action: `send_email`
- gold arguments: `{"body": "Meet in room 302", "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_028_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument keys mismatch for send_email; missing=[], extra=['body_replace']"`

## 192. w3v2_028_low_saver_b96_r1_d5000

- sample_id: `w3v2_028`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "Meet in room 302", "body_replace": true, "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- gold action: `send_email`
- gold arguments: `{"body": "Meet in room 302", "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_028_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument keys mismatch for send_email; missing=[], extra=['body_replace']"`

## 193. w3v2_028_low_saver_b96_r1_d10000

- sample_id: `w3v2_028`
- performance_mode: `low_saver`
- deadline_ms: `10000`
- time_to_valid_action_ms: `NA`
- action_valid: `false`
- action_correct: `false`
- action_schema_error: `false`
- predicted action: `send_email`
- predicted arguments: `{"body": "Meet in room 302", "body_replace": true, "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- gold action: `send_email`
- gold arguments: `{"body": "Meet in room 302", "high_priority": false, "recipient": "team@example.com", "subject": "Room change"}`
- error_type: `wrong_argument`
- notes: `physical_run_id=w3v2_028_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message="argument keys mismatch for send_email; missing=[], extra=['body_replace']"`

## 194. w3v2_029_low_saver_b96_r1_d2000

- sample_id: `w3v2_029`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `5159.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "nearest train station", "result_limit": 8, "safe_search": false}`
- gold action: `search_web`
- gold arguments: `{"query": "nearest train station", "result_limit": 8, "safe_search": false}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_029_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 195. w3v2_029_low_saver_b96_r1_d5000

- sample_id: `w3v2_029`
- performance_mode: `low_saver`
- deadline_ms: `5000`
- time_to_valid_action_ms: `5159.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `search_web`
- predicted arguments: `{"query": "nearest train station", "result_limit": 8, "safe_search": false}`
- gold action: `search_web`
- gold arguments: `{"query": "nearest train station", "result_limit": 8, "safe_search": false}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_029_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

## 196. w3v2_030_low_saver_b96_r1_d2000

- sample_id: `w3v2_030`
- performance_mode: `low_saver`
- deadline_ms: `2000`
- time_to_valid_action_ms: `4461.0`
- action_valid: `true`
- action_correct: `true`
- action_schema_error: `false`
- predicted action: `find_ui_element`
- predicted arguments: `{"description": "Settings icon", "visible_only": false}`
- gold action: `find_ui_element`
- gold arguments: `{"description": "Settings icon", "visible_only": false}`
- error_type: `deadline_miss`
- notes: `physical_run_id=w3v2_030_low_saver_b96_r1;action_validator_version=strict_json_v2;action_error_message=""`

