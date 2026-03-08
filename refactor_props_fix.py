import re

def main():
    with open('temp_frontend/src/App.tsx', 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Fix the `setCurrentJd` that I missed replacing
    # Lines 237/547 area:
    code = re.sub(
        r'await api\.setCurrentJd\(\{\s*title: confirmedJd\.title[\s\S]*?\} as any\);',
        r'await api.setCurrentJd(confirmedJd);',
        code
    )
    code = re.sub(
        r'await api\.setCurrentJd\(\{\s*title: finalJd\.title[\s\S]*?\} as any\);',
        r'await api.setCurrentJd(finalJd);',
        code
    )
    code = re.sub(
        r'await api\.setCurrentJd\(\{\s*title: jdData\.title[\s\S]*?\} as any\);',
        r'await api.setCurrentJd(jdData);',
        code
    )

    # 2. Fix JdReviewPanel keys
    code = code.replace("handleChange('role',", "handleChange('title',")
    code = code.replace("handleChange('exp_level',", "handleChange('experience_level',")
    code = code.replace("handleChange('stack',", "handleChange('required_skills',")
    code = code.replace("handleChange('plus_points',", "handleChange('bonus_skills',")
    code = code.replace("handleChange('remarks',", "handleChange('salary', { ...jd.salary, description: e.target.value })") # wait, handleChange accepts keyof JobDefinition. If we pass 'salary', we need to pass the whole salary object.
    
    # Let's just fix handleChange directly in App.tsx using regex on the textarea for remarks
    # Old: onChange={e => handleChange('remarks', e.target.value)}
    # Let's change it to:
    code = code.replace("onChange={e => handleChange('remarks', e.target.value)}", "onChange={e => handleChange('salary', { ...jd.salary, description: e.target.value })}")

    # 3. Fix SpecConfigurator init role -> title
    code = code.replace("role: initialUserInput", "title: initialUserInput")
    
    # 4. Fix `setFormData({ ...formData, role: '' })` or similar
    code = code.replace("...formData, role:", "...formData, title:")
    
    # 5. Fix mis-replaced ChatMessage.title -> ChatMessage.role
    # E.g. `msg.title === 'user'`, `msg.title === 'assistant'`, `title: 'user'`
    code = code.replace("msg.title === 'user'", "msg.role === 'user'")
    code = code.replace("msg.title === 'assistant'", "msg.role === 'assistant'")
    code = code.replace("msg.title", "msg.role")  # This could be dangerous but there shouldn't be other `msg.title`
    code = code.replace("title: 'user'", "role: 'user'")
    code = code.replace("title: 'assistant'", "role: 'assistant'")
    
    # 6. Any stray missing fields from JdDefinition
    # if `await api.setCurrentJd` has raw object missing culture_fit and education
    # Actually I replaced them all with passing `finalJd` / `confirmedJd` / `jdData` so it should be fine.
    
    with open('temp_frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(code)

if __name__ == "__main__":
    main()
