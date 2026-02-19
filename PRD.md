# 打字英雄 (Typing Hero) - 产品需求文档 (PRD)

## 1. 项目概述

**打字英雄 (Typing Hero)** 是一款专为中小学生设计的趣味中文打字练习软件。它通过游戏化的激励机制（连击、特效、音效）、丰富的国学素材（古诗词）以及独特的“毒舌/暖心”语音反馈系统，解决传统打字练习枯燥乏味的问题，让用户在热血的氛围中提高打字速度和准确率。

## 2. 用户流程

1.  **启动应用**：进入全屏沉浸式界面，显示动态 Logo 和“开始游戏”遮罩层。
2.  **开始游戏**：点击按钮或按回车键，遮罩层消失，背景音乐启动，第一句诗词加载。
3.  **打字练习**：
    *   用户在输入框中输入显示的诗词。
    *   **正确输入**：字符变绿，连击数 (Combo) 增加，播放键盘音效。
    *   **错误输入**：输入框变红，连击数清零，播放错误音效和随机吐槽语音。
    *   **超时/停滞**：在 10s/20s/30s 无进度或慢速时，触发不同等级的语音催促；60s 未完成触发游戏结束。
4.  **完成单句**：
    *   输入完全正确后，触发烟花特效和夸奖语音。
    *   显示本句耗时统计。
    *   1秒后自动切换到下一句，且保持连击数。
5.  **游戏胜利/结束**：
    *   **通关**：连击数达到 200，触发终极胜利，满屏烟花，播放胜利语音。
    *   **失败**：单句耗时超过 60 秒，触发游戏结束，播放遗憾语音。
6.  **重玩/退出**：用户可随时点击顶部按钮重置游戏或退出应用。

## 3. 功能需求详解

### 3.1 核心游戏机制

*   **素材库**：
    *   内置大量唐诗、宋词、毛主席诗词及经典名句（带出处）。
    *   支持随机抽取，每次练习不重复（直至循环）。
*   **拼音辅助**：
    *   使用 `pinyin-pro` 库（或降级方案）自动为汉字标注拼音，辅助学生识字与输入。
*   **输入验证**：
    *   实时监听输入框内容。
    *   支持中文输入法（监听 `compositionstart` 和 `compositionend` 事件），在拼音选词阶段不触发校验，选词上屏后立即校验。
    *   **前缀匹配**：只有当输入内容完全匹配目标文本的前缀时才算正确。

### 3.2 连击 (Combo) 系统

这是游戏的核心激励机制：

*   **增加规则**：每正确输入一个字符，Combo +1。
*   **重置规则**：一旦输入错误字符（与目标文本不符），Combo 立即归零。
*   **保持规则**：单句完成后进入下一句时，Combo 数保持不变。
*   **视觉反馈**：
    *   **Combo 条**：顶部进度条随 Combo 数增长（0-200）。
    *   **动态计数器**：屏幕右侧显示巨大的 Combo 数字，每次增加都有缩放动画。
    *   **火焰特效**：
        *   Combo > 2: 显示计数器。
        *   Combo > 20: 计数器周围出现 CSS 呼吸火焰。
        *   Combo > 10: 底部键盘区域出现 Canvas 粒子火焰特效，强度随 Combo 增加。
*   **里程碑**：
    *   100 Combo / 200 Combo 时点亮对应图标。

### 3.3 音频系统 (AudioEngine)

音频是营造沉浸感的关键，包含 BGM、音效 (SFX) 和语音 (Voice)。

*   **背景音乐 (BGM)**：
    *   **动态切换**：根据 Combo 数切换曲目，情绪层层递进。
        *   Combo < 100: `waltz.mp3` (舒缓圆舞曲)
        *   100 <= Combo < 150: `bgm.mp3` (激昂，如土耳其进行曲)
        *   Combo >= 150: `v3.m4a` (高潮，如贝多芬悲怆第三乐章)
        *   游戏结束: `gameover.mp3`
    *   支持淡入淡出或断点续传（当前实现为直接切换）。
*   **音效 (SFX)**：
    *   **打字音**：机械键盘敲击声 (`clickonce.mp3`)，音调微随机化以模拟真实感。
    *   **错误音**：低沉的错误提示 (`wrong.mp3`)。
    *   **铃声**：时间警报 (10s/20s/30s) 播放急促铃声 (`hurryup.mp3`)。
    *   **爆炸/胜利**：Combo 里程碑或通关时播放 (`fireworks.mp3`)。
*   **语音反馈 (Voice)**：
    *   **机制**：单例播放器，避免重叠，支持优先级打断。
    *   **嘲讽 (Mockery)**：
        *   触发条件：单句耗时达到 10s, 20s, 30s 且未完成。
        *   内容库：分级嘲讽，时间越长语气越急促/毒舌。
    *   **夸奖 (Praise)**：
        *   触发条件：单句正确完成。
        *   内容库：随机播放“太棒了”、“手速逆天”等鼓励语。
    *   **游戏结束/胜利**：播放专用语音。

### 3.4 视觉特效系统

*   **UI 动画**：
    *   Logo 悬浮动画。
    *   输入框错误震动/变红。
    *   界面元素在胜利时“炸裂”散开 (`explode-out`)。
*   **粒子系统 (Canvas)**：
    *   **打字火花**：按键激活时，在对应键位生成向上飞溅的火星。
    *   **全屏烟花**：单句完成或通关时，在屏幕随机位置绽放彩色烟花。
    *   **底部火焰**：基于 Combo 数的持续燃烧火焰，颜色随 Combo 阶段变化（红 -> 蓝 -> 紫 -> 金）。

