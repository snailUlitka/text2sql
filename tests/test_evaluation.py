from text2sql.evaluation import same_rows


def test_result_comparison_preserves_duplicates_and_optional_order():
    assert same_rows([[1], [2]], [[2], [1]], ordered=False)
    assert not same_rows([[1], [2]], [[2], [1]], ordered=True)
    assert not same_rows([[1], [1]], [[1]], ordered=False)
