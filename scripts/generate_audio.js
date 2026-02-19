const https = require('https');
const fs = require('fs');
const path = require('path');

const API_KEY = 'sk-api-8cOnCUI2O-PFoPi3LzwNU5USJaz4OI819TF2_vTlhiDJnxwKsKmL1AnS560wSaPrzW883s-98Kna1fzFYcH4Xdt1TtDp6nmbqP6BoCVMnBVu53sRSDVcCKs';
// 尝试一个假的 GroupID，看看错误信息是否改变
const FAKE_GROUP_ID = '1234567890'; 

const OUTPUT_DIR = path.join(__dirname, '../audio_assets');
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR);
}

const texts = [
  { name: 'mock', text: "测试音频", voice: 'male-qn-qingse' }
];

async function generateAudio(item) {
  // 尝试 v1/text_to_speech 带 GroupId
  const url = `https://api.minimax.chat/v1/text_to_speech?GroupId=${FAKE_GROUP_ID}`; 
  
  const payload = JSON.stringify({
    model: 'speech-01-turbo',
    voice_setting: {
      voice_id: item.voice,
      speed: 1.0,
      vol: 1.0,
      pitch: 0
    },
    text: item.text
  });

  return new Promise((resolve, reject) => {
    const options = {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(url, options, (res) => {
      let responseData = '';
      res.on('data', (d) => { responseData += d; });
      res.on('end', () => {
          console.log(`Response for ${item.name}:`);
          console.log('Status:', res.statusCode);
          console.log('Body:', responseData);
          resolve();
      });
    });

    req.on('error', (e) => {
      console.error(`Problem with request: ${e.message}`);
      reject(e);
    });

    req.write(payload);
    req.end();
  });
}

generateAudio(texts[0]);
