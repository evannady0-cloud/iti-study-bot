import os
import subprocess
import gradio as gr

# Load token from environment or default
token = os.environ.get("TELEGRAM_BOT_TOKEN", "8744413280:AAEgvLcuwZ7vdo35V9ikU3hWEdplHer5pHE")
os.environ["TELEGRAM_BOT_TOKEN"] = token

# Start the Node.js ITI Study Telegram Bot in background
print("Starting ITI Telegram Bot process...")
bot_process = subprocess.Popen(["node", "bot.mjs"])

def get_status():
    poll = bot_process.poll()
    if poll is None:
        return "🟢 البوت شغال لايف 24/7 على تليجرام (@Studdyhelpbot) ومتصل بسيرفرات Hugging Face!"
    else:
        return f"🔴 Bot exited with code {poll}"

with gr.Blocks(theme=gr.themes.Soft(), title="ITI Study Bot") as demo:
    gr.Markdown("# 🎓 ITI Admission Exam Preparation Bot (@Studdyhelpbot)")
    gr.Markdown("""
    ### البوت شغال سحابياً 24/7 لخدمة المتقدمين لاختبارات معهد تكنولوجيا المعلومات ITI!
    - **6 نماذج IQ واقعية (40 سؤالاً لكل نموذج)**
    - **2 نموذج English (26 سؤالاً لكل نموذج)**
    - **شرح تفصيلي بالخطوات والقوانين الرياضية السريعة**
    - **زرار المساعدة المباشر: `[ ❓ مش عارف (اشرحلي الحل) ]`**
    
    👉 افتح تليجرام وابدأ التدريب الآن مع البوت: **[@Studdyhelpbot](https://t.me/Studdyhelpbot)**
    """)
    
    status_box = gr.Textbox(value=get_status, every=10, label="حالة السيرفر (Server Health)", interactive=False)
    refresh_btn = gr.Button("🔄 تحديث الحالة")
    refresh_btn.click(fn=get_status, outputs=status_box)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
