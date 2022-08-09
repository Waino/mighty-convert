# See LICENSE.md and ThirdPartyNotices.md for licensing information

import os
from pathlib import Path


def get_output_dir(model_name):
    repository_dir = str(os.path.abspath(os.path.join(__file__, "..", "output")))

    if os.path.isabs(model_name):
        # when converting a custom model from the local filesystem,
        # use the last path element instead of full path
        _, model_name = os.path.split(model_name)
    output_dir = Path(str(os.path.abspath(os.path.join(repository_dir, model_name))))
    return output_dir
