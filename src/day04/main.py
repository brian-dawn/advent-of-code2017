
def get_passphrases(file_name):
    with open('../../resources/' + file_name, 'r') as fp:
        for text in fp.read().split('\n'):
            yield text.split(' ')


def run():
    phrases = get_passphrases('day4.txt')
    count = 0
    for phrase in phrases:
        count += 1 if len(phrase) == len(set(phrase)) else 0
    return count


def run_2():
    phrases = get_passphrases('day4.txt')
    count = 0
    for phrase in phrases:
        ana_phrase = [''.join(sorted(word)) for word in phrase]
        count += 1 if len(phrase) == len(set(ana_phrase)) else 0
    return count

if __name__ == '__main__':
    print run()
    print run_2()
