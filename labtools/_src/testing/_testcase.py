# Copyright 2021 Cory Paik. All Rights Reserved.
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
""" TestCase with support for Arrays, Dataframes, and Tensors

Implementation inspired and adapted from `jax.test_util.JaxTestCase`.

References:
 [1] https://github.com/google/jax/blob/main/jax/test_util.py

"""

from functools import lru_cache
from types import ModuleType
from typing import Any, Dict, Optional, Union
import zlib

from absl.flags import FLAGS
from absl.testing import parameterized

from labtools._src.util import maybe_import
from labtools._src.util import require

# This testing library requires none of these. They are only needed for testing
# their associated datatypes, thus we will only need them if we use them.
jax = maybe_import('jax')
np = maybe_import('numpy')
pd = maybe_import('pandas')
jnp = maybe_import('jax.numpy')
_xla_client = maybe_import('jax._srx.lib.xla_client')
_xla_bridge = maybe_import('jax._src.lib.xla_bridge')

_dtype = lambda x: x.dtype

DType = Any


def _jax_x64_enabled():
  return jax and jax.config.x64_enabled


def is_sequence(x):
  try:
    iter(x)
  except TypeError:
    return False
  else:
    return True


if np:

  _dtype_to_32bit_dtype = {
      np.dtype('int64'): np.dtype('int32'),
      np.dtype('uint64'): np.dtype('uint32'),
      np.dtype('float64'): np.dtype('float32'),
      np.dtype('complex128'): np.dtype('complex64'),
  }

  # Trivial vectorspace datatype needed for tangent values of int/bool primals
  float0 = np.dtype([('float0', np.void, 0)])

  _default_tolerance_map = {
      float0: 0,
      np.dtype(np.bool_): 0,
      np.dtype(np.int8): 0,
      np.dtype(np.int16): 0,
      np.dtype(np.int32): 0,
      np.dtype(np.int64): 0,
      np.dtype(np.uint8): 0,
      np.dtype(np.uint16): 0,
      np.dtype(np.uint32): 0,
      np.dtype(np.uint64): 0,
      np.dtype(np.float16): 1e-3,
      np.dtype(np.float32): 1e-6,
      np.dtype(np.float64): 1e-15,
      np.dtype(np.complex64): 1e-6,
      np.dtype(np.complex128): 1e-15,
  }

# bfloat16 support
if jax and _xla_client:
  bfloat16: type = _xla_client.bfloat16
  _default_tolerance_map[np.dtype(bfloat16)] = 1e-2
else:
  bfloat16 = None


def _device_under_test() -> bool:
  return jax and _xla_bridge and (FLAGS.jax_test_dut or
                                  _xla_bridge.get_backend().platform)


@require('numpy', as_arg=True)
def _default_tolerance(np: ModuleType) -> Dict[DType, float]:
  if _device_under_test() != "tpu":
    return _default_tolerance_map
  tol = _default_tolerance_map.copy()
  tol[np.dtype(np.float32)] = 1e-3
  tol[np.dtype(np.complex64)] = 1e-3
  return tol


@require('numpy')
def _assert_numpy_allclose(a, b, atol=None, rtol=None, err_msg=''):
  if a.dtype == b.dtype == float0:
    np.testing.assert_array_equal(a, b, err_msg=err_msg)
    return
  a = a.astype(np.float32) if a.dtype == bfloat16 else a
  b = b.astype(np.float32) if b.dtype == bfloat16 else b
  kw = {}
  if atol:
    kw["atol"] = atol
  if rtol:
    kw["rtol"] = rtol
  with np.errstate(invalid='ignore'):
    np.testing.assert_allclose(a, b, **kw, err_msg=err_msg)


@lru_cache()
def _canonicalize_dtype(dtype):
  """Convert from a dtype to a canonical dtype based on config.x64_enabled."""
  try:
    dtype = np.dtype(dtype)
  except TypeError as e:
    raise TypeError(f'dtype {dtype!r} not understood') from e

  if _jax_x64_enabled:
    return dtype
  else:
    return _dtype_to_32bit_dtype.get(dtype, dtype)


@require('numpy')
def tolerance(dtype: str, tol: Optional[Union[Dict[str, float], float]] = None):
  tol = {} if tol is None else tol
  if not isinstance(tol, dict):
    return tol
  tol = {np.dtype(key): value for key, value in tol.items()}
  dtype = _canonicalize_dtype(np.dtype(dtype))
  return tol.get(dtype, _default_tolerance()[dtype])


