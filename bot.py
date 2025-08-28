import asyncio
import logging
import os
import sys
import signal
import subprocess
from datetime import datetime, timedelta
import uuid
import psutil
import aiohttp
from aiohttp import web
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.errors import FloodWait, ChannelPrivate, MessageDeleteForbidden
from config import API_ID, API_HASH, BOT_TOKEN, SESSION, CHAT_IDS, ID_DUR
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - 🤖 %(name)s - %(levelname)s - ✨ %(message)s'
)
logger = logging.getLogger(__name__)
start_time = datetime.now()

scheduler = None
app = None
user = None
web_app = None
shutdown_event = None
OWNER_ID = None

PORT = int(os.environ.get("PORT", 8080))
HOST = "0.0.0.0"

async def health_check(request):
    uptime = str(datetime.now() - start_time).split('.')[0]
    active_jobs = len(scheduler.get_jobs()) if scheduler else 0
    
    health_data = {
        "status": "healthy",
        "uptime": uptime,
        "active_jobs": active_jobs,
        "monitored_chats": len(CHAT_IDS),
        "timestamp": datetime.now().isoformat(),
        "bot_running": app.is_connected if app else False,
        "user_running": user.is_connected if user else False
    }
    
    return web.json_response(health_data)

async def root_handler(request):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Auto-Cleaner Bot</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{ 
                background: white; 
                padding: 30px; 
                border-radius: 10px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .status {{ 
                background: #e8f5e8; 
                padding: 15px; 
                border-radius: 5px; 
                border-left: 4px solid #4CAF50;
                margin: 20px 0;
            }}
            h1 {{ color: #333; }}
            .metric {{ margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Auto-Cleaner Bot</h1>
            <div class="status">
                <h3>✅ Bot Status: Running</h3>
                <div class="metric">⏳ Uptime: {str(datetime.now() - start_time).split('.')[0]}</div>
                <div class="metric">📌 Monitored Chats: {len(CHAT_IDS)}</div>
                <div class="metric">⚙️ Active Jobs: {len(scheduler.get_jobs()) if scheduler else 0}</div>
                <div class="metric">🕐 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
            </div>
            
            <h3>🔧 Features</h3>
            <ul>
                <li>🗑️ Automatic message deletion after set duration</li>
                <li>📊 Real-time monitoring and statistics</li>
                <li>🛡️ Admin commands for bot management</li>
                <li>⏰ Scheduled cleanup every 4 minutes</li>
                <li>🌐 Web dashboard for monitoring</li>
            </ul>
            
            <p><a href="/health">🩺 Health Check</a> | <a href="/stats">📊 Statistics</a></p>
        </div>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

async def stats_handler(request):
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        load_avg = psutil.getloadavg() if hasattr(psutil, "getloadavg") else (0, 0, 0)
        
        stats_data = {
            "uptime": str(datetime.now() - start_time).split('.')[0],
            "active_jobs": len(scheduler.get_jobs()) if scheduler else 0,
            "monitored_chats": len(CHAT_IDS),
            "system": {
                "cpu_percent": round(cpu_percent, 2),
                "memory_percent": round(memory.percent, 2),
                "memory_total_gb": round(memory.total / (1024**3), 2),
                "disk_percent": round(disk.percent, 2),
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "load_avg": [round(x, 2) for x in load_avg]
            },
            "bot_status": {
                "bot_connected": app.is_connected if app else False,
                "user_connected": user.is_connected if user else False,
                "scheduler_running": scheduler.running if scheduler else False
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return web.json_response(stats_data)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

async def create_web_app():
    webapp = web.Application()
    
    webapp.router.add_get('/', root_handler)
    webapp.router.add_get('/health', health_check)
    webapp.router.add_get('/stats', stats_handler)
    
    return webapp

async def start_web_server():
    global web_app
    
    web_app = await create_web_app()
    runner = web.AppRunner(web_app)
    await runner.setup()
    
    site = web.TCPSite(runner, HOST, PORT)
    await site.start()
    
    logger.info(f"🌐 Web server started on http://{HOST}:{PORT}")
    return runner

async def ping_web_server():
    base_url = f"http://localhost:{PORT}"
    
    while not shutdown_event.is_set():
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(f"{base_url}/health") as response:
                    if response.status == 200:
                        logger.debug(f"🏓 Web server ping successful: {response.status}")
                    else:
                        logger.warning(f"⚠️ Web server ping returned status: {response.status}")
        except Exception as e:
            logger.warning(f"💔 Web server ping failed: {e}")
        
        await asyncio.sleep(120)

async def process_delete(chat_id, msg_id):
    try:
        await app.delete_messages(chat_id, msg_id)
        logger.info(f"🗑️ Deleted message {msg_id} from {chat_id}")
    except (ChannelPrivate, MessageDeleteForbidden):
        logger.warning(f"🔒 Cannot delete message {msg_id} in {chat_id} - no permission")
    except FloodWait as e:
        wait_time = e.value
        logger.warning(f"⏳ FloodWait {wait_time}s for {chat_id}:{msg_id} - retrying after delay")
        await asyncio.sleep(wait_time)
        await process_delete(chat_id, msg_id)
    except Exception as e:
        logger.error(f"💥 Delete failed {chat_id}:{msg_id} - {e}")

def schedule_deletion(chat_id, msg_id, duration):
    if duration:
        job_id = f"delete_{uuid.uuid4().hex}"
        scheduler.add_job(
            process_delete,
            'date',
            run_date=datetime.now() + timedelta(seconds=duration),
            args=[chat_id, msg_id],
            id=job_id
        )
        logger.debug(f"⏰ Scheduled deletion of {msg_id} in {duration}s (Job: {job_id})")

async def handle_messages(client, message, is_new=True, duration=None):
    duration = duration or ID_DUR.get(message.chat.id)
    if duration:
        schedule_deletion(message.chat.id, message.id, duration)

async def process_chat_history(chat_id, time_limit):
    try:
        duration = ID_DUR.get(chat_id)
        if not duration:
            logger.info(f"⚠️ No duration set for chat {chat_id}, skipping history cleanup")
            return

        message_count = 0
        processed_ids = set()
        logger.info(f"🔍 Starting history cleanup for chat {chat_id}...")

        async for msg in user.get_chat_history(chat_id, limit=21000):
            if not msg.date or msg.date < time_limit:
                break

            if msg.id in processed_ids:
                continue

            await handle_messages(user, msg, is_new=False, duration=duration)
            processed_ids.add(msg.id)
            message_count += 1

            if message_count % 100 == 0:
                logger.info(f"📊 Processed {message_count} messages in {chat_id}")
                await asyncio.sleep(1)

        logger.info(f"✅ Scheduled {message_count} old messages for deletion in {chat_id}")

    except Exception as e:
        logger.error(f"❌ Failed to process history for {chat_id}: {e}")

async def handle_bot_commands(client, message):
    cmd = message.command[0].lower()

    if cmd == "start":
        await message.reply_text(
            "👋 **Hello! I'm your Group Auto-Cleaner Bot.**\n\n"
            "🗑️ I automatically **delete all messages** after a set time.\n"
            "✨ Keep your groups **clean, clutter-free, and spam-free!**\n\n"
            f"🌐 Web Dashboard: http://localhost:{PORT}"
        )

    elif cmd == "status":
        uptime = str(datetime.now() - start_time).split('.')[0]
        active_jobs = len(scheduler.get_jobs())

        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        load_avg = psutil.getloadavg() if hasattr(psutil, "getloadavg") else (0, 0, 0)

        status_text = (
            f"📊 **Bot Status**\n\n"
            f"⏳ Uptime: `{uptime}`\n"
            f"⚙️ Active Jobs: `{active_jobs}`\n"
            f"📌 Monitored Chats: `{len(CHAT_IDS)}`\n"
            f"🛡️ Status: `🟢 Running`\n"
            f"🌐 Web Server: `http://localhost:{PORT}`\n\n"
            f"💻 **System Stats**\n"
            f"🔹 CPU: `{cpu_percent}%`\n"
            f"🔹 RAM: `{memory.percent}% of {round(memory.total / (1024**3), 2)} GB`\n"
            f"🔹 Disk: `{disk.percent}% of {round(disk.total / (1024**3), 2)} GB`\n"
            f"🔹 Load Avg (1m, 5m, 15m): `{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}`"
        )

        await message.reply_text(status_text)

    elif cmd == "ping":
        start = datetime.now()
        msg = await message.reply_text("🏓 Pinging...")
        latency = (datetime.now() - start).total_seconds()
        await msg.edit_text(f"🏓 **Pong!**\n⏱️ Latency: `{latency:.3f}s`")

async def handle_user_commands(client, message):
    if message.from_user.id != OWNER_ID:
        logger.warning(f"🚫 Unauthorized command attempt by user {message.from_user.id}")
        return

    cmd = message.command[0].lower()
    logger.info(f"🛠️ Executing command: /{cmd} from owner")

    if cmd == "delete":
        reply = await message.reply_text("🔄 Processing messages...")
        await delete_messages(reply)

    elif cmd == "update":
        try:
            msg = await message.reply_text("📥 Checking for updates...")
            result = subprocess.run(["git", "pull"], capture_output=True, text=True)

            if result.returncode != 0:
                await msg.edit_text(f"❌ Update failed:\n```\n{result.stderr}\n```")
                return

            await msg.edit_text("✅ Update successful! 🔁 Restarting...")
            os.execl(sys.executable, sys.executable, *sys.argv)

        except Exception as e:
            await message.reply_text(f"💥 Error: `{str(e)}`")

    elif cmd == "restart":
        await message.reply_text("🔁 Restarting bot...")
        os.execl(sys.executable, sys.executable, *sys.argv)

    elif cmd == "chats":
        if not CHAT_IDS:
            await message.reply_text("⚠️ No chats are being monitored.")
        else:
            text = "📌 **Monitored Chats:**\n" + "\n".join([f"🔐 `{cid}`" for cid in CHAT_IDS])
            await message.reply_text(text)

    elif cmd == "webapp":
        await message.reply_text(
            f"🌐 **Web Dashboard Info:**\n\n"
            f"📍 URL: `http://localhost:{PORT}`\n"
            f"🩺 Health: `/health`\n"
            f"📊 Stats: `/stats`\n"
            f"🔧 Status: `{'🟢 Running' if web_app else '🔴 Stopped'}`"
        )

async def delete_messages(reply=None):
    time_limit = datetime.now() - timedelta(hours=24)
    tasks = [process_chat_history(chat_id, time_limit) for chat_id in CHAT_IDS]
    await asyncio.gather(*tasks, return_exceptions=True)

    if reply:
        queue_size = sum(1 for job in scheduler.get_jobs() if job.id.startswith("delete_"))
        await reply.edit_text(f"✅ Cleanup complete! 📦 {queue_size} deletions scheduled.")

async def heartbeat():
    while not shutdown_event.is_set():
        try:
            uptime = str(datetime.now() - start_time).split('.')[0]
            active_jobs = len(scheduler.get_jobs())
            web_status = "🟢" if web_app else "🔴"
            logger.info(f"💓 Heartbeat | ⏳ Up: {uptime} | 🛠️ Jobs: {active_jobs} | 🌐 Web: {web_status}")
            await asyncio.sleep(300)
        except Exception as e:
            logger.error(f"💔 Heartbeat failed: {e}")
            await asyncio.sleep(60)

async def main():
    global app, user, scheduler, shutdown_event, OWNER_ID

    loop = asyncio.get_running_loop()
    shutdown_event = asyncio.Event()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: shutdown_event.set())

    logger.info("🌐 Starting web server...")
    web_runner = await start_web_server()

    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.start()
    scheduler.add_job(delete_messages, 'interval', minutes=4, id="regular_cleanup")
    logger.info("⏰ Scheduler started with regular cleanup every 4 minutes.")

    app = Client("AutoWiperBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    user = Client("UserAutoWiper", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

    app.add_handler(MessageHandler(
        handle_bot_commands,
        filters=filters.command(["start", "status", "ping"]) & filters.private
    ))

    user.add_handler(MessageHandler(
        handle_messages,
        filters=filters.chat(CHAT_IDS) & ~filters.pinned_message
    ))

    user.add_handler(MessageHandler(
        handle_user_commands,
        filters.private & filters.command(["delete", "update", "restart", "chats", "webapp"])
    ))

    logger.info("🤖 Starting bot and user clients...")
    await app.start()
    await user.start()

    me = await user.get_me()
    OWNER_ID = me.id
    logger.info(f"🎯 Owner ID auto-set to: {OWNER_ID} (@{me.username or 'Unknown'})")

    ping_task = loop.create_task(ping_web_server())
    heartbeat_task = loop.create_task(heartbeat())

    try:
        await user.send_message(
            me.id,
            "✅ **Auto-Cleaner Bot Started!**\n\n"
            f"📊 Monitoring: `{len(CHAT_IDS)}` groups\n"
            f"🗑️ Auto-delete enabled\n"
            f"🛠️ Admin commands active for you only\n"
            f"🌐 Web Dashboard: `http://localhost:{PORT}`\n"
            f"ℹ️ Use `/status`, `/chats`, `/delete`, `/webapp` as needed."
        )
    except Exception as e:
        logger.error(f"📩 Failed to send startup message: {e}")

    try:
        await delete_messages()
        logger.info("🚀 Bot is now running with web server support! 🌐")

        if not CHAT_IDS:
            logger.warning("⚠️ No CHAT_IDS configured — bot will not monitor any chats.")

        await shutdown_event.wait()

    except Exception as e:
        logger.error(f"💥 Critical error: {e}")

    finally:
        logger.info("🛑 Shutting down gracefully...")

        for task in [ping_task, heartbeat_task]:
            if not task.done():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        await asyncio.gather(
            app.stop() if app and app.is_connected else asyncio.sleep(0),
            user.stop() if user and user.is_connected else asyncio.sleep(0),
            return_exceptions=True
        )

        if scheduler and scheduler.running:
            scheduler.shutdown()
            logger.info("📋 Scheduler stopped.")

        if web_runner:
            await web_runner.cleanup()
            logger.info("🌐 Web server stopped.")

        logger.info("✅ Bot stopped gracefully. Goodbye! 👋")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped manually by user.")