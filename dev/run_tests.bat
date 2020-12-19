
@echo off

echo ##### Calling: "%~nx0" (%0)

setlocal

set SCRIPT_DIR=%~dp0
set TEST_DIR=%SCRIPT_DIR%Testing
set ERROR_FOUND=
set ERROR_LIST=

echo ### Start Testing ###
call:run_tester "Pytest"        "%TEST_DIR%\RunPytest.bat"
rem call:run_tester "DjangoTests"   "%TEST_DIR%\RunDjangoTests.bat"
echo ### Testing finished ###

if defined ERROR_FOUND (
    goto error
) else (
    goto end
)

: #########################################
: ##### START OF FUNCTION DEFINITIONS #####
: #########################################
:run_tester
set TESTER_NAME=%~1
set TESTER_SCRIPT=%~2

echo ### TESTS START - '%TESTER_SCRIPT%' ###
call "%TESTER_SCRIPT%"

set return_code=%errorlevel%
echo return_code: %return_code%
if %return_code% gtr 0 (
    set ERROR_FOUND=TRUE
    set ERROR_LIST=%ERROR_LIST% %TESTER_NAME%
    echo   Issues Found
) else (
    echo   No Issues
)
echo ### TESTS END - '%TESTER_SCRIPT%' ###
echo[
goto:eof
: #######################################
: ##### END OF FUNCTION DEFINITIONS #####
: #######################################

:error
echo !!! CHECK OUTPUT, SOME TESTING ISSUE FOUND WITH
for %%a in (%ERROR_LIST%) do (
   echo   - %%a
)

endlocal
echo exit /B 1
exit /B 1

:end
echo !!! NO TESTING ISSUE FOUND
endlocal
echo exit /B 0
exit /B 0
