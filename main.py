from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--inject-cases', action='store_true', help='Scrape case files and inject to database.')
    parser.add_argument('--summarization', type=str, default='extractive', help='Summarization method to use.')
    args = parser.parse_args()

    if args.inject_cases:
        from jobs.inject_cases import inject_cases
        inject_cases(summarization=args.summarization)
    else:
        from app import run_app
        run_app()