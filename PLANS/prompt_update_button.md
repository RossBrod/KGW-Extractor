# Update Prompts from Files Plan

## Overview
Add a button to the AdminApp that will read prompt files from the Prompts folder and update them in the database by functional_area.

## File Analysis
- Prompts are stored in `/mnt/c/_Repo/KGW-Extractor/Prompts/`
- File naming follows pattern: `S{number} {FunctionalArea}{FileType}.txt`
- Each functional_area has 3 associated files:
  - `S{number} {FunctionalArea}System.txt` → system_prompt
  - `S{number} {FunctionalArea}Extractor.txt` → extraction_prompt  
  - `S{number} {FunctionalArea}Assistant.txt` → confirmation_prompt

## Implementation Plan

### 1. Backend API Endpoint (server.js)
- Create a new POST endpoint `/api/prompts/update-from-files`
- Implement logic to:
  - Scan the Prompts directory
  - Group files by functional_area
  - Read content from each file
  - Update only existing database records (no new records will be created)

### 2. Frontend API Service (api.ts)
- Add a new function `updatePromptsFromFiles()` that calls the endpoint

### 3. UI Component (App.tsx)
- Add a button at the top of the existing interface
- Display loading state during update
- Show success/error messages

### 4. Error Handling
- Handle file read errors
- Handle database update errors
- Provide user feedback

## Technical Details

### Database Operation
```sql
-- For each prompt set, execute:
UPDATE prompts 
SET system_prompt = $1, 
    extraction_prompt = $2, 
    confirmation_prompt = $3
WHERE functional_area = $4;
```

NOTE: No new prompts will be created. The prompts must already exist in the database with the corresponding functional_area.

### File Path Mapping
The backend will need to:
1. Parse filenames to extract functional_area
2. Group files by functional_area
3. Map file content to the appropriate database field