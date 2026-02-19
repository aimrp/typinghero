# IMPLEMENTATION_PLAN - 实施计划与迭代步骤

本文件的目标是把「要做什么」拆成清晰的小步，让人或 AI 在实现 / 重构时有一个顺序可循，而不是一上来就“随便写点代码”。

> 说明：其中一部分步骤已经在当前版本中完成，依然保留在此，方便未来回溯或在新仓库中复用。

## 1. 初始化与基础结构

1.1 初始化项目
- 创建 Electron 项目结构，初始化 `package.json`。
- 安装开发依赖：
  - `electron@^40.4.1`
  - `electron-builder@^26.7.0`

1.2 配置打包
- 在 `package.json` 中配置 `build` 字段：
  - `appId` / `productName`；
  - Windows portable 目标；
  - macOS DMG 目标；
  - 图标路径与打包输出目录。

1.3 建立主进程入口
- 编写 `main.js`：
  - 创建浏览器窗口；
  - 加载 `keyboard.html`；
  - 处理基本的生命周期（关闭窗口等）。

## 2. 前端基础界面

2.1 搭建页面骨架
- 在 `keyboard.html` 中搭建三个主要区域：
  - 顶部：Logo + Combo 容器 + 控制按钮；
  - 中部：文本展示区 + 输入框；
  - 底部：虚拟键盘 + Canvas 画布。

2.2 实现基础样式
- 使用 CSS 完成：
  - 深色渐变背景；
  - 卡片式 UI 容器；
  - 按钮和输入框样式；
  - 虚拟键盘键帽布局。

## 3. 核心游戏逻辑

3.1 状态管理
- 在脚本中定义全局 `state` 对象：
  - 目标文本 / 拼音；
  - Combo、错误计数；
  - 计时信息（游戏总时长、当前句时长）；
  - BGM / SFX 开关状态；
  - 统计数据（平均 WPM、平均准确率等）。

3.2 素材与随机抽取
- 定义诗句素材库（数组），包含文本和来源信息。
- 实现随机抽取逻辑，避免短时间内重复。

3.3 输入校验
- 实现 `validateInput` 函数：
  - 前缀匹配；
  - 正确 / 错误判定；
  - Combo 增减规则；
  - WPM / 准确率 / 进度统计；
  - 句子完成判定。

3.4 慢速与超时检测
- 通过定时器定期检查当前句用时：
  - 10s / 20s / 30s：触发不同等级的嘲讽语音；
  - 60s：触发游戏结束逻辑。

## 4. 视听反馈与特效

4.1 AudioEngine
- 封装 `AudioEngine` 单例：
  - 预加载常用音频；
  - `playClick` / `playError` / `playVoice` / `switchBgm` 等方法；
  - BGM 动态切换（按 Combo 阶段）。

4.2 虚拟键盘与粒子
- 给虚拟键盘每个键定义 `data-key` 属性。
- 在键盘事件时：
  - 高亮对应键帽；
  - 在键帽位置生成火花粒子；
  - 通过 Canvas 渲染火花动画。

4.3 底部火焰与全屏烟花
- 基于 Combo 值：
  - 生成底部火焰粒子并持续渲染；
  - 在单句完成 / 通关时触发全屏烟花。

## 5. IME（输入法）兼容与优化

5.1 基础 IME 支持
- 监听输入框的：
  - `compositionstart` / `compositionupdate` / `compositionend`；
  - `input` / `beforeinput`。
- 在拼音组合阶段暂停正式前缀校验，上屏后再校验。

5.2 Windows + 搜狗拼音兼容
- 目标：在 Electron 打包版中，拼音输入阶段也有按键声音和虚拟键盘特效。
- 实施要点：
  - 通过全局 `keydown`/`keyup` 捕获事件，记录哪些按键有 keydown；
  - 对于只有 keyup 没有 keydown 的情况（如搜狗拼音组合阶段），在 keyup 时补发一次声音和特效；
  - 合理处理 `Process` 键与 `e.code` 的映射，让 `Process` + `KeyA` 还原为 `A` 等。

5.3 调试工具（内部使用）
- 在 keyboard.html 中保留隐藏的调试钩子：
  - 日志函数 `logEvent`；
  - 可以通过启用调试模式记录 IME 相关事件（keydown/keyup/beforeinput/composition/input）。
- 默认情况下 UI 中不展示调试按钮，不影响用户体验。

## 6. 文档体系与协作（当前步骤）

6.1 文档目录整理
- 创建 `docs/` 目录；
- 将 PRD 移至 `docs/PRD.md`，PRD 以产品与体验为主；
- 新增：
  - `docs/APP_FLOW.md`
  - `docs/TECH_STACK.md`
  - `docs/FRONTEND_GUIDELINES.md`
  - `docs/BACKEND_STRUCTURE.md`
  - `docs/IMPLEMENTATION_PLAN.md`（本文件）。

6.2 文档使用约定
- 在新增功能前：
  - 先更新 PRD 与相关文档；
  - 再开始实现。
- 在使用 AI 辅助开发时：
  - 把 docs 目录作为「唯一可信的规格来源」提供给 AI；
  - 明确要求按照文档约定实现或修改代码。

## 7. 后续迭代建议（占位）

> 以下是建议的未来迭代方向，具体细节需要在 PRD 和其他文档中进一步细化。

- 增加「关卡模式」与多难度配置；
- 增加「学生练习记录」和「教师查看面板」；
- 支持云端同步或多人排行榜；
- 增加更多键盘皮肤与主题；
- 为关键逻辑（如 validateInput）编写自动化测试，保证重构安全。

