from jinja2 import Environment, FileSystemLoader
import os
import subprocess
from copy import deepcopy

from sys import argv

from time import ctime
import yaml
from collections import OrderedDict

from textwrap import wrap


def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)

j2_env = Environment(loader=FileSystemLoader("."),
                    trim_blocks=True)

def format_descriptions(desc):
    capitalized = " ".join([s.capitalize() for s in desc.split("_")])
    dashes = "-" * len(desc)
    return " ".join(["#", dashes, "\n#", capitalized, "\n#", dashes])

def format_comments(c):

    return "# " + "\n# ".join(wrap(str(c), 78))

def required(r):

    return "# (Required)" if r else "# (Not required)"

def default(d):

    if d != "None":
        return str(d)
    else:
        return ""

def example(e):

    if not e:
        return ""

    if isinstance(e, list):
        example = "\n#".join([str(s) for s in e])
    else:
        example = str(e)

    return "# Example: " + example


def _update_config(existing_config, description_config):

    modify_config = deepcopy(description_config)
    for k, v in description_config.items():

        items = list(v.items())

        for k2, v2 in items:

            if existing_config.get(k2):
                modify_config[k][k2]["default"] = existing_config[k2]

    return modify_config


def update_config(configuration_file, description):

    existing_config = yaml.load(open(configuration_file))
    description_config = ordered_load(open(description))

    updated_config = _update_config(existing_config, description_config)

    return updated_config


if __name__ == "__main__":

    configuration_list = argv[1]
    description = argv[2] # config_description.yaml
    template = argv[3] # base_template.conf

    j2_env.filters["format_descriptions"] = format_descriptions
    j2_env.filters["format_comments"] = format_comments
    j2_env.filters["required"] = required
    j2_env.filters["example"] = example
    j2_env.filters["default"] = default

    configuration_files = [f.strip() for f in open(configuration_list).readlines()]

    for configuration_file in configuration_files:

        time_str = ctime().replace(" ", "_").replace(":", "_")
        subprocess.call("cp {0} {0}_{1}.bkup".format(configuration_file, time_str), shell=True)

        updated_config = update_config(configuration_file, description)

        updated_config_file = j2_env.get_template(template).render(
            config=updated_config.items()
        )

        with open(configuration_file, "w+") as outhandle:
            outhandle.write(updated_config_file)
