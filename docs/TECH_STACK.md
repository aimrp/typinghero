# TECH_STACK - 技术栈与依赖约定

本文件用于「锁定」打字英雄项目的技术栈与关键依赖版本，避免 AI 或协作者在实现和扩展功能时随意换技术、随便升版本。

## 1. 运行时与整体架构

- **应用类型**：桌面应用（Windows / macOS），通过 Electron 打包。
- **架构模式**：
  - Electron 主进程负责窗口创建与生命周期；
  - 渲染进程加载一个主页面（keyboard.html），在其中完成全部 UI 和逻辑；
  - 当前无独立后端服务，所有逻辑和状态在本地运行。

## 2. 具体技术栈

### 2.1 Electron 与 Node

- Electron：**40.4.1**（来自 package.json，使用 `^40.4.1`）
- Node：使用与 Electron 40 兼容的 Node 版本（建议 Node 20+）
- 打包工具：**electron-builder 26.7.0**

### 2.2 前端技术

- 语言与标准：
  - 原生 HTML5
  - 原生 CSS3
  - 原生 JavaScript（ES6+）
- 不使用：
  - 无 React / Vue / Angular 等大型框架
  - 无 TypeScript（目前）
- 图形与动画：
  - Canvas 2D API：键盘火花、底部火焰、全屏烟花粒子系统
  - CSS 动画与过渡：Logo 悬浮、按钮动效、错误震动等
- 音频：
  - HTML5 Audio 对象
  - 自封装的 AudioEngine（非第三方库）

### 2.3 第三方依赖

#### NPM 依赖（devDependencies）

来自 [package.json](file:///c:/workspace/typinghero/package.json#L65-L68)：

- `"electron": "^40.4.1"`
- `"electron-builder": "^26.7.0"`

> 当前 `package.json` 中没有声明前端运行时依赖，主要逻辑都在 keyboard.html 中以内联脚本的形式实现。

#### CDN 依赖

- 拼音库：`pinyin-pro`
  - 引入方式：CDN `<script src="https://unpkg.com/pinyin-pro"></script>`
  - 用途：为汉字生成拼音，辅助练习和输入。

> 如果未来需要在本地使用或做单元测试，可以考虑将 `pinyin-pro` 通过 npm 安装并显式加入依赖。

### 2.4 资源文件

- 音效 (SFX)：
  - `assets/audio/sfx/clickonce.mp3`
  - `assets/audio/sfx/wrong.mp3`
  - `assets/audio/sfx/fireworks.mp3`
  - `assets/audio/sfx/hurryup.mp3`
- 背景音乐 (BGM)：
  - `assets/audio/bgm/bgm.mp3`
  - `assets/audio/bgm/v3.m4a`
  - `assets/audio/bgm/waltz.mp3`
  - `assets/audio/bgm/gameover.mp3`
- 语音文案 (Voice)：
  - `assets/audio/voice/` 下的各种 mp3 文件，对应不同嘲讽/夸奖/提示语音。
- 图标与 Logo：
  - `assets/img/logo.png` 用于应用图标与安装包等。

## 3. 打包配置约定

来源：`package.json` 中的 `build` 字段。

### 3.1 基本信息

- `appId`: `com.xingguangdazi.app`
- `productName`: `打字英雄`
- 输出目录：`dist`

### 3.2 Windows

- 目标：`portable`
  - 生成：`dist\打字英雄_Portable_1.0.0.exe`
  - 适合作为「绿色版」单文件分发。
- 图标：`assets/img/logo.png`

### 3.3 macOS

- 目标：`dmg`
- 分类：`public.app-category.education`
- 图标：`assets/img/logo.png`
- DMG 布局：
  - 应用图标 + Applications 目录快捷方式

### 3.4 其他重要打包约定

- `files` 配置中明确排除了：
  - `dist/**/*`
  - `node_modules/**/*`
  - `package-lock.json`
- Windows 下还配置了 NSIS 相关选项（当前实际打包使用的是 portable 目标，NSIS 作为未来可选）：
  - `oneClick: false`
  - 支持用户选择安装目录
  - 自动创建桌面和开始菜单快捷方式

## 4. 运行环境与目标平台

- 目标用户主要在 **Windows** 平台使用：
  - 广泛兼容 Windows 10 及以上；
  - 默认使用系统中的中文输入法（微软拼音、搜狗拼音等）。
- macOS 支持：
  - 可打包为 DMG 安装包；
  - 体验上以全屏/窗口模式运行。

## 5. AI / 开发协作时的约束

当后续使用 AI 或有其他开发者参与时，请遵守以下约定：

1. **不要更换架构**：
   - 仍然以「Electron + 单页 keyboard.html」为基础；
   - 如需引入 React/Vue 等，必须先在文档中更新本文件并在实现前做明确记录。

2. **不要随意升级 Electron / electron-builder 大版本**：
   - 升级前需要在本文件中记录新版本号和升级原因；
   - 同时验证 IME 行为、打包脚本和音频/Canvas 兼容性。

3. **新增依赖需在此登记**：
   - 无论是 npm 包还是 CDN 引入，一律在此文件说明用途、版本和引入方式；
   - 避免「代码里偷偷多了一个库」的情况。

4. **技术方案变更优先更新文档**：
   - 先改 docs/TECH_STACK.md，再改代码；
   - 保证文档是整个项目的“单一事实来源”。
