# coding: utf-8

import yaml
import warnings


CONFIG_SKELTON_YAML = """
backlog:
  default_project: default_project_key
  user: alice
  api_key: api_key
"""


def load_conf(filename="./conf.yml"):
    warnings.warn('load_conf will omit in future. See issue #17')
    with open(filename) as f:
        return yaml.load(f, Loader=yaml.Loader)


def generate_default_config():
    warnings.warn('load_conf will omit in future. See issue #17')
    return CONFIG_SKELTON_YAML
