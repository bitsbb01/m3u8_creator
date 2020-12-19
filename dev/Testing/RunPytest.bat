@echo off

setlocal

set PROJ_MAIN_DIR=%~dp0../..
set PACKAGE_ROOT=ez_m3u8_creator

set PYTHONPATH=%PYTHONPATH%;%PACKAGE_ROOT%
pushd "%PROJ_MAIN_DIR%"

rem To see how to loop through multiple Command Line Arguments: https://www.robvanderwoude.com/parameters.php

rem Disable Unwanted tests when run from Travis
if "%1"=="travis-ci" (
    rem add testing exclusions for travis
    rem set PYTEST_ADDOPTS=-m "(not ???)"
    echo Argument "travis-ci" passed, set "PYTEST_ADDOPTS" env variable
    goto run_tests
)

:local_setup

:run_tests
pytest --cov="%PACKAGE_ROOT%"
set return_code=%errorlevel%
if %return_code% equ 0 (
    echo *** No Pytest Issues Found
    goto exit_ok
) else (
    echo *** Some Pytest Issues Found
    goto exit_error
)

rem Some pytest resources
rem https://hackingthelibrary.org/posts/2018-02-09-code-coverage/
rem https://code.activestate.com/pypm/pytest-cov/
rem https://docs.pytest.org/en/latest/usage.html
rem http://blog.thedigitalcatonline.com/blog/2018/07/05/useful-pytest-command-line-options/
rem https://www.patricksoftwareblog.com/python-unit-testing-structuring-your-project/

:exit_error
popd
endlocal
echo exit /B 1
exit /B 1

:exit_ok
popd
endlocal
echo exit /B 0
exit /B 0
