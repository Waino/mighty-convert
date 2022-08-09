# See LICENSE.md and ThirdPartyNotices.md for licensing information

import os
import json
import requests
from pathlib import Path
from transformers import AutoModel, AutoTokenizer

from core import get_output_dir


def download_config(model_name):
    source = f"https://huggingface.co/{model_name}"
    url = f"{source}/raw/main/config.json"
    resp = requests.get(url=url)
    data = resp.json()
    data["name"] = model_name
    data["source"] = source
    output_dir = get_output_dir(model_name)
    config_path = output_dir.joinpath("config.json")
    with open(config_path, "w") as fd:
        json.dump(data, fd, indent=2)
    return data


def download(model_name):

    output_dir = get_output_dir(model_name)

    try:
        # get the model if there is one
        _ = AutoModel.from_pretrained(model_name)
    except Exception:
        print(f"Oops!  Couldn't download the model {model_name}")

    try:
        # get the tokenizer if there is one
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(
            save_directory=output_dir, legacy_format=False, push_to_hub=False
        )
    except Exception:
        print(f"Oops!  Couldn't download the tokenizer {model_name}")

    if not os.path.isabs(model_name):
        try:
            # get the config if there is one
            # config = AutoConfig.from_pretrained(model_name)
            config = download_config(model_name)
            print(config)
        except Exception:
            print(
                f"Oops!  Couldn't download "
                f"the model configuration {model_name}"
            )
    else:
        try:
            with open(output_dir / 'config.json', 'w') as fout:
                with open(Path(model_name) / 'config.json', 'r') as fin:
                    config = json.load(fin)
                    if 'name' not in config:
                        config['name'] = config.get('_name_or_path', 'unnamed')
                    if 'source' not in config:
                        config['source'] = 'local'
                    json.dump(config, fout, indent=2)
        except Exception:
            print(f"Oops!  Couldn't copy the config from {model_name}")
