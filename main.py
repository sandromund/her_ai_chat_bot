import yaml

from src.ai import AI

if __name__ == '__main__':
    with open("config.yaml", "r") as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.FullLoader)

    her = AI(config=config)
    her.run()
