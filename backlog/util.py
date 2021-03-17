# coding: utf-8

import yaml

CONFIG_SKELTON_YAML = """
backlog:
  default_project: default_project_key
  user: alice
  api_key: api_key
"""


def load_conf(filename="./conf.yml"):
    with open(filename) as f:
        return yaml.load(f, Loader=yaml.Loader)


def generate_default_config():
    return CONFIG_SKELTON_YAML
