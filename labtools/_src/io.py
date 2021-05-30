# Copyright 2021 The LabTools Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Union

import toolz.curried as T
from absl import logging

from labtools._src.util import (BestEffortJSONEncoder, CustomJSONEncoder,
                                require)


@require('yaml')
def load_and_check_yml(path: Union[str, Path], *loadkeys: list[str]):
  """ Loads and extract the specified key(s) from a yml file

    Args:
      path: Path to the yml file
      *loadkeys: Keys to load from the config file. These can either be shallow
        keys or deep addresses seperated as '/'. In the latter case, the file 
        will be flattened to find the objects recursively.  
   
    Returns:
      A list of Objects cooresponding to each key in loadkeys. Note that keys 
      not present will have a value of None
  """
  import yaml
  logging.debug('Loading YML from %s', path)

  # raw load
  with Path(path).open() as f:
    _loaded = yaml.safe_load(f)

  ret = list(T.map(lambda x: T.get_in(x.split('/'), _loaded), loadkeys))
  return ret


def dump_jsonl(path: Union[Path, str], data: list[dict[str, Any]],
               relaxed: bool = True) -> None:
  """ Dump to jsonl. 
  Args:
    path: Path to the jsonl file. 
    data: object to dump. 
    relaxed: predicate indicating whether to throw an error when part of the
      data cannot be encoded using CustomJSONEncoder. 
    mkdirs: make parent dirs if they don't exist
  """
  path = Path(path)
  path.parent.mkdir(exist_ok=True, parents=True)
  encoder_cls = BestEffortJSONEncoder if relaxed else CustomJSONEncoder
  path.write_text('\n'.join([json.dumps(obj, cls=encoder_cls) for obj in data]))


def load_jsonl(path: Union[Path, str]) -> list[dict[str, Any]]:
  """ Load from jsonl. """
  path = Path(path)
  return [json.loads(line) for line in path.read_text().splitlines()]
