from solve_suiting_words import solve_suited_words


def nice_print(total_score, solution, all_results, also_print_all_found_words):
    print('Total Score: %d' % total_score)
    for i, (score, word) in enumerate(solution, start=1):
        print('%d) %s = %d' % (i, word, score))
    if also_print_all_found_words:
        print('\nAll words found:')
        for j, (word, score) in enumerate(all_results, start=1):
            print('%d) %s = %d' % (j, word, score))


if __name__ == '__main__':
    nice_print(
        *solve_suited_words(
            board_as_string='krocnflueatisdyq',
            column_scores=(10, 5, 2, 1),
            words_path='words.txt',
            min_length=3,
            max_length=6,
            num_best_words=12),
        also_print_all_found_words=False)
