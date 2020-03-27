from sandberg.harmony import substitute_major_for_minor


def test_substitute_major_for_minor():
    major_chords = ['I', 'VI', 'IV', 'II']
    result = substitute_major_for_minor(major_chords)
    expected_result = ['VI', 'IV', 'II', 'VII']
    assert result == expected_result
    
