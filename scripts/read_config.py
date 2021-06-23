import yaml

def read_config(config_root):

  with open(f'{config_root}/config.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

  config = yaml.load(content, Loader=yaml.FullLoader)

  return config