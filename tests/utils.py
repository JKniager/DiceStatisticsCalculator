def check_within_error(correct_answer: float, given_answer: float, err: float) -> bool:
    return (correct_answer - err) <= given_answer <= (correct_answer + err)
