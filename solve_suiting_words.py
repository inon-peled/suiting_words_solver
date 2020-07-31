def _load_words(path):
    with open(path) as f:
        return {line.rstrip() for line in f}


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


def _search(column_scores, words_path, board, min_length, max_length):
    results = dict()
    for i in range(len(board)):
        for j in range(len(board)):
            _recursive_backtrack_search(
                column_scores=column_scores,
                words=_load_words(words_path),
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


def solve_suited_words(words_path, column_scores, board_as_string, min_length, max_length, num_best_words):
    results = sorted(
        _search(
            column_scores=column_scores,
            words_path=words_path,
            board=_str_to_board(board_as_string),
            min_length=min_length,
            max_length=max_length
        ).items(),
        key=lambda pair: (-pair[1], pair[0])
    )
    solution = _best_words_that_begin_with_different_letters(
        results=results, num_best_words=num_best_words)
    return sum(map(lambda pair: pair[0], solution)), solution, results