class LzTestCase(parameterized.TestCase):

  def maybeSetUpNumpy(self):
    if np is not None:
      self.rng = np.random.RandomState(self.random_state)

  def maybeSetUpPandas(self):
    # Disable row/col limits so test errors are useful.
    if pd is not None:
      pd.options.display.max_rows = None
      pd.options.display.max_columns = None
      pd.options.display.max_colwidth = None
      pd.options.display.width = None

  def setUp(self):
    """ setup rng for random tests """
    super().setUp()
    # See: https://github.com/google/jax/blob/main/jax/test_util.py
    self.random_state = zlib.adler32(self._testMethodName.encode())

    self.maybeSetUpNumpy()
    self.maybeSetUpPandas()

  @require('numpy')
  def assertArraysEqual(self, x, y, *, check_dtypes=True, err_msg=''):
    """Assert that x and y arrays are exactly equal.[1] """
    if check_dtypes:
      self.assertDtypesMatch(x, y)
    # Work around https://github.com/numpy/numpy/issues/18992
    with np.errstate(over='ignore'):
      np.testing.assert_array_equal(x, y, err_msg=err_msg)

  @require('numpy')
  def assertArraysAllClose(self,
                           x,
                           y,
                           *,
                           check_dtypes=True,
                           atol=None,
                           rtol=None,
                           err_msg=''):
    """Assert that x and y are close (up to numerical tolerances)."""
    self.assertEqual(x.shape, y.shape)
    atol = max(tolerance(_dtype(x), atol), tolerance(_dtype(y), atol))
    rtol = max(tolerance(_dtype(x), rtol), tolerance(_dtype(y), rtol))

    _assert_numpy_allclose(x, y, atol=atol, rtol=rtol, err_msg=err_msg)

    if check_dtypes:
      self.assertDtypesMatch(x, y)

  def assertDtypesMatch(self, x, y, *, canonicalize_dtypes=True):
    if not _jax_x64_enabled() and canonicalize_dtypes:
      self.assertEqual(_canonicalize_dtype(_dtype(x)),
                       _canonicalize_dtype(_dtype(y)))
    else:
      self.assertEqual(_dtype(x), _dtype(y))

  @require('pandas')
  def assertDataframesAllClose(self,
                               a,
                               b,
                               aname='a',
                               bname='b',
                               tol=None,
                               tolerances=None):

    # check the index first
    pd = maybe_import('pandas')
    if pd is None:
      raise ImportError(
          'Attempted to test dataframes, but pandas is not installed.')
    pd.testing.assert_index_equal(a.index, b.index)
    pd.testing.assert_index_equal(a.columns, b.columns, obj='Columns')

    # Round first (tolerances)
    if tolerances is None:
      tolerances = tol
    if tolerances is not None:
      a = a.round(tolerances)
      b = b.round(tolerances)

    df_is_equal = a.compare(b)

    rename_map = {
        'self': aname,
        'other': bname,
    }

    if df_is_equal.any(None):
      cols = map(lambda c: (*c[:-1], rename_map[c[-1]]), df_is_equal.columns)
      df_is_equal.columns = pd.MultiIndex.from_tuples(cols)
      raise AssertionError('Mismatched elements:\n%s' % df_is_equal)

  def assertAllClose(self,
                     x,
                     y,
                     *,
                     check_dtypes=True,
                     atol=None,
                     rtol=None,
                     canonicalize_dtypes=True,
                     err_msg=''):
    """Assert that x and y, either arrays or nested tuples/lists, are close."""
    if isinstance(x, dict):
      self.assertIsInstance(y, dict)
      self.assertEqual(set(x.keys()), set(y.keys()))
      for k in x.keys():
        self.assertAllClose(x[k],
                            y[k],
                            check_dtypes=check_dtypes,
                            atol=atol,
                            rtol=rtol,
                            canonicalize_dtypes=canonicalize_dtypes,
                            err_msg=err_msg)
    elif is_sequence(x) and not hasattr(x, '__array__'):
      self.assertTrue(is_sequence(y) and not hasattr(y, '__array__'))
      self.assertEqual(len(x), len(y))
      for x_elt, y_elt in zip(x, y):
        self.assertAllClose(x_elt,
                            y_elt,
                            check_dtypes=check_dtypes,
                            atol=atol,
                            rtol=rtol,
                            canonicalize_dtypes=canonicalize_dtypes,
                            err_msg=err_msg)
    elif hasattr(x, '__array__') or np.isscalar(x):
      self.assertTrue(hasattr(y, '__array__') or np.isscalar(y))
      if check_dtypes:
        self.assertDtypesMatch(x, y, canonicalize_dtypes=canonicalize_dtypes)
      x = np.asarray(x)
      y = np.asarray(y)
      self.assertArraysAllClose(x,
                                y,
                                check_dtypes=False,
                                atol=atol,
                                rtol=rtol,
                                err_msg=err_msg)
    elif x == y:
      return
    else:
      raise TypeError((type(x), type(y)))

  def assertAllEqual(self,
                     x,
                     y,
                     *,
                     check_dtypes=True,
                     canonicalize_dtypes=True,
                     err_msg=''):
    """Assert that x and y, either arrays or nested tuples/lists, are close."""
    if isinstance(x, dict):
      self.assertIsInstance(y, dict)
      self.assertEqual(set(x.keys()), set(y.keys()))
      for k in x.keys():
        self.assertAllEqual(x[k],
                            y[k],
                            check_dtypes=check_dtypes,
                            canonicalize_dtypes=canonicalize_dtypes,
                            err_msg=err_msg)
    elif is_sequence(x) and not hasattr(x, '__array__'):
      self.assertTrue(is_sequence(y) and not hasattr(y, '__array__'))
      self.assertEqual(len(x), len(y))
      for x_elt, y_elt in zip(x, y):
        self.assertAllEqual(x_elt,
                            y_elt,
                            check_dtypes=check_dtypes,
                            canonicalize_dtypes=canonicalize_dtypes,
                            err_msg=err_msg)
    elif hasattr(x, '__array__') or np.isscalar(x):
      self.assertTrue(hasattr(y, '__array__') or np.isscalar(y))
      if check_dtypes:
        self.assertDtypesMatch(x, y, canonicalize_dtypes=canonicalize_dtypes)
      x = np.asarray(x)
      y = np.asarray(y)
      self.assertArraysEqual(x, y, check_dtypes=False, err_msg=err_msg)
    elif x == y:
      return
    else:
      raise TypeError((type(x), type(y)))
