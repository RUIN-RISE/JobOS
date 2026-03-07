import re

def main():
    with open('temp_frontend/src/App.tsx', 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Replace the StructuredJD interface
    code = re.sub(
        r'interface StructuredJD \{[\s\S]*?\}',
        r'',
        code
    )
    
    # Import JobDefinition
    code = code.replace(
        "import type { ChatMessage, CandidateRank } from './api';",
        "import type { ChatMessage, CandidateRank, JobDefinition } from './api';"
    )
    
    # Replace INITIAL_JD
    old_initial = r'const INITIAL_JD: StructuredJD = \{[\s\S]*?\};'
    new_initial = '''const INITIAL_JD: JobDefinition = {
  title: "",
  key_responsibilities: [],
  required_skills: [],
  experience_level: "未指定",
  education: "未指定",
  bonus_skills: [],
  culture_fit: [],
  work_location: "杭州",
  salary: { range: "面议", tax_type: "税前", has_bonus: false, description: "" }
};'''
    code = re.sub(old_initial, new_initial, code)
    
    # Replace all StructuredJD occurrences with JobDefinition
    code = code.replace('StructuredJD', 'JobDefinition')
    
    with open('temp_frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(code)

if __name__ == "__main__":
    main()
