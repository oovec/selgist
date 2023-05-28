import argparse
import toml
import os
from selgist.types_ import Config
from selgist.fetcher import Fetcher
from selgist.gen import render_all


def main():
    print("hehe")
    parser = argparse.ArgumentParser(
        description='Generate selected static pages')
    parser.add_argument('-c',
                        '--config',
                        help='Config file path',
                        default='config.toml')
    parser.add_argument('-o',
                        '--output',
                        help='Output directory path',
                        default='public')
    args = parser.parse_args()
    try:
        with open(args.config, 'r') as f:
            config_dict = {}
            for k, v in toml.load(f).items():
                config_dict[k] = v
            config = Config(config_dict)
    except toml.TomlDecodeError as e:
        print("Error decoding TOML file: ", e)
        os._exit(1)
    fetcher = Fetcher(config)
    gists = fetcher.get_selected_gists()
    for g in gists:
        print(g.id, g.title, g.category, g.tags)
    render_all(config, gists, args.output)


if __name__ == "__main__":
    main()
