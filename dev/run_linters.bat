
@echo off

echo ##### Calling: "%~nx0" (%0)

setlocal

set SCRIPT_DIR=%~dp0
set LINTER_DIR=%SCRIPT_DIR%Linting
set ERROR_FOUND=
set ERROR_LIST=

echo ### Start Linting ###
call:run_linter "Bandit"        "%LINTER_DIR%\RunBandit.bat"
rem call:run_linter "MyPy"          "%LINTER_DIR%\RunMyPy.bat"
call:run_linter "Pycodestyle"   "%LINTER_DIR%\RunPycodestyle.bat"
call:run_linter "Pydocstyle"    "%LINTER_DIR%\RunPydocstyle.bat"
call:run_linter "Pylint"        "%LINTER_DIR%\RunPylint.bat"
echo ### Linting finished ###

if defined ERROR_FOUND (
    goto error
) else (
    goto end
)

: #########################################
: ##### START OF FUNCTION DEFINITIONS #####
: #########################################
:run_linter
set LINTER_NAME=%~1
set LINTER_SCRIPT=%~2

echo ### LINTER START - '%LINTER_SCRIPT%' ###
call "%LINTER_SCRIPT%"

set return_code=%errorlevel%
if %return_code% gtr 0 (
    set ERROR_FOUND=TRUE
    set ERROR_LIST=%ERROR_LIST% %LINTER_NAME%
    echo   Issues Found
) else (
    echo   No Issues
)
echo ### LINTER END - '%LINTER_SCRIPT%' ###
echo[
goto:eof
: #######################################
: ##### END OF FUNCTION DEFINITIONS #####
: #######################################

:error
echo !!! CHECK OUTPUT, SOME LINTING ISSUE FOUND WITH
for %%a in (%ERROR_LIST%) do (
   echo   - %%a
)

endlocal
echo exit /B 1
exit /B 1

:end
echo !!! NO LINTING ISSUE FOUND
endlocal
echo exit /B 0
exit /B 0
