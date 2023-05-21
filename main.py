import argparse
from src.unstable import unstable
from src.save_and_append import save_and_append

def main(config_file, output_folder):
    response = unstable(config_file)
    save_and_append(response, output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Path to the config file", default="./config.yml")
    parser.add_argument("--output", help="Path to the output folder", default="./output")
    args = parser.parse_args()

    main(args.config, args.output)