@echo off

setlocal EnableDelayedExpansion

echo Args: %*

set SCRIPT_DIR=%~dp0
set FILE_ARG=%1


if [%1]==[] (
    goto set_all_files
) else (
    goto set_one_file
)

:set_all_files
pushd %SCRIPT_DIR%
for /R %%I in ("*.sh") do (
    echo TEST: %%I
    set REL_PATH=%%I
    echo # Current Permissions for "%%I"
    git ls-files --stage "%%I"
    git update-index --chmod=+x "%%I%"
    echo # New Permissions for "%%I"
    git ls-files --stage "%%I"
    echo ########################################################################
    echo[
)
popd


pushd %SCRIPT_DIR%..\scripts
for /R %%I in ("*.sh") do (
    echo TEST: %%I
    set REL_PATH=%%I
    echo # Current Permissions for "%%I"
    git ls-files --stage "%%I"
    git update-index --chmod=+x "%%I%"
    echo # New Permissions for "%%I"
    git ls-files --stage "%%I"
    echo ########################################################################
    echo[
)
popd



goto end

:set_one_file
echo File Argument: "%FILE_ARG%"
echo # Current Permissions for "%FILE_ARG%"
git ls-files --stage "%FILE_ARG%"
git update-index --chmod=+x "%FILE_ARG%"
echo # New Permissions for "%FILE_ARG%"
git ls-files --stage "%FILE_ARG%"
echo ########################################################################
echo[
goto end


:end
endlocal
