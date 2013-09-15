..\..\pyinstaller\Build.py ../../build/radiance_debug.spec --noconfirm


copy ..\radiance.db ..\..\build\dist\radiance /y
xcopy ..\templates ..\..\build\dist\radiance\templates /e /i /h
xcopy ..\i18n ..\..\build\dist\radiance\i18n /e /i /h