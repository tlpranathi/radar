import re
from functools import lru_cache
import numpy as np


DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_SEMANTIC_THRESHOLD = 0.55


@lru_cache(maxsize=1)
def _load_embedding_model():
    """Load the embedding model only when semantic matching is needed."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(DEFAULT_MODEL_NAME)


def _split_sentences(text: str) -> list[str]:
    """Split resume text into useful evidence snippets."""
    snippets = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # preserve bullet points and headings as individual snippets
        parts = re.split(r"(?<=[.!?])\s+", line)
        snippets.extend(part.strip() for part in parts if part.strip())

    return snippets


def _contains_skill(text: str, skill: str) -> bool:
    """Check for a literal skill phrase, ignoring letter case."""
    pattern = rf"(?<!\w){re.escape(skill.strip())}(?!\w)"
    return bool(re.search(pattern, text, flags=re.IGNORECASE))


def _cosine_similarities(skill_vector, sentence_vectors):
    """Calculate cosine similarity between one vector and many vectors."""
    skill_vector = np.asarray(skill_vector, dtype=float).reshape(-1)
    sentence_vectors = np.asarray(sentence_vectors, dtype=float)

    skill_norm = np.linalg.norm(skill_vector)
    sentence_norms = np.linalg.norm(sentence_vectors, axis=1)

    if skill_norm == 0:
        return np.zeros(len(sentence_vectors))

    denominators = skill_norm * sentence_norms
    similarities = np.zeros(len(sentence_vectors))
    valid = denominators > 0

    similarities[valid] = (
        sentence_vectors[valid] @ skill_vector
    ) / denominators[valid]

    return similarities


def match_resume(
    requirements: dict,
    resume_text: str,
    model=None,
    semantic_threshold: float = DEFAULT_SEMANTIC_THRESHOLD,
) -> dict:
    """
    Match job requirements against resume text.

    Exact matches are preferred. If no exact match exists, semantic
    similarity can identify a possible match with supporting evidence.

    `model` is injectable to make tests independent of model downloads.
    """
    if not isinstance(requirements, dict):
        raise TypeError("requirements must be a dictionary")

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("resume_text must be a non-empty string")

    if not 0 <= semantic_threshold <= 1:
        raise ValueError("semantic_threshold must be between 0 and 1")

    for field in ("required_skills", "preferred_skills"):
        if not isinstance(requirements.get(field, []), list):
            raise TypeError(f"{field} must be a list")

    required = list(dict.fromkeys(
        skill.strip()
        for skill in requirements.get("required_skills", [])
        if isinstance(skill, str) and skill.strip()
    ))
    preferred = list(dict.fromkeys(
        skill.strip()
        for skill in requirements.get("preferred_skills", [])
        if isinstance(skill, str) and skill.strip()
    ))

    # a skill appearing in both lists should only be counted once
    preferred = [skill for skill in preferred if skill not in required]
    all_skills = required + preferred

    sentences = _split_sentences(resume_text)
    if not sentences:
        raise ValueError("No usable text found in resume")

    # first pass: exact matching doesn't require an embedding model
    results = {}
    unresolved = []

    for skill in all_skills:
        evidence = next(
            (sentence for sentence in sentences
             if _contains_skill(sentence, skill)),
            None,
        )

        if evidence:
            results[skill] = {
                "match_type": "exact",
                "similarity": 1.0,
                "evidence": evidence,
            }
        else:
            unresolved.append(skill)

    # second pass: use embeddings only for skills without exact matches
    if unresolved:
        if model is None:
            model = _load_embedding_model()

        skill_vectors = model.encode(
            unresolved, convert_to_numpy=True
        )
        sentence_vectors = model.encode(
            sentences, convert_to_numpy=True
        )

        for skill, skill_vector in zip(unresolved, skill_vectors):
            scores = _cosine_similarities(
                skill_vector, sentence_vectors
            )
            best_index = int(np.argmax(scores))
            best_score = float(scores[best_index])

            if best_score >= semantic_threshold:
                results[skill] = {
                    "match_type": "semantic",
                    "similarity": round(best_score, 4),
                    "evidence": sentences[best_index],
                }
            else:
                results[skill] = {
                    "match_type": "missing",
                    "similarity": round(best_score, 4),
                    "evidence": None,
                }

    matched_required = [
        {"skill": skill, **results[skill]}
        for skill in required
        if results[skill]["match_type"] != "missing"
    ]
    missing_required = [
        skill for skill in required
        if results[skill]["match_type"] == "missing"
    ]
    preferred_found = [
        {"skill": skill, **results[skill]}
        for skill in preferred
        if results[skill]["match_type"] != "missing"
    ]

    # transparent weighted score:
    # required skills are worth 3 points; preferred skills are worth 1
    # exact match = full points; semantic match = 70% of points
    points = 0.0
    total_points = 3 * len(required) + len(preferred)

    for skill in required:
        match_type = results[skill]["match_type"]
        points += 3 * (
            1.0 if match_type == "exact"
            else 0.7 if match_type == "semantic"
            else 0.0
        )

    for skill in preferred:
        match_type = results[skill]["match_type"]
        points += (
            1.0 if match_type == "exact"
            else 0.7 if match_type == "semantic"
            else 0.0
        )

    score = round(100 * points / total_points, 1) if total_points else 0.0

    return {
        "matched_skills": matched_required,
        "missing_required_skills": missing_required,
        "preferred_skills_found": preferred_found,
        "missing_preferred_skills": [
            skill for skill in preferred
            if results[skill]["match_type"] == "missing"
        ],
        "evidence": {
            skill: result["evidence"]
            for skill, result in results.items()
            if result["evidence"] is not None
        },
        "match_score": score,
        "score_method": (
            "Required skills: 3 points each; preferred skills: "
            "1 point each; exact match earns full points, semantic "
            "match earns 70%, missing earns 0%."
        ),
    }
