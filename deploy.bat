@echo off
if [%1]==[] goto usage

@echo on
c:\apps\Google\google_appengine\appcfg.py --noauth_local_webserver -A %1 update .
goto :EOF

:usage
echo usage: %0 [app_id]
