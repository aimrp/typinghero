import requests
import json
import os
import time

# --- 配置部分 ---
# 请填入您的 Minimax API Key 和 Group ID
# 建议通过环境变量配置，或者创建一个 .env 文件 (不要提交到 Git)
API_KEY = os.getenv("MINIMAX_API_KEY", "YOUR_API_KEY_HERE")
GROUP_ID = os.getenv("MINIMAX_GROUP_ID", "YOUR_GROUP_ID_HERE")

# 检查是否配置了 Key
if API_KEY == "YOUR_API_KEY_HERE" or GROUP_ID == "YOUR_GROUP_ID_HERE":
    print("⚠️  警告: 请先配置 MINIMAX_API_KEY 和 MINIMAX_GROUP_ID 环境变量，或修改脚本中的默认值。")
    # 为了演示，不直接退出，但后续请求可能会失败


# 语音设置
VOICE_ID = "female-yujie" # 假设使用御姐音，具体 ID 需参考 Minimax 文档
SPEED = 1.0

# 输出目录
OUTPUT_DIR = "assets/audio/voice"

# 文案数据 (与 keyboard.html 中的 V2 版本保持一致)
audio_data = {
    # Level 10
    "mock_error_0": "才10秒？键盘都还没热身呢！",
    "mock_time_10_1": "10秒过去了，你是在思考人生吗？",
    "mock_time_10_2": "才10秒，别慌，还有机会追回来。",
    "mock_time_10_3": "10秒已过，请开始你的表演。",
    "mock_time_10_4": "键盘：我都等了10秒了，给点反应好吗？",
    "mock_time_10_5": "才过了10秒，不用这么紧张，深呼吸。",
    "mock_time_10_6": "10秒钟，足够高手打完半句诗了。",
    "mock_time_10_7": "嘿，10秒了，你的手指是不是粘住了？",
    
    "mock_error_1": "键盘：请给我一点压力，好吗？",
    "mock_error_2": "是不是拼音还在睡懒觉？",
    "mock_error_3": "发呆可以让时间变慢吗？并不能哦。",
    "mock_error_4": "你的手指是在做慢动作回放吗？",
    "mock_error_5": "这速度，蜗牛都要超车了！",
    "mock_error_6": "嘿，醒醒，还没到下课时间。",
    "mock_error_7": "键盘在等你长大吗？",
    "mock_error_8": "这个字不难，相信你自己。",
    "mock_error_9": "别停啊，连击都要断了！",

    # Level 20
    "mock_error_10": "20秒了，键盘快要睡着了。",
    "mock_time_20_1": "已经20秒了，手指动起来呀！",
    "mock_time_20_2": "20秒倒计时，留给你的时间不多了。",
    "mock_time_20_3": "20秒，如果是泡面都已经软了。",
    "mock_time_20_4": "加油加油，20秒而已，你能行的！",
    "mock_time_20_5": "20秒过去了，蜗牛都爬出三米远了。",
    "mock_time_20_6": "别发呆，20秒很宝贵的。",
    "mock_time_20_7": "20秒警报！你的速度需要提一提了。",
    
    "mock_error_11": "加油，你可以比树懒快一点。",
    "mock_error_12": "你是在用意念打字吗？",
    "mock_error_13": "键盘在呼唤你的手指！",
    "mock_error_14": "这种速度，网线都要着急了。",
    "mock_error_15": "是不是需要查一下字典？",
    "mock_error_16": "别犹豫，敲下去就是胜利。",
    "mock_error_17": "再不敲，键盘就要长草了。",
    "mock_error_18": "你的手速是被封印了吗？解开它！",
    "mock_error_19": "加油啊，后面的字都在排队等你。",

    # Level 30
    "mock_error_20": "30秒！灵感还在路上吗？",
    "mock_time_30_1": "30秒过半，加油冲刺！",
    "mock_time_30_2": "30秒了，别让键盘凉了。",
    "mock_time_30_3": "半分钟过去了，你的进度条还在散步吗？",
    "mock_time_30_4": "30秒！留给你的时间不多了，加速！",
    "mock_time_30_5": "已经30秒了，键盘在哭泣，你知道吗？",
    "mock_time_30_6": "30秒，足够喝杯水了，但你还在打这句。",
    "mock_time_30_7": "警报拉响！30秒了，快醒醒！",
    
    "mock_error_21": "这手速，抢不到第一名哦。",
    "mock_error_22": "别发呆了，时间在滴答滴答跑。",
    "mock_error_23": "和键盘做朋友，别怕它。",
    "mock_error_24": "看来你需要深呼吸一下。",
    "mock_error_25": "这种效率，作业什么时候能写完呀？",
    "mock_error_26": "是不是被这个字的美貌惊呆了？",
    "mock_error_27": "键盘：求求你，敲我一下吧。",
    "mock_error_28": "手指动起来，不要停！",
    "mock_error_29": "再不打完，天都要黑了。",

    # Level 60
    "mock_error_30": "一分钟了！键盘都等得花儿都谢了。",
    "mock_time_60_1": "一分钟到！游戏结束，下次加油。",
    "mock_time_60_2": "时间到！虽然超时了，但精神可嘉。",
    "mock_time_60_3": "一分钟！很遗憾，挑战失败，再接再厉。",
    "mock_time_60_4": "时间到！键盘已经尽力了，是你手速的问题。",
    "mock_time_60_5": "结束了！一分钟都没打完，我也很无奈啊。",
    "mock_time_60_6": "一分钟！虽然没通关，但你坚持到了最后。",
    "mock_time_60_7": "时间到！别灰心，下次一定能更快。",
    
    "mock_error_31": "这局游戏要变成马拉松了吗？",
    "mock_error_32": "我已经开始怀疑人生了，你呢？",
    "mock_error_33": "键盘都要长蘑菇了，真的。",
    "mock_error_34": "挑战一下自己，你可以更快的！",
    "mock_error_35": "别放弃，爆发你的小宇宙！",

    # Praise
    "praise_0": "太棒了！这手速简直逆天！",
    "praise_1": "完美！键盘都在为你欢呼！",
    "praise_2": "不可思议！你是闪电侠转世吗？",
    "praise_3": "这节奏，简直就是艺术！",
    "praise_4": "干得漂亮！继续保持！",
    "praise_5": "你是电，你是光，你是键盘的神话！",
    "praise_6": "这速度，我眼睛都快跟不上了！",
    "praise_7": "太强了！请收下我的膝盖！",
    "praise_8": "行云流水，一气呵成！",
    "praise_9": "这就是传说中的无影手吗？",
    "praise_10": "稳准狠！职业选手的水平！",
    "praise_11": "键盘侠中的战斗机！",
    "praise_12": "你的指尖在跳舞！",
    "praise_13": "这不仅是打字，这是享受！",
    "praise_14": "太快了，小心键盘起火！",
    "praise_15": "精准打击，例无虚发！",
    "praise_16": "你是怎么做到的？太厉害了！",
    "praise_17": "这手速，练了很久吧？",
    "praise_18": "简直就是打字机器！",
    "praise_19": "太丝滑了，像吃了巧克力一样！",
    "praise_20": "你的手指是装了马达吗？",
    "praise_21": "这波操作我给满分！",
    "praise_22": "秀得我头皮发麻！",
    "praise_23": "你是吃键盘长大的吗？",
    "praise_24": "这反应速度，绝了！",
    "praise_25": "键盘之神附体了！",
    "praise_26": "太疯狂了，根本停不下来！",
    "praise_27": "你的手速已经超越了人类极限！",
    "praise_28": "这才是真正的速度与激情！",
    "praise_29": "我都看呆了，太厉害了！",
    "praise_30": "这手速，不去弹钢琴可惜了！",
    "praise_31": "无敌是多么寂寞！",
    "praise_32": "你的键盘在燃烧！",
    "praise_33": "这就是传说中的人键合一！",

    # Game Over
    "gameover_0": "游戏结束！这成绩，还得再练练哦。",
    "gameover_1": "完了？就这？我还以为你能多坚持一会儿。",
    "gameover_2": "虽然失败了，但你成功地浪费了一分钟。",
    "gameover_3": "这水平，建议重新开始挑战。",
    "gameover_4": "键盘：我尽力了，是你还需要努力。",
    "gameover_5": "别灰心，虽然现在慢，但是你心态好啊。",
    "gameover_6": "这手速，离高手还有一段距离。",
    "gameover_7": "看来你需要多练习，熟能生巧。",
    "gameover_8": "游戏结束，你的自信心还在吗？",
    "gameover_9": "这操作，还有很大的进步空间。",
    "gameover_10": "我都看困了，终于结束了。",
    "gameover_11": "是不是键盘不听话？",
    "gameover_12": "没事，下次记得把手带上。",
    "gameover_13": "这成绩，只能说重在参与。",
    "gameover_14": "别气馁，至少你比树懒快一点点。",
    "gameover_15": "游戏结束，请接受现实的挑战。",
    "gameover_16": "这水平，连我奶奶都看不下去了。",
    "gameover_17": "承认吧，你需要更多的练习。",
    "gameover_18": "失败是成功之母，加油再来一次。",
    "gameover_19": "别放弃，下次一定能行！"
}

