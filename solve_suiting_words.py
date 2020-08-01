def _load_valid_words(words_file_path, min_length, max_length):
    with open(words_file_path) as f:
        return set(filter(lambda word:
                          all(letter in 'abcdefghjklmnopqrstuvwxyz' for letter in word) and
                          min_length <= len(word) <= max_length and
                          len(set(word)) == len(word),
                          map(lambda l: l.rstrip(), f))
                   )


def _str_to_board(s):
    n = int(len(s) ** 0.5)
    return [[e.lower() for e in s[i * n:(i + 1) * n]] for i in range(n)]


def _get_next_locations(board, i, j):
    return [(i_next, j_next)
            for i_next in range(len(board))
            for j_next in range(len(board))
            if (i_next == i or j_next == j) and board[i_next][j_next]
            ]


def _recursive_backtrack_search(
        column_scores, words, board, i, j, min_length, max_length, results, current_word, current_score):
    if len(current_word) > max_length:
        return
    if len(current_word) >= min_length and current_word in words:
        results[current_word] = current_score
    current_word += board[i][j]
    current_score += column_scores[j]
    board[i][j] = None
    for i_next, j_next in _get_next_locations(board, i, j):
        _recursive_backtrack_search(
            column_scores=column_scores,
            words=words,
            board=board,
            i=i_next,
            j=j_next,
            min_length=min_length,
            max_length=max_length,
            results=results,
            current_word=current_word,
            current_score=current_score)
    board[i][j] = current_word[-1]


def _search(column_scores, words_file_path, board, min_length, max_length):
    results = dict()
    for i in range(len(board)):
        for j in range(len(board)):
            _recursive_backtrack_search(
                column_scores=column_scores,
                words=_load_valid_words(
                    words_file_path=words_file_path,
                    min_length=min_length,
                    max_length=max_length),
                board=board,
                i=i,
                j=j,
                min_length=min_length,
                max_length=max_length,
                results=results,
                current_word='',
                current_score=0
            )
    return results


def _best_words_that_begin_with_different_letters(results, num_best_words):
    d = {}
    for word, score in results:
        if word[0] not in d or d[word[0]][0] < score:
            d[word[0]] = score, word
    return sorted(d.values(), reverse=True)[:num_best_words]


def solve_suited_words(words_file_path, column_scores, board_as_string, min_length, max_length, num_best_words):
    results = sorted(
        _search(
            column_scores=column_scores,
            words_file_path=words_file_path,
            board=_str_to_board(board_as_string),
            min_length=min_length,
            max_length=max_length
        ).items(),
        key=lambda pair: (-pair[1], pair[0])
    )
    solution = _best_words_that_begin_with_different_letters(
        results=results, num_best_words=num_best_words)
    return sum(map(lambda pair: pair[0], solution)), solution, results
