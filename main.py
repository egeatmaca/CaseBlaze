from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--inject-cases', action='store_true', help='Scrape case files and inject to database.')
    args = parser.parse_args()

    if args.inject_cases:
        from jobs.inject_cases import inject_cases
        inject_cases()
    else:
        from app import run_app
        run_app()