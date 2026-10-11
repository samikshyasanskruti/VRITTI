const c = (name, score, semantic, skills, evidence, have, missing, snippet) => ({
  title: name, name, company: "", location: "", workType: "", level: "",
  score, semantic, skills, evidence, have, missing,
  rec: "", reasons: [], snippets: [], snippet, url: "",
});

// SAMPLE candidates. All names are made up.
export const demoCandidates = [
  c("Aarav Sample", 88, 85, 90, 80, ["Python", "SQL", "Statistics", "Excel"], ["Tableau"],
    "Final-year student with two analytics projects and strong SQL."),
  c("Diya Example", 76, 74, 70, 72, ["Python", "SQL", "Excel"], ["Tableau", "Statistics"],
    "Built dashboards for a college club; learning statistics."),
  c("Kabir Demo", 63, 66, 55, 60, ["Excel", "SQL"], ["Python", "Statistics", "Tableau"],
    "Strong Excel background; limited programming experience."),
  c("Meera Test", 52, 55, 45, 50, ["Python"], ["SQL", "Excel", "Tableau", "Statistics"],
    "Good Python skills, little experience with data tools."),
  c("Rohan Placeholder", 39, 42, 30, 35, ["Excel"], ["Python", "SQL", "Statistics", "Tableau"],
    "Early-stage learner with basic spreadsheet experience."),
];