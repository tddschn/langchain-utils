from langchain_utils.utils import convert_str_slice_notation_to_slice


def test_convert_str_slice_notation_to_slice():
    assert convert_str_slice_notation_to_slice('1:3') == slice(1, 3)
    assert convert_str_slice_notation_to_slice('1:') == slice(1, None)
    assert convert_str_slice_notation_to_slice(':3') == slice(None, 3)
    assert convert_str_slice_notation_to_slice(':') == slice(None, None)
    assert convert_str_slice_notation_to_slice('3') == slice(3)
    assert convert_str_slice_notation_to_slice('1:8:2') == slice(1, 8, 2)
