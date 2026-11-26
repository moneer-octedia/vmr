from evals import score


def test_empty_answer_scores_zero() -> None:
    assert score("") == 0.0


def test_any_answer_scores_one() -> None:
    assert score("hello") == 1.0
