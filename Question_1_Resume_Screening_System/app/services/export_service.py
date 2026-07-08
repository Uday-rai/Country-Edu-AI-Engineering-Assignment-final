import io
import pandas as pd


def candidates_to_csv(candidates) -> io.StringIO:
    rows = []
    for candidate in candidates:
        rows.append(
            {
                "name": candidate.name,
                "email": candidate.email,
                "phone": candidate.phone,
                "skills": candidate.skills,
                "education": candidate.education,
                "experience_years": candidate.experience_years,
                "match_score": candidate.match_score,
                "matched_skills": candidate.matched_skills,
                "missing_skills": candidate.missing_skills,
            }
        )
    output = io.StringIO()
    pd.DataFrame(rows).to_csv(output, index=False)
    output.seek(0)
    return output
