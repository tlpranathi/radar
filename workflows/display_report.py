def display_job_report(result):

    print("\n")
    print("=" * 65)
    print("                 RADAR - JOB ANALYSIS")
    print("=" * 65)

    print(f"\nCompany : {result['company']}")
    print(f"Role    : {result['role']}")

    # resume match
    match = result["resume_match"]

    print("\n" + "-" * 65)
    print("RESUME COMPATIBILITY")
    print("-" * 65)

    score = match["match_score"]
    print(f"\nOverall Match Score: {score}%")

    bar_length = 30
    filled = int(score / 100 * bar_length)

    print("[" + "#" * filled + "-" * (bar_length - filled) + "]")

    # matched skills
    print("\nSKILLS DETECTED")

    for item in match["matched_skills"]:
        print(
            f"  + {item['skill']} "
            f"({item['match_type']})"
        )

    for item in match["preferred_skills_found"]:
        print(
            f"  + {item['skill']} "
            f"({item['match_type']}, preferred)"
        )

    # missing skills
    print("\nSKILLS TO IMPROVE")

    for skill in match["missing_required_skills"]:
        print(f"  - {skill}")

    # research
    print("\n" + "-" * 65)
    print("INTERVIEW RESEARCH")
    print("-" * 65)

    research = result["interview_research"]

    if not research:
        print("  No relevant research results found.")

    for index, item in enumerate(research, start=1):
        print(f"\n  {index}. {item['title']}")
        print(f"     {item['url']}")

    # preparation plan
    plan = result["prep_plan"]

    print("\n" + "-" * 65)
    print("PERSONALIZED PREPARATION PLAN")
    print("-" * 65)

    print("\nPRIORITY GAPS")

    for gap in plan["priority_gaps"]:
        print(f"  - {gap}")

    print("\nSTUDY TOPICS")

    for topic in plan["study_topics"]:
        print(f"  - {topic}")

    print("\nPRACTICE TASKS")

    for task in plan["practice_tasks"]:
        print(f"  - {task}")

    print("\nWEEKLY ROADMAP")

    for week in plan["weekly_plan"]:
        week_number = week.get("week", "?")
        focus = week.get("focus", "General preparation")

        print(f"\n  Week {week_number}: {focus}")

        objectives = week.get("objectives", [])

        if objectives:
            for objective in objectives:
                print(f"    - {objective}")
        else:
            print("    No specific objectives provided.")

    print("\n" + "=" * 65)
    print("                 END OF REPORT")
    print("=" * 65)