### 3.5 数据统计 (Dashboard)

*   **实时数据**：
    *   WPM (Words Per Minute)：基于当前句耗时计算。
    *   准确率：`Max(0, 100 - 错误次数 * 2)`。
    *   进度：当前句字符数 / 总字符数。
*   **全局数据**：
    *   平均 WPM。
    *   平均准确率。
    *   已完成句数。

## 4. 技术架构

### 4.1 技术栈

*   **Runtime**: Electron (主进程管理，跨平台打包)。
*   **Frontend**: 原生 HTML5 / CSS3 / JavaScript (ES6+)。
    *   无大型框架依赖 (如 React/Vue)，保证极速启动和低资源占用。
    *   Canvas API 用于粒子特效。
    *   Web Audio API / HTML5 Audio 用于音频管理。
*   **Build Tool**: `electron-builder` (打包为 DMG/EXE)。

### 4.2 文件结构

```
typinghero/
├── main.js                 # Electron 主进程入口
├── keyboard.html           # 游戏主界面 (包含所有逻辑与样式)
├── package.json            # 项目配置与依赖
├── audio_assets/           # 语音素材 (mp3)
├── audio_bgm/              # 背景音乐 (mp3/m4a)
├── tipssound/              # 音效素材 (mp3)
└── dist/                   # 打包产物
```

### 4.3 关键类/对象设计

*   **`state` (全局状态)**：
    *   管理 `targetText`, `combo`, `startTime`, `bgmEnabled` 等核心变量。
    *   管理各类定时器 (`gameTimerInterval`, `slowCheckTimer` 等)。
*   **`els` (DOM 缓存)**：
    *   缓存所有频繁操作的 DOM 节点，避免重复查询。
*   **`AudioEngine` (音频引擎)**：
    *   单例对象。
    *   方法：`init()`, `playVoice(file)`, `switchBgm(type)`, `playClick()`, `playExplosion()`。
    *   负责音频资源的预加载和播放控制。
*   **`FireParticle` / `Spark` / `Firework` (特效类)**：
    *   独立的粒子类，包含 `update()` 和 `draw()` 方法，由 `requestAnimationFrame` 驱动。

## 5. 详细逻辑规范 (用于 AI 生成代码)

### 5.1 输入校验逻辑 (`validateInput`)

```javascript
function validateInput(inputValue) {
    if (gameCompleted) return;

    // 1. 启动计时器 (如果是首个字符)
    if (!startTime) startTime = Date.now();

    // 2. 前缀匹配校验
    let isCorrect = true;
    for (let i = 0; i < inputValue.length; i++) {
        if (inputValue[i] !== targetText[i]) {
            isCorrect = false;
            break;
        }
    }

    // 3. 处理校验结果
    if (!isCorrect) {
        // 仅当输入长度增加时才判错 (避免删除操作触发错误)
        if (inputValue.length > lastInputLength) {
            triggerErrorEffect();
            errorCount++;
            combo = 0; // 重置连击
            AudioEngine.playError();
        }
    } else {
        // 输入正确
        clearErrorEffect();
        // 计算新增字符数，增加 Combo
        const diff = inputValue.length - lastInputLength;
        if (diff > 0) {
            combo += diff;
            checkBgmSwitch(combo); // 检查是否需要切换 BGM
            checkUltimateWin(combo); // 检查是否通关 (>200)
        }
    }

    // 4. 更新 UI
    renderTextHighlighting();
    updateDashboardStats();
    
    // 5. 检查是否完成
    if (inputValue === targetText) {
        completeSentence();
    }
    
    lastInputLength = inputValue.length;
}
```

### 5.2 慢速检测逻辑 (Timer Loop)

```javascript
// 每 100ms 执行一次
setInterval(() => {
    const elapsedSeconds = (Date.now() - currentSentenceStartTime) / 1000;
    
    // 游戏结束检测
    if (elapsedSeconds > 60) {
        triggerGameOver();
        return;
    }
    
    // 嘲讽检测 (仅当 Combo < 190 时)
    if (!completed && combo < 190) {
        if (elapsedSeconds == 10 && !triggered10) {
            AudioEngine.playVoice(getRandomMockery(10));
            triggered10 = true;
        }
        // 同理检测 20s, 30s...
    }
}, 100);
```

### 5.3 火焰特效逻辑

*   **Canvas**: 全屏覆盖，`z-index` 位于键盘下方。
*   **粒子生成**: 
    *   当 `combo > 10` 时，每帧以一定概率生成新粒子。
    *   粒子生成位置：键盘区域底部 (60%)、左侧 (20%)、右侧 (20%)。
    *   粒子颜色：HSL 模式，Hue 值随 Combo 变化 (0-30 橙红 -> 200-240 蓝 -> 260-300 紫 -> 30-50 金)。
*   **粒子行为**: 向上漂浮 (`vy < 0`)，左右随机扰动 (`vx`)，大小随生命周期减小，透明度随生命周期减小。
*   **循环控制**: 使用 `requestAnimationFrame`。当 `combo <= 10` 且无活跃粒子时，暂停循环以节省性能；当 `combo > 10` 时自动唤醒。

---
*本 PRD 由 AI 辅助生成，旨在完整描述“打字英雄”项目的业务逻辑与技术实现，可作为后续开发或重构的基准文档。*
