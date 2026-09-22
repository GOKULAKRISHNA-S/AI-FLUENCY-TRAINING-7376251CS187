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


def get_academic_performance():

    student = load_json(
        STUDENT_FILE
    )

    return {
        "academics":
            student["academics"]
    }


def get_skill_profile():

    student = load_json(
        STUDENT_FILE
    )

    return {
        "skills":
            student["skills"]
    }


def get_dsa_progress():

    student = load_json(
        STUDENT_FILE
    )

    return {
        "dsa":
            student["dsa"]
    }


def get_project_profile():

    student = load_json(
        STUDENT_FILE
    )

    return {
        "projects":
            student["projects"]
    }


def get_target_job_requirements():

    return load_json(
        ROLE_FILE
    )


def calculate_skill_gaps():

    student = load_json(
        STUDENT_FILE
    )

    role = load_json(
        ROLE_FILE
    )

    gaps = []

    for skill, required in role[
        "required_skills"
    ].items():

        current = student[
            "skills"
        ].get(
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

    return {
        "role":
            role["role"],

        "skill_gaps":
            gaps
    }