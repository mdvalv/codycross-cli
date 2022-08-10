import sys
import requests
from bs4 import BeautifulSoup as bs
import argparse


URL = "https://codycrossanswers.net"


def get_level_name(level: int):
    names = ['earth', 'under-the-sea', 'inventions', 'seasons', 'circus', 'transports', 'culinary', 'sports',
             'fauna-and-flora', 'ancient-egypt', 'amusement-park', 'medieval-times', 'paris', 'casino', 'library',
             'science-lab', 'the-70s', 'pet-shop', 'new-york-new-york', 'popcorn-time', 'la-bella-roma', 'wild-west',
             'airport', 'farm', 'london', 'department-store', 'fashion-show', 'resorts', 'welcome-to-japan',
             'concert-hall', 'tv-station', 'home-sweet-home', 'cruise-ship', 'greece', 'small-world', 'train-travel',
             'art-museum', 'water-park', 'brazilian-tour', 'the-80s', 'spa-time', 'campsite-adventures',
             'trip-to-spain', 'fantasy-world', 'performing-arts', 'space-exploration', 'student-life', 'games',
             'mesopotamia', 'futuristic-city', 'australia', 'treasure-island', 'tracking-time', 'comics',
             'a-sweet-life', 'house-of-horrors', 'the-90s', 'california', 'architectural-styles', 'spaceship',
             'rainforest', 'working-from-home', 'prehistory', 'canada']
    return names[(level - 1) // 20]


def get_answer(question_url: str):
    res = requests.get(question_url)
    soup = bs(res.content, 'html.parser')

    solutions = soup.find_all("div", {"class": "solutions"})
    if len(solutions) == 0:
        solutions = soup.find_all("div", {"class": "entry-content"})
    strong = solutions[0].strong.text.strip()

    if strong.endswith(":"):
        return solutions[0].text.split(":")[-1].strip()
    elif strong == 'SOLUTION':
        return solutions[0].select_one('p:-soup-contains("SOLUTION")').text.split()[-1]
    elif len(strong) > 0:
        return strong
    else:
        return solutions[0].find_all("div", {"class": "answer-text"})[0].text


def get_parser():
    parser = argparse.ArgumentParser(description='CodyCross CLI')
    parser.add_argument('level', type=int, help='level number')
    parser.add_argument('puzzle', type=int, help='puzzle number')
    parser.add_argument('question', type=int, help='question number, if 0, get answers for all questions')
    parser.add_argument('-d', '--debug', help='debug mode', action='store_true')
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    if args.puzzle < 1 or args.puzzle > 5:
        sys.exit(f"Puzzle value should be between 1 and 5")

    question_number = args.question

    try:
        lvl_name = get_level_name(args.level)
    except Exception:
        sys.exit(f"Unknown level {args.level}")

    puzzle_url = f"{URL}/codycross-{lvl_name}-group-{args.level}-puzzle-{args.puzzle}-answers"
    if args.debug:
        print(puzzle_url)
        print("====================")

    res = requests.get(puzzle_url)
    soup = bs(res.content, 'html.parser')
    levels = soup.find_all("div", {"class": "levels-div"})
    if len(levels) == 0:
        levels = soup.find_all("div", {"class": "entry-content"})
    levels = levels[0].find_all('li')

    if question_number > 0:
        try:
            question = levels[question_number - 1]
            question_url = question.find('a')['href']
        except Exception:
            sys.exit(f"Unknown question {question_number}")
        print(question.text.strip())
        print(f'> {get_answer(question_url)}')
        if args.debug:
            print("====================")
            print(question_url)
    else:
        question_urls = []
        for li in levels:
            question_url = li.find('a')['href']
            question_urls.append(question_url)
            print(li.text.strip())
            print(f'> {get_answer(question_url)}')
        if args.debug:
            print("====================")
            for question_url in question_urls:
                print(question_url)
