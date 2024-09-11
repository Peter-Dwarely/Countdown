import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=CountDown18_30',
    '--onefile',
    '--noconsole',
    '--upx-dir=C:\\Users\\HKPL711918\\Downloads\\upx-4.2.4-win64 (2)\\upx-4.2.4-win64',  # 修正路径
    'main1.py'
])
