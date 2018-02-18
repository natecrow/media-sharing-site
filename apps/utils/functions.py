def determine_page_numbers(middle_number, max_numbers_per_side, total_numbers):
    '''
    Determine and return list of page numbers to display, with the current page
    number in the middle of the list ("middle_number") and the given amount of
    pages numbers on each side of it ("numbers_per_side").
    '''
    assert max_numbers_per_side >= 0, 'Max numbers per side %r is not 0 or higher' % max_numbers_per_side
    assert total_numbers >= 1, 'Total numbers %r is not 1 or more' % total_numbers
    assert middle_number >= 1 and middle_number <= total_numbers, 'Middle number %r is outside the allowed range' % middle_number

    page_numbers = []
    for i in range(max_numbers_per_side, 0, -1):
        if middle_number - i >= 1:
            page_numbers.append(middle_number - i)
    if middle_number >= 1 and middle_number <= total_numbers:
        page_numbers.append(middle_number)
    for i in range(1, max_numbers_per_side + 1):
        if middle_number + i <= total_numbers:
            page_numbers.append(middle_number + i)
    return page_numbers
