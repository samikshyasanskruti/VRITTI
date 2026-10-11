from backend.app.services.matching.skill_matcher import compare_skills
def test_skill_gap():
    result=compare_skills(["python"],["python","sql"])
    assert result["matched_skills"]==["python"]
    assert result["missing_skills"]==["sql"]
