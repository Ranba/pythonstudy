# VideoDown 🎬 — YouTube & Bilibili 高清视频下载工具使用文档

`VideoDown` 是一个基于 Python 3 开发的命令行视频下载工具。它封装了 `yt-dlp` 和 `ffmpeg`，旨在为用户提供一键式、最高画质音质的视频下载体验，并自动归档和清洗特殊字符。

---

## 📌 核心功能
* **最高画质音质**：自动下载最佳视频轨与音频轨，并使用 `ffmpeg` 无损合并为 MP4。
* **智能文件夹归档**：每个视频独立创建一个文件夹，视频、字幕及封面均保存在该文件夹内。
* **非法字符清洗**：自动将视频标题中 Windows/Linux 文件系统不支持的字符（如 `\ / : * ? " < > |`）替换为空格，避免路径报错。
* **精简字幕下载**：自动下载简体中文（`zh-Hans`）与英文（`en`）字幕，并转换为标准的 `.srt` 格式。
* **防限流保护**：内置 1 秒的请求延迟与出错忽略机制，防止因并发过多触发平台的 429 频率限制。
* **免打扰 Cookie 认证**：自动检测脚本目录下的 `cookies.txt`，绕过 YouTube 机器人验证。

---

## 🛠️ 依赖安装指南

要将此脚本移植到其他电脑上使用，目标电脑必须安装以下四个依赖项：

### 1. Python 3
脚本运行的基础环境。
* **Ubuntu / Debian**: `sudo apt install -y python3`
* **macOS**: `brew install python`
* **Windows**: 从 [官网](https://www.python.org/downloads/) 下载并安装，勾选 **"Add Python to PATH"**。

### 2. yt-dlp
负责解析视频链接与下载数据流。
* **通过 Pip 安装（推荐）**:
  ```bash
  pip install -U "yt-dlp[default]"
  ```
  *(注：带 `[default]` 选项会安装额外的解析加速依赖。)*
* **其他方式**: 参考 [yt-dlp 官方安装文档](https://github.com/yt-dlp/yt-dlp#installation)。

### 3. FFmpeg
负责将分离的高清视频轨与音频轨合并，以及嵌入缩略图封面。
* **Ubuntu / Debian**: 
  ```bash
  sudo apt update && sudo apt install -y ffmpeg
  ```
* **macOS**: 
  ```bash
  brew install ffmpeg
  ```
* **Windows**:
  1. 使用包管理器：`winget install Gyan.FFmpeg`
  2. 或从 [FFmpeg 官网](https://ffmpeg.org/download.html) 下载二进制包，并将其 `bin` 目录添加到系统的环境变量 `PATH` 中。

### 4. Deno (重要)
YouTube 采用动态参数限制（n-challenge）以防止自动化下载。`yt-dlp` 需要一个 JavaScript 运行时来实时解密。**Deno** 是官方推荐的引擎。
* **Ubuntu / Debian / macOS**:
  ```bash
  sudo apt install -y unzip # Linux 下安装 Deno 必须先有 unzip
  curl -fsSL https://deno.land/install.sh | sh
  
  # 配置环境变量（将其写入 ~/.bashrc 或 ~/.zshrc 中）
  export DENO_INSTALL="$HOME/.deno"
  export PATH="$DENO_INSTALL/bin:$PATH"
  ```
* **Windows (PowerShell)**:
  ```powershell
  irm https://deno.land/install.ps1 | iex
  ```
* **验证安装**：终端运行 `deno --version` 应能正确输出版本号。

---

## 🍪 如何获取并配置 `cookies.txt`

由于 YouTube 具有极严的防爬虫机制，直接匿名下载极易触发 `Sign in to confirm you're not a bot` 报错。此时必须配置浏览器 Cookie 才能正常下载。

### 获取步骤：
1. **安装浏览器扩展**：
   在 Chrome / Edge / Firefox 浏览器中搜索并安装扩展：**`Get cookies.txt LOCALLY`**。
   * [Chrome Web Store 链接](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
2. **登录平台**：
   在浏览器中打开并登录 [YouTube](https://www.youtube.com) (如果下载 Bilibili 大会员视频，则需登录 Bilibili)。
3. **导出 Cookie**：
   点击浏览器右上角的扩展图标，点击 **Export** 按钮，系统会提示保存一个名为 `youtube.com_cookies.txt` 的文件。
4. **放置到脚本目录**：
   将下载好的文件重命名为 **`cookies.txt`**，并直接放在 `videodown.py` 脚本的**同级目录下**。

> [!WARNING]
> * **Cookie 的时效性**：Cookie 会随着你在浏览器里登出、修改密码或 YouTube 的安全策略更迭而失效。如果下载再次报错 `Sign in to confirm you're not a bot`，重复上述步骤重新导出一次并替换 `cookies.txt` 即可。
> * **隐私安全**：`cookies.txt` 包含你的账户登录凭证，**切勿分享给他人**。

---

## 🚀 运行与移植

### 移植步骤：
1. 将 `videodown.py` 文件复制到新电脑的任意文件夹中。
2. 按照上面的 **[依赖安装指南]** 安装好 Python3、yt-dlp、FFmpeg 和 Deno。
3. 如果需要下载 YouTube 限制视频，将刚导出的 `cookies.txt` 放入该文件夹。

### 运行方式：
进入脚本所在目录，执行：
```bash
python3 videodown.py
```
**运行流程展示**：
1. 脚本启动，自动执行依赖项（`yt-dlp` 和 `ffmpeg`）检查。
2. 自动检索同级目录下的 `cookies.txt`。
3. 提示输入视频链接：
   ```text
   请输入视频链接（q 退出）：https://www.youtube.com/watch?v=xxxxxx
   ```
4. 脚本开始解析并下载，在当前目录下自动创建清洗好非法字符的同名文件夹，并将最终的 `.mp4` 和 `.srt` 归入其中。
5. 下载完成后，会询问是否继续下载。输入 `n` 或直接回车即可退出。
