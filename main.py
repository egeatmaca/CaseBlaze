from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--scrape-and-inject', action='store_true', help='Scrape case files and inject to database.')
    args = parser.parse_args()

    if args.scrape_and_inject:
        from jobs.scrape_and_inject import scrape_and_inject
        scrape_and_inject()
    else:
        from app import run_app
        run_app()