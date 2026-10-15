@echo off
rem Compatibility for the earlier launcher path. Engine belongs to UI review.
call "%~dp0..\..\..\..\product-ui-review\vendor\impeccable\scripts\impeccable.cmd" %*
exit /b %errorlevel%
