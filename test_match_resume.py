import unittest
import numpy as np
from tools.match_resume import match_resume


class FakeEmbeddingModel:
    """Deterministic embeddings for testing; not a real language model."""

    vectors = {
        "REST API development": [1.0, 0.0, 0.0],
        "Kubernetes": [0.0, 0.0, 1.0],
        "Built REST endpoints for internal services.": [0.8, 0.6, 0.0],
        "Used Python to automate data processing.": [0.0, 1.0, 0.0],
    }

    def encode(self, texts, convert_to_numpy=True):
        return np.array([self.vectors[text] for text in texts])


class TestMatchResume(unittest.TestCase):

    def setUp(self):
        self.requirements = {
            "required_skills": [
                "Python",
                "REST API development",
                "Kubernetes",
            ],
            "preferred_skills": ["Docker"],
        }

        self.resume = (
            "Used Python to automate data processing.\n"
            "Built REST endpoints for internal services."
        )

        # docker needs a vector too if it isn't found exactly.
        FakeEmbeddingModel.vectors["Docker"] = [0.0, 0.0, 1.0]

    def test_exact_match(self):
        result = match_resume(
            {"required_skills": ["Python"], "preferred_skills": []},
            "Used Python to automate data processing.",
        )

        self.assertEqual(len(result["matched_skills"]), 1)
        self.assertEqual(result["matched_skills"][0]["match_type"], "exact")
        self.assertEqual(result["match_score"], 100.0)

    def test_semantic_match(self):
        result = match_resume(
            {"required_skills": ["REST API development"],
             "preferred_skills": []},
            self.resume,
            model=FakeEmbeddingModel(),
        )

        match = result["matched_skills"][0]
        self.assertEqual(match["match_type"], "semantic")
        self.assertEqual(
            match["evidence"],
            "Built REST endpoints for internal services.",
        )

    def test_missing_required_skill(self):
        result = match_resume(
            {"required_skills": ["Kubernetes"], "preferred_skills": []},
            self.resume,
            model=FakeEmbeddingModel(),
        )

        self.assertEqual(result["missing_required_skills"], ["Kubernetes"])
        self.assertEqual(result["match_score"], 0.0)

    def test_invalid_resume(self):
        with self.assertRaises(ValueError):
            match_resume(self.requirements, "  ")

    def test_invalid_requirements(self):
        with self.assertRaises(TypeError):
            match_resume([], self.resume)

    def test_score_prioritizes_required_skills(self):
        result = match_resume(
            {
                "required_skills": ["Python", "Kubernetes"],
                "preferred_skills": ["Docker"],
            },
            "Used Python to automate data processing.",
            model=FakeEmbeddingModel(),
        )

        # python: 3 points kubernetes: 0 docker: 0.
        # total possible: 3 + 3 + 1 = 7
        self.assertEqual(result["match_score"], 42.9)


if __name__ == "__main__":
    unittest.main()
