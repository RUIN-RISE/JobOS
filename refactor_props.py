import re

def main():
    with open('temp_frontend/src/App.tsx', 'r', encoding='utf-8') as f:
        code = f.read()

    # Apply mappings strictly to .property access where relevant
    code = code.replace('.role', '.title')
    code = code.replace('.stack', '.required_skills')
    code = code.replace('.exp_level', '.experience_level')
    code = code.replace('.plus_points', '.bonus_skills')
    
    # .remarks is tricky because it maps to salary.description, but we'll do our best
    code = code.replace('.remarks', '.salary.description')

    # Fix the `INITIAL_JD` definition which might have got messed up with salary.description mapping
    # Just to be safe, we rewrite the INITIAL_JD definition perfectly:
    initial_jd = '''const INITIAL_JD: JobDefinition = {
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
    code = re.sub(r'const INITIAL_JD: JobDefinition = \{[\s\S]*?\};', initial_jd, code)

    # Fix SpecConfigurator init
    code = code.replace('title: initialUserInput, salary.description: ""', 'title: initialUserInput, salary: { ...INITIAL_JD.salary, description: "" }')

    # Fix the `finalJd: JobDefinition` in `handleLoadHistoryRecord`
    history_record_repl = '''const finalJd: JobDefinition = {
      title: rawJd.title || rawJd.role || "",
      key_responsibilities: rawJd.key_responsibilities || [],
      required_skills: rawJd.required_skills || rawJd.stack || [],
      experience_level: rawJd.experience_level || rawJd.exp_level || "未指定",
      culture_fit: rawJd.culture_fit || [],
      education: rawJd.education || "未指定",
      bonus_skills: rawJd.bonus_skills || rawJd.plus_points || [],
      salary: {
         range: rawJd.salary?.range || "面议",
         tax_type: rawJd.salary?.tax_type || "税前",
         has_bonus: rawJd.salary?.has_bonus || false,
         description: rawJd.salary?.description || rawJd.remarks || ""
      },
      work_location: rawJd.work_location || "杭州"
    };'''
    code = re.sub(r'const finalJd: JobDefinition = \{[\s\S]*?\n    \};', history_record_repl, code, count=1)
    
    # Fix the duplicate setCurrentJd payloads that used to do:
    # salary: { range: "", tax_type: "税前", has_bonus: false, description: confirmedJd.salary.description }
    # Let's just pass `jdData` entirely or just `confirmedJd` where applicable
    code = code.replace('''await api.setCurrentJd({
        title: confirmedJd.title || "未命名职位",
        key_responsibilities: [],
        required_skills: confirmedJd.required_skills || [],
        experience_level: confirmedJd.experience_level || "未指定",
        salary: { range: "", tax_type: "税前", has_bonus: false, description: confirmedJd.salary.description },
        work_location: "不限",
        bonus_skills: confirmedJd.bonus_skills || []
      } as any);''', 'await api.setCurrentJd(confirmedJd);')

    code = code.replace('''await api.setCurrentJd({
        title: finalJd.title || "未命名职位",
        key_responsibilities: [],
        required_skills: finalJd.required_skills || [],
        experience_level: finalJd.experience_level || "未指定",
        salary: { range: "", tax_type: "税前", has_bonus: false, description: finalJd.salary.description },
        work_location: "不限",
        bonus_skills: finalJd.bonus_skills || []
      } as any);''', 'await api.setCurrentJd(finalJd);')

    code = code.replace('''await api.setCurrentJd({
          title: jdData.title || "通用岗位",
          key_responsibilities: [],
          required_skills: jdData.required_skills || [],
          experience_level: jdData.experience_level || "未指定",
          salary: { range: "", tax_type: "税前", has_bonus: false, description: jdData.salary.description || "" },
          work_location: "不限",
          bonus_skills: jdData.bonus_skills || []
        } as any);''', 'await api.setCurrentJd(jdData);')

    # Fix handleFieldRemove
    code = code.replace("prev.required_skills.filter", "prev.required_skills!.filter")
    code = code.replace("prev.bonus_skills.filter", "prev.bonus_skills!.filter")
    code = code.replace("prev.culture_fit.filter", "prev.culture_fit!.filter")

    with open('temp_frontend/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(code)

if __name__ == "__main__":
    main()
