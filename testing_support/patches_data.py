# Copyright (c) 2011 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Samples patches to test patch.py."""


class RAW(object):
  PATCH = (
      'Index: chrome/file.cc\n'
      '===================================================================\n'
      '--- chrome/file.cc\t(revision 74690)\n'
      '+++ chrome/file.cc\t(working copy)\n'
      '@@ -3,6 +3,7 @@ bb\n'
      ' ccc\n'
      ' dd\n'
      ' e\n'
      '+FOO!\n'
      ' ff\n'
      ' ggg\n'
      ' hh\n')

  NEW = (
      '--- /dev/null\n'
      '+++ foo\n'
      '@@ -0,0 +1 @@\n'
      '+bar\n')

  NEW_NOT_NULL = (
      '--- file_a\n'
      '+++ file_a\n'
      '@@ -0,0 +1 @@\n'
      '+foo\n')

  MINIMAL_NEW = (
      '--- /dev/null\t2\n'
      '+++ chrome/file.cc\tfoo\n')

  MINIMAL = (
      '--- file_a\n'
      '+++ file_a\n')

  MINIMAL_RENAME = (
      '--- file_a\n'
      '+++ file_b\n')

  DELETE = (
      '--- tools/clang_check/README.chromium\n'
      '+++ /dev/null\n'
      '@@ -1,1 +0,0 @@\n'
      '-bar\n')

  MINIMAL_DELETE = (
      '--- chrome/file.cc\tbar\n'
      '+++ /dev/null\tfoo\n')

  # http://codereview.chromium.org/api/7530007/5001
  # http://codereview.chromium.org/download/issue7530007_5001_4011.diff
  CRAP_ONLY = (
      'Index: scripts/master/factory/skia/__init__.py\n'
      '===================================================================\n')


class GIT(object):
  """Sample patches generated by git diff."""
  PATCH = (
      'diff --git a/chrome/file.cc b/chrome/file.cc\n'
      'index 0e4de76..8320059 100644\n'
      '--- a/chrome/file.cc\n'
      '+++ b/chrome/file.cc\n'
      '@@ -3,6 +3,7 @@ bb\n'
      ' ccc\n'
      ' dd\n'
      ' e\n'
      '+FOO!\n'
      ' ff\n'
      ' ggg\n'
      ' hh\n')

  # http://codereview.chromium.org/download/issue6368055_22_29.diff
  DELETE = (
      'Index: tools/clang_check/README.chromium\n'
      'diff --git a/tools/clang_check/README.chromium '
          'b/tools/clang_check/README.chromium\n'
      'deleted file mode 100644\n'
      'index fcaa7e0e94bb604a026c4f478fecb1c5796f5413..'
          '0000000000000000000000000000000000000000\n'
      '--- a/tools/clang_check/README.chromium\n'
      '+++ /dev/null\n'
      '@@ -1,9 +0,0 @@\n'
      '-These are terrible, terrible hacks.\n'
      '-\n'
      '-They are meant \n'
      '-AND doing the normal \n'
      '-run during normal \n'
      '-build system to do a syntax check.\n'
      '-\n'
      '-Also see\n'
      '\n')

  # http://codereview.chromium.org/download/issue8508015_6001_7001.diff
  DELETE_EMPTY = (
      'Index: tests/__init__.py\n'
      'diff --git a/tests/__init__.py b/tests/__init__.py\n'
      'deleted file mode 100644\n'
      'index e69de29bb2d1d6434b8b29ae775ad8c2e48c5391..'
          '0000000000000000000000000000000000000000\n')

  # http://codereview.chromium.org/download/issue6250123_3013_6010.diff
  RENAME_PARTIAL = (
      'Index: chromeos/views/webui_menu_widget.h\n'
      'diff --git a/chromeos/views/DOMui_menu_widget.h '
          'b/chromeos/views/webui_menu_widget.h\n'
      'similarity index 79%\n'
      'rename from chromeos/views/DOMui_menu_widget.h\n'
      'rename to chromeos/views/webui_menu_widget.h\n'
      'index 095d4c474fd9718f5aebfa41a1ccb2d951356d41..'
          '157925075434b590e8acaaf605a64f24978ba08b 100644\n'
      '--- a/chromeos/views/DOMui_menu_widget.h\n'
      '+++ b/chromeos/views/webui_menu_widget.h\n'
      '@@ -1,9 +1,9 @@\n'
      '-// Copyright (c) 2010\n'
      '+// Copyright (c) 2011\n'
      ' // Use of this source code\n'
      ' // found in the LICENSE file.\n'
      ' \n'
      '-#ifndef DOM\n'
      '-#define DOM\n'
      '+#ifndef WEB\n'
      '+#define WEB\n'
      ' #pragma once\n'
      ' \n'
      ' #include <string>\n')

  # http://codereview.chromium.org/download/issue6287022_3001_4010.diff
  RENAME = (
      'Index: tools/run_local_server.sh\n'
      'diff --git a/tools/run_local_server.PY b/tools/run_local_server.sh\n'
      'similarity index 100%\n'
      'rename from tools/run_local_server.PY\n'
      'rename to tools/run_local_server.sh\n')

  COPY = (
      'diff --git a/PRESUBMIT.py b/pp\n'
      'similarity index 100%\n'
      'copy from PRESUBMIT.py\n'
      'copy to pp\n')

  COPY_PARTIAL = (
      'diff --git a/wtf b/wtf2\n'
      'similarity index 98%\n'
      'copy from wtf\n'
      'copy to wtf2\n'
      'index 79fbaf3..3560689 100755\n'
      '--- a/wtf\n'
      '+++ b/wtf2\n'
      '@@ -1,4 +1,4 @@\n'
      '-#!/usr/bin/env python\n'
      '+#!/usr/bin/env python1.3\n'
      ' # Copyright (c) 2010 The Chromium Authors. All rights reserved.\n'
      ' # blah blah blah as\n'
      ' # found in the LICENSE file.\n')

  NEW = (
      'diff --git a/foo b/foo\n'
      'new file mode 100644\n'
      'index 0000000..5716ca5\n'
      '--- /dev/null\n'
      '+++ b/foo\n'
      '@@ -0,0 +1 @@\n'
      '+bar\n')

  NEW_EXE = (
      'diff --git a/natsort_test.py b/natsort_test.py\n'
      'new file mode 100755\n'
      '--- /dev/null\n'
      '+++ b/natsort_test.py\n'
      '@@ -0,0 +1,1 @@\n'
      '+#!/usr/bin/env python\n')

  # To make sure the subdirectory was created as needed.
  NEW_SUBDIR = (
      'diff --git a/new_dir/subdir/new_file b/new_dir/subdir/new_file\n'
      'new file mode 100644\n'
      '--- /dev/null\n'
      '+++ b/new_dir/subdir/new_file\n'
      '@@ -0,0 +1,2 @@\n'
      '+A new file\n'
      '+should exist.\n')

  NEW_MODE = (
      'diff --git a/natsort_test.py b/natsort_test.py\n'
      'new file mode 100644\n'
      '--- /dev/null\n'
      '+++ b/natsort_test.py\n'
      '@@ -0,0 +1,1 @@\n'
      '+#!/usr/bin/env python\n')

  MODE_EXE = (
      'diff --git a/git_cl/git-cl b/git_cl/git-cl\n'
      'old mode 100644\n'
      'new mode 100755\n')

  MODE_EXE_JUNK = (
      'Index: Junk\n'
      'diff --git a/git_cl/git-cl b/git_cl/git-cl\n'
      'old mode 100644\n'
      'new mode 100755\n')
