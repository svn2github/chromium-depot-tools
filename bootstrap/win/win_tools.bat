@echo off
:: Copyright (c) 2009 The Chromium Authors. All rights reserved.
:: Use of this source code is governed by a BSD-style license that can be
:: found in the LICENSE file.

:: This script will try to find if svn and python are accessible and it not,
:: it will try to download it and 'install' it in depot_tools.

:: Sadly, we can't use SETLOCAL here otherwise it ERRORLEVEL is not correctly
:: returned.

set WIN_TOOLS_ROOT_URL=http://src.chromium.org/svn/trunk/tools
set WIN_TOOLS_ROOT_DIR=%~dp0..\..

if "%1" == "force" (
  set WIN_TOOLS_FORCE=1
  shift /1
)

:SVN_CHECK
:: If the batch file exists, skip the svn check.
if "%WIN_TOOLS_FORCE%" == "1" goto :SVN_INSTALL
if exist "%WIN_TOOLS_ROOT_DIR%\svn.bat" goto :PYTHON_CHECK
call svn --version 2>nul 1>nul
if errorlevel 1 goto :SVN_INSTALL
goto :PYTHON_CHECK


:SVN_INSTALL
echo Installing subversion ...
:: svn is not accessible; check it out and create 'proxy' files.
if exist "%~dp0svn.7z" del "%~dp0svn.7z"
cscript //nologo //e:jscript "%~dp0get_file.js" %WIN_TOOLS_ROOT_URL%/third_party/svn_win_client.zip "%~dp0svn.zip"
if errorlevel 1 goto :SVN_FAIL
:: Cleanup svn directory if it was existing.
if exist "%WIN_TOOLS_ROOT_DIR%\svn\." rd /q /s "%WIN_TOOLS_ROOT_DIR%\svn"
cscript //nologo //e:jscript "%~dp0unzip.js" "%~dp0svn.zip" "%WIN_TOOLS_ROOT_DIR%"
if errorlevel 1 goto :SVN_FAIL
if not exist "%WIN_TOOLS_ROOT_DIR%\svn\." goto :SVN_FAIL
del "%~dp0svn.zip"
:: Create the batch file.
call copy /y "%~dp0svn.new.bat" "%WIN_TOOLS_ROOT_DIR%\svn.bat" 1>nul
goto :PYTHON_CHECK


:SVN_FAIL
echo ... Failed to checkout svn automatically.
echo Please visit http://subversion.tigris.org to download the latest subversion client
echo before continuing.
echo You can also get the "prebacked" version used at %WIN_TOOLS_ROOT_URL%/third_party/
set ERRORLEVEL=1
goto :END


:PYTHON_CHECK
:: If the batch file exists, skip the python check.
if "%WIN_TOOLS_FORCE%" == "1" goto :PYTHON_INSTALL
set ERRORLEVEL=0
if exist "%WIN_TOOLS_ROOT_DIR%\python.bat" goto :END
call python --version 2>nul 1>nul
if errorlevel 1 goto :PYTHON_INSTALL

:: We are done.
set ERRORLEVEL=0
goto :END


:PYTHON_INSTALL
echo Installing python ...
:: Cleanup python directory if it was existing.
if exist "%WIN_TOOLS_ROOT_DIR%\python\." rd /q /s "%WIN_TOOLS_ROOT_DIR%\python"
call svn co -q %WIN_TOOLS_ROOT_URL%/third_party/python "%WIN_TOOLS_ROOT_DIR%\python"
if errorlevel 1 goto :PYTHON_FAIL
:: Create the batch file.
call copy /y "%~dp0python.new.bat" "%WIN_TOOLS_ROOT_DIR%\python.bat" 1>nul
set ERRORLEVEL=0
goto :END


:PYTHON_FAIL
echo ... Failed to checkout python automatically.
echo Please visit http://python.org to download the latest python 2.x client before
echo continuing.
echo You can also get the "prebacked" version used at %WIN_TOOLS_ROOT_URL%/third_party/
set ERRORLEVEL=1
goto :END


:returncode
set WIN_TOOLS_ROOT_URL=
set WIN_TOOLS_ROOT_DIR=
exit /b %ERRORLEVEL%

:END
call :returncode %ERRORLEVEL%
