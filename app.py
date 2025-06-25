from flask import Flask, request, render_template_string, send_file
import yt_dlp
import os

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head><title>YouTube to MP3</title></head>
<body>
    <h2>Download YouTube as MP3</h2>
    <form method="post">
        YouTube URL: <input type="text" name="url" required>
        <input type="submit" value="Download">
    </form>
    {% if filename %}
        <p>Download ready: <a href="/download/{{ filename }}">Click here</a></p>
    {% endif %}
</body>
</html>
'''

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    filename = None
    if request.method == 'POST':
        url = request.form['url']
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info['title']
            filename = f"{title}.mp3"
    return render_template_string(HTML, filename=filename)

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
