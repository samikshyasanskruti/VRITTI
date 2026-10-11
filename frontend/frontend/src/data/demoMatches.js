import { demoInternships as J } from "./demoInternships";

// Builds one match result from a job + sample scores.
const make = (job, score, semantic, skills, evidence, have, rec, snippets = []) => ({
  title: job.title, name: job.title, company: job.company, location: job.location,
  workType: job.workType, level: job.level,
  score, semantic, skills, evidence,
  have,
  missing: job.requiredSkills.filter((s) => !have.includes(s)),
  rec, reasons: [], snippets, snippet: "", url: job.url,
});

// SAMPLE numbers only. They are not real model output.
export const demoMatches = [
  make(J[0], 82, 80, 75, 70, ["Python", "SQL", "Machine Learning", "Pandas"].slice(0, 3),
    "Strong fit. Add Pandas to your resume to close the gap.",
    ["Built a movie recommender using Python and scikit-learn."]),
  make(J[1], 64, 70, 50, 60, ["Python", "Machine Learning"],
    "Good fit if you learn PyTorch and Docker.",
    ["Trained classification models on small datasets."]),
  make(J[4], 58, 55, 50, 55, ["Excel", "SQL"],
    "Solid base. Learn Tableau and Statistics to stand out.",
    ["Built a sales dashboard with Excel and SQL."]),
  make(J[3], 47, 50, 50, 40, ["Python", "SQL"],
    "Learn FastAPI and Docker to become a stronger backend candidate."),
  make(J[2], 41, 45, 25, 35, ["SQL"],
    "Needs Power BI, Excel and Statistics skills for this role."),
];

// SAMPLE profile used by the resume service in demo mode.
export const demoProfile = {
  name: "Sample Student",
  email: "sample@example.com",
  text:
    "Computer science student skilled in Python, SQL, machine learning, pandas and scikit-learn.\n" +
    "Projects: Movie Recommender (Python, scikit-learn), Sales Dashboard (Excel, SQL).\n" +
    "Looking for a data science internship.",
  skills: ["Python", "SQL", "Machine Learning", "Pandas", "Scikit-learn", "Excel"],
  projects: [
    { title: "Movie Recommender", description: "Suggests movies using similarity scores.", tech: ["Python", "Scikit-learn"] },
    { title: "Sales Dashboard", description: "Weekly sales summary for a small shop.", tech: ["Excel", "SQL"] },
  ],
  domains: [
    { name: "Data Science", value: 45 },
    { name: "Analytics", value: 30 },
    { name: "Software", value: 25 },
  ],
};