def generate_tts(text, filename):
    # 更新 API Endpoint 为 T2A v2
    url = f"https://api.minimax.chat/v1/t2a_v2?GroupId={GROUP_ID}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 使用 T2A v2 的参数结构
    data = {
        "model": "speech-01-turbo",
        "text": text,
        "stream": False, # 关闭流式返回，直接获取完整音频
        "voice_setting": {
            "voice_id": VOICE_ID,
            "speed": SPEED,
            "vol": 1.0,
            "pitch": 0
        },
        "audio_setting": {
            "sample_rate": 32000,
            "bitrate": 128000,
            "format": "mp3",
            "channel": 1
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            # 检查响应头是否为音频
            content_type = response.headers.get('content-type')
            if 'audio/mpeg' in content_type:
                with open(os.path.join(OUTPUT_DIR, f"{filename}.mp3"), "wb") as f:
                    f.write(response.content)
                print(f"✅ Generated: {filename}.mp3 -> {text}")
            elif 'application/json' in content_type:
                # 可能是 JSON 响应 (包含错误或 hex data)
                try:
                    resp_json = response.json()
                    if resp_json.get('base_resp', {}).get('status_code') == 0:
                        # 有些版本 v2 即使 stream=false 也可能返回 hex data 在 json 里
                        # 但通常 audio/mpeg 直接返回二进制
                        # 如果是 JSON 且成功，检查是否有 data.audio
                        if 'data' in resp_json and 'audio' in resp_json['data']:
                            audio_hex = resp_json['data']['audio']
                            with open(os.path.join(OUTPUT_DIR, f"{filename}.mp3"), "wb") as f:
                                f.write(bytes.fromhex(audio_hex))
                            print(f"✅ Generated (from JSON): {filename}.mp3 -> {text}")
                        else:
                             print(f"❌ Failed (JSON OK but no audio): {resp_json}")
                    else:
                        print(f"❌ Failed (API Error): {resp_json}")
                except Exception as e:
                    print(f"❌ Failed (Parse JSON): {response.text[:100]}...")
            else:
                print(f"❌ Failed (Unknown Content-Type): {content_type}")
        else:
            print(f"❌ Failed {filename}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error {filename}: {e}")
        
    # 增加延时以避免 RPM 限制
    # 检测到 RPM 限制，增加延时到 3 秒
    time.sleep(3.0)

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"Start generating {len(audio_data)} audio files...")
    
    for filename, text in audio_data.items():
        generate_tts(text, filename)
        
    print("Done!")

if __name__ == "__main__":
    main()
