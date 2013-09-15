..\..\pyinstaller\Build.py ../../build/radiance.spec --noconfirm


copy ..\*.db ..\..\build\dist\radiance /y
xcopy ..\templates ..\..\build\dist\radiance\templates /e /i /h
xcopy ..\i18n ..\..\build\dist\radiance\i18n /e /i /h
xcopy ..\help ..\..\build\dist\radiance\help /e /i /h