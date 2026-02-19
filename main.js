const { app, BrowserWindow, Menu } = require('electron');
const path = require('path');
const { exec } = require('child_process');
const fs = require('fs');

function createWindow() {
    // 创建浏览器窗口
    const mainWindow = new BrowserWindow({
        width: 1280,
        height: 800,
        fullscreen: true, // 默认全屏
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            webSecurity: true
        },
        backgroundColor: '#f5f7fa', // 与 keyboard.html 背景色一致
        show: false, // 先隐藏，加载完再显示
        autoHideMenuBar: true // 自动隐藏菜单栏
    });

    // 加载 keyboard.html
    mainWindow.loadFile('keyboard.html');

    // 加载完成后显示窗口，避免白屏
    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
        mainWindow.focus(); // 确保获得焦点
    });

    // 禁用默认菜单
    Menu.setApplicationMenu(null);

    // 开发环境下打开开发者工具
    // mainWindow.webContents.openDevTools();
}

// 自动卸载 DMG 逻辑
function autoEjectDmg() {
    // 仅在 macOS 且是打包后的应用中运行
    if (process.platform === 'darwin' && app.isPackaged) {
        // 扫描 /Volumes 目录，查找任何包含 "打字英雄" 的挂载点
        // 这样即使卷名包含版本号（如 "打字英雄 1.0.0"），也能正确识别
        const volumesDir = '/Volumes';
        
        fs.readdir(volumesDir, (err, files) => {
            if (err) return;
            
            // 找到所有匹配的卷
            const targetVolumes = files.filter(file => file.includes('打字英雄'));
            
            targetVolumes.forEach(volumeName => {
                const mountPoint = path.join(volumesDir, volumeName);
                
                // 只有当当前应用不是运行在这个卷里时，才尝试卸载
                // 这样避免了误删正在运行的 App 所在的 DMG
                if (!process.execPath.startsWith(mountPoint)) {
                    exec(`hdiutil detach "${mountPoint}"`, (error) => {
                        if (!error) {
                            console.log(`Successfully ejected DMG volume: ${volumeName}`);
                        }
                    });
                }
            });
        });
    }
}

// 当 Electron 完成初始化并准备创建浏览器窗口时调用此方法
app.whenReady().then(() => {
    // 尝试自动卸载残留的 DMG
    autoEjectDmg();

    createWindow();


    app.on('activate', function () {
        // macOS 应用通常在没有打开任何窗口的情况下也继续运行
        // 点击 dock 图标时如果没有窗口打开，则重新创建一个窗口
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

// 除了 macOS 外，当所有窗口都被关闭的时候退出程序
app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit();
});
