<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>M4A → MP3 Converter</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/lamejs/1.2.1/lame.min.js"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Bebas+Neue&display=swap');

  * { margin: 0; padding: 0; box-sizing: border-box; }

  :root {
    --bg: #0a0a0a;
    --card: #111;
    --border: #222;
    --accent: #ff3c00;
    --accent2: #ff9500;
    --text: #f0f0f0;
    --muted: #555;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Space Mono', monospace;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    overflow: hidden;
  }

  body::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at 60% 40%, rgba(255,60,0,0.06) 0%, transparent 60%),
                radial-gradient(ellipse at 20% 80%, rgba(255,149,0,0.04) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
  }

  .container {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 520px;
  }

  .title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(2.5rem, 8vw, 4rem);
    letter-spacing: 4px;
    background: linear-gradient(135deg, #fff 30%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
  }

  .subtitle {
    color: var(--muted);
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 40px;
  }

  .drop-zone {
    border: 2px dashed var(--border);
    border-radius: 12px;
    padding: 48px 24px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    background: var(--card);
    position: relative;
    overflow: hidden;
  }

  .drop-zone::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,60,0,0.05), transparent);
    opacity: 0;
    transition: opacity 0.2s;
  }

  .drop-zone:hover, .drop-zone.dragover {
    border-color: var(--accent);
    transform: translateY(-2px);
  }

  .drop-zone:hover::before, .drop-zone.dragover::before {
    opacity: 1;
  }

  .drop-icon {
    font-size: 2.5rem;
    margin-bottom: 12px;
    display: block;
  }

  .drop-text {
    font-size: 0.85rem;
    color: var(--muted);
    line-height: 1.6;
  }

  .drop-text strong {
    color: var(--accent);
    display: block;
    font-size: 1rem;
    margin-bottom: 4px;
  }

  input[type="file"] { display: none; }

  .file-info {
    display: none;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px 20px;
    margin-top: 16px;
    font-size: 0.78rem;
    color: var(--muted);
  }

  .file-info.visible { display: flex; align-items: center; gap: 12px; }

  .file-name {
    color: var(--text);
    font-weight: 700;
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .file-size { color: var(--accent2); font-size: 0.72rem; }

  .btn {
    width: 100%;
    margin-top: 20px;
    padding: 16px;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 10px;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    letter-spacing: 3px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: none;
  }

  .btn.visible { display: block; }
  .btn:hover { background: #ff5722; transform: translateY(-1px); }
  .btn:disabled { background: var(--muted); cursor: not-allowed; transform: none; }

  .progress-wrap {
    display: none;
    margin-top: 20px;
  }

  .progress-wrap.visible { display: block; }

  .progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.72rem;
    color: var(--muted);
    margin-bottom: 8px;
  }

  .progress-bar-bg {
    background: var(--border);
    border-radius: 99px;
    height: 6px;
    overflow: hidden;
  }

  .progress-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    border-radius: 99px;
    width: 0%;
    transition: width 0.2s ease;
  }

  .status {
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 10px;
    min-height: 20px;
    text-align: center;
  }

  .status.error { color: #ff4444; }
  .status.success { color: #00e676; }

  .download-btn {
    display: none;
    width: 100%;
    margin-top: 16px;
    padding: 14px;
    background: transparent;
    border: 2px solid #00e676;
    color: #00e676;
    border-radius: 10px;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    letter-spacing: 3px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
    text-align: center;
  }

  .download-btn.visible { display: block; }
  .download-btn:hover { background: rgba(0,230,118,0.1); }

  .note {
    margin-top: 32px;
    font-size: 0.65rem;
    color: #333;
    text-align: center;
    line-height: 1.8;
    letter-spacing: 1px;
  }
</style>
</head>
<body>

<div class="container">
  <div class="title">M4A → MP3</div>
  <div class="subtitle">Converter / No Upload / Stays On Device</div>

  <div class="drop-zone" id="dropZone">
    <label for="fileInput" style="cursor:pointer; display:block;">
      <span class="drop-icon">🎵</span>
      <div class="drop-text">
        <strong>Drop your M4A file here</strong>
        or tap to browse
      </div>
    </label>
    <input type="file" id="fileInput" accept=".m4a,audio/mp4,audio/m4a">
  </div>

  <div class="file-info" id="fileInfo">
    <span>🎵</span>
    <span class="file-name" id="fileName"></span>
    <span class="file-size" id="fileSize"></span>
  </div>

  <button class="btn" id="convertBtn">Convert to MP3</button>

  <div class="progress-wrap" id="progressWrap">
    <div class="progress-label">
      <span>Converting...</span>
      <span id="progressPct">0%</span>
    </div>
    <div class="progress-bar-bg">
      <div class="progress-bar" id="progressBar"></div>
    </div>
  </div>

  <div class="status" id="status"></div>
  <a class="download-btn" id="downloadBtn" download="converted.mp3">⬇ Download MP3</a>

  <div class="note">
    CONVERSION HAPPENS IN YOUR BROWSER<br>
    YOUR AUDIO NEVER LEAVES YOUR DEVICE
  </div>
</div>

<script>
let selectedFile = null;

const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const convertBtn = document.getElementById('convertBtn');
const progressWrap = document.getElementById('progressWrap');
const progressBar = document.getElementById('progressBar');
const progressPct = document.getElementById('progressPct');
const status = document.getElementById('status');
const downloadBtn = document.getElementById('downloadBtn');

function formatSize(bytes) {
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function handleFile(file) {
  if (!file) return;
  selectedFile = file;
  fileName.textContent = file.name;
  fileSize.textContent = formatSize(file.size);
  fileInfo.classList.add('visible');
  convertBtn.classList.add('visible');
  downloadBtn.classList.remove('visible');
  status.textContent = '';
  status.className = 'status';
}

fileInput.addEventListener('change', e => handleFile(e.target.files[0]));

dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  handleFile(e.dataTransfer.files[0]);
});

convertBtn.addEventListener('click', async () => {
  if (!selectedFile) return;

  convertBtn.disabled = true;
  progressWrap.classList.add('visible');
  downloadBtn.classList.remove('visible');
  status.textContent = 'Decoding audio...';
  status.className = 'status';

  try {
    const arrayBuffer = await selectedFile.arrayBuffer();
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

    status.textContent = 'Encoding to MP3...';

    const channels = audioBuffer.numberOfChannels;
    const sampleRate = audioBuffer.sampleRate;
    const samples = audioBuffer.length;

    const mp3encoder = new lamejs.Mp3Encoder(channels === 1 ? 1 : 2, sampleRate, 128);
    const mp3Data = [];

    const left = audioBuffer.getChannelData(0);
    const right = channels > 1 ? audioBuffer.getChannelData(1) : left;

    const BLOCK = 1152;
    let processed = 0;

    function toInt16(floatArr, start, length) {
      const int16 = new Int16Array(length);
      for (let i = 0; i < length; i++) {
        const s = Math.max(-1, Math.min(1, floatArr[start + i]));
        int16[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
      }
      return int16;
    }

    function processChunk() {
      const end = Math.min(processed + BLOCK * 50, samples);
      for (let i = processed; i < end; i += BLOCK) {
        const blockSize = Math.min(BLOCK, samples - i);
        const l = toInt16(left, i, blockSize);
        const r = channels > 1 ? toInt16(right, i, blockSize) : l;
        const encoded = channels > 1
          ? mp3encoder.encodeBuffer(l, r)
          : mp3encoder.encodeBuffer(l);
        if (encoded.length > 0) mp3Data.push(encoded);
      }
      processed = end;
      const pct = Math.round((processed / samples) * 100);
      progressBar.style.width = pct + '%';
      progressPct.textContent = pct + '%';

      if (processed < samples) {
        setTimeout(processChunk, 0);
      } else {
        const final = mp3encoder.flush();
        if (final.length > 0) mp3Data.push(final);

        const blob = new Blob(mp3Data, { type: 'audio/mp3' });
        const url = URL.createObjectURL(blob);
        const outName = selectedFile.name.replace(/\.m4a$/i, '.mp3');

        downloadBtn.href = url;
        downloadBtn.download = outName;
        downloadBtn.classList.add('visible');
        downloadBtn.textContent = '⬇ Download ' + outName;

        status.textContent = '✅ Done! ' + formatSize(blob.size);
        status.className = 'status success';
        convertBtn.disabled = false;
      }
    }

    processChunk();

  } catch (err) {
    status.textContent = '❌ Error: ' + err.message;
    status.className = 'status error';
    convertBtn.disabled = false;
    progressWrap.classList.remove('visible');
  }
});
</script>
</body>
</html>
