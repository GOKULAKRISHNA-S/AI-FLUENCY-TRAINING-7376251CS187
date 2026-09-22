import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

STUDENT_FILE = (
    BASE_DIR / "data" / "student_profile.json"
)

ROLE_FILE = (
    BASE_DIR / "data" / "target_role.json"
)


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def calculate_skill_gaps(
    student,
    role
):

    gaps = []

    student_skills = student["skills"]

    required_skills = role[
        "required_skills"
    ]

    for skill, required in required_skills.items():

        current = student_skills.get(
            skill,
            0
        )

        gap = max(
            0,
            required - current
        )

        gaps.append(
            {
                "skill": skill,
                "current": current,
                "required": required,
                "gap": gap
            }
        )

    gaps.sort(
        key=lambda item: item["gap"],
        reverse=True
    )

    return gaps


def analyze_dsa(
    student,
    role
):

    dsa = student["dsa"]

    expectation = role[
        "dsa_expectation"
    ]

    total_gap = max(
        0,
        expectation["total_problems"]
        - dsa["problems_solved"]
    )

    medium_gap = max(
        0,
        expectation["medium_problems"]
        - dsa["medium"]
    )

    hard_gap = max(
        0,
        expectation["hard_problems"]
        - dsa["hard"]
    )

    return {
        "problems_solved":
            dsa["problems_solved"],

        "total_target":
            expectation["total_problems"],

        "total_gap":
            total_gap,

        "medium_gap":
            medium_gap,

        "hard_gap":
            hard_gap
    }


def analyze_projects(
    student,
    role
):

    project_count = len(
        student["projects"]
    )

    minimum = role[
        "project_expectation"
    ]["minimum_projects"]

    preferred = role[
        "project_expectation"
    ]["preferred_projects"]

    return {
        "current_projects":
            project_count,

        "minimum_required":
            minimum,

        "preferred":
            preferred,

        "minimum_gap":
            max(
                0,
                minimum - project_count
            ),

        "preferred_gap":
            max(
                0,
                preferred - project_count
            )
    }


def create_priorities(
    skill_gaps,
    dsa,
    projects
):

    priorities = []

    for item in skill_gaps:

        if item["gap"] > 0:

            priorities.append(
                f"Improve {item['skill']} "
                f"(gap: {item['gap']})"
            )

    if dsa["total_gap"] > 0:

        priorities.append(
            f"Complete "
            f"{dsa['total_gap']} "
            f"additional DSA problems"
        )

    if dsa["medium_gap"] > 0:

        priorities.append(
            f"Solve "
            f"{dsa['medium_gap']} more "
            f"medium-level DSA problems"
        )

    if projects["minimum_gap"] > 0:

        priorities.append(
            "Build another project"
        )

    return priorities


def run_workflow():

    student = load_json(
        STUDENT_FILE
    )

    role = load_json(
        ROLE_FILE
    )

    skill_gaps = calculate_skill_gaps(
        student,
        role
    )

    dsa_analysis = analyze_dsa(
        student,
        role
    )

    project_analysis = analyze_projects(
        student,
        role
    )

    priorities = create_priorities(
        skill_gaps,
        dsa_analysis,
        project_analysis
    )

    print("=" * 70)
    print("CAREERLENS — RULE-BASED WORKFLOW")
    print("=" * 70)

    print("\nSKILL GAPS")

    for item in skill_gaps:

        print(
            f"{item['skill']}: "
            f"{item['current']} → "
            f"{item['required']} "
            f"(gap {item['gap']})"
        )

    print("\nDSA ANALYSIS")

    print(
        f"Problems: "
        f"{dsa_analysis['problems_solved']} / "
        f"{dsa_analysis['total_target']}"
    )

    print(
        f"Total gap: "
        f"{dsa_analysis['total_gap']}"
    )

    print(
        f"Medium gap: "
        f"{dsa_analysis['medium_gap']}"
    )

    print(
        f"Hard gap: "
        f"{dsa_analysis['hard_gap']}"
    )

    print("\nPROJECT ANALYSIS")

    print(
        f"Projects: "
        f"{project_analysis['current_projects']} / "
        f"{project_analysis['minimum_required']}"
    )

    print("\nPRIORITIES")

    for index, priority in enumerate(
        priorities,
        1
    ):

        print(
            f"{index}. {priority}"
        )


if __name__ == "__main__":
    run_workflow()
