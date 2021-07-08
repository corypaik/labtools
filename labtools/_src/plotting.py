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
import os
from functools import lru_cache
from pathlib import Path

from labtools._src.util import maybe_import, require


@require('altair_saver')
@lru_cache(maxsize=None)
def altair_saver():
  """ Wrapper for altair_saver to patch vega paths for saving pdfs

  altair-saver requires vega-cli and vega-lite to be in your path *before*
  importing altair_saver. This function adds the vega-cli and vega-lite binaries
  to your path and returns the imported altaier_saver package.

  """
  # patch paths to vega binaries
  runfiles_dir = Path(os.getenv('PWD', os.getcwd())).parent
  node_modules = runfiles_dir / 'labtools__yarn/node_modules'
  os.environ["PATH"] += f":{node_modules}/vega-cli/bin"
  os.environ["PATH"] += f":{node_modules}/vega-lite/bin"

  # return the module
  return maybe_import('altair_saver')


def __altair_theme():
  colorscheme = 'tableau10'
  stroke_color = '333'
  title_size = 24
  label_size = 16
  line_width = 5

  return {
    'config': {
      'view': {
        'height': 500,
        'width': 600,
        'strokeWidth': 0,
        'background': 'white'},
      'title': {
        'fontSize': title_size},
      'range': {
        'category': {
          'scheme': colorscheme},
        'ordinal': {
          'scheme': colorscheme}},
      'axis': {
        'titleFontSize': title_size,
        'labelFontSize': label_size,
        'grid': False,
        'domainWidth': 5,
        'domainColor': stroke_color,
        'tickWidth': 3,
        'tickSize': 9,
        'tickCount': 4,
        'tickColor': stroke_color,
        'tickOffset': 0},
      'legend': {
        'titleFontSize': title_size,
        'labelFontSize': label_size,
        'labelLimit': 0,
        'titleLimit': 0,
        'orient': 'top-right',
        'padding': 10,
        'titlePadding': 10,
        'rowPadding': 5,
        'fillColor': 'white',
        'strokeColor': 'black',
        'cornerRadius': 0},
      'rule': {
        'size': 3,
        'color': '999',},
      'line': {
        'size': line_width,
        'opacity': 0.4},
      'text': {
        'fontSize': label_size}}}


def __plotly_theme():
  stroke_color = '#333333'
  title_size = 24
  label_size = 16
  line_width = 5

  font_base = {'color': 'black'}

  axis_base = {
    'titlefont': {
      **font_base, 'size': title_size},
    'showgrid': False,
    'showline': True,
    'linecolor': stroke_color,
    'linewidth': line_width,
    'zerolinecolor': 'white',
    'zerolinewidth': 0,
    'tickwidth': 3,
    'ticklen': 4,
    'ticks': 'outside',
    'tickcolor': stroke_color,
    'title': {
      'standoff': 0},
    'automargin': True}

  return {
    'layout': {
      'width': 600,
      'height': 500,
      'plot_bgcolor': 'white',
      'font': {
        **font_base, 'size': label_size},
      'title': {
        'font': {
          **font_base, 'size': title_size}},
      'xaxis': axis_base,
      'yaxis': axis_base,
      'legend': {
        'bordercolor': 'black',
        'borderwidth': 2,
        'yanchor': 'top',
        'y': 1,
        'xanchor': 'left',
        'x': 0.01,},
      'margin': {
        't': 0,
        'r': 0,
        'l': 65,
        'b': 65}}}


def setup_plotting_themes():
  """ Configure plotting themes for altair and plotly if installed. """
  # altair theme
  if alt := maybe_import('altair'):
    alt.themes.register('labtools', __altair_theme)
    alt.themes.enable('labtools')

  # plotly theme
  if plotly := maybe_import('plotly'):
    template = __plotly_theme()
    plotly.io.templates['labtools'] = template
    plotly.io.templates.default = 'labtools'
