import asyncio
import logging
import os
import sys
import signal
import subprocess
from datetime import datetime, timedelta
import uuid
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.errors import FloodWait, ChannelPrivate, MessageDeleteForbidden
from config import API_ID, API_HASH, BOT_TOKEN, SESSION, CHAT_IDS, ID_DUR
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
start_time = datetime.now()

scheduler = None
app = None
user = None
shutdown_event = None

async def process_delete(chat_id, msg_id):
    try:
        await app.delete_messages(chat_id, msg_id)
        logger.info(f"Deleted message {msg_id} from {chat_id}")
    except (ChannelPrivate, MessageDeleteForbidden):
        logger.warning(f"Cannot delete message {msg_id} in {chat_id} - no permission")
    except FloodWait as e:
        logger.warning(f"FloodWait for {e.value} seconds")
        await asyncio.sleep(e.value)
        await process_delete(chat_id, msg_id)
    except Exception as e:
        logger.error(f"Delete error {chat_id}:{msg_id} - {e}")

def schedule_deletion(chat_id, msg_id, duration):
    if duration:
        scheduler.add_job(
            process_delete,
            'date',
            run_date=datetime.now() + timedelta(seconds=duration),
            args=[chat_id, msg_id],
            id=f"delete_{uuid.uuid4().hex}"
        )

async def handle_messages(client, message, is_new=True, duration=None):
    duration = duration or ID_DUR.get(message.chat.id)
    if duration:
        schedule_deletion(message.chat.id, message.id, duration)

async def process_chat_history(chat_id, time_limit):
    try:
        duration = ID_DUR.get(chat_id)
        if not duration:
            return
            
        message_count = 0
        processed_ids = set()
        
        async for msg in user.get_chat_history(chat_id, limit=21000):
            if not msg.date or msg.date < time_limit:
                break
                
            if msg.id in processed_ids:
                continue
                
            await handle_messages(user, msg, is_new=False, duration=duration)
            processed_ids.add(msg.id)
            
            message_count += 1
            if message_count % 100 == 0:
                await asyncio.sleep(1)
                
        logger.info(f"Scheduled {message_count} messages for deletion in chat {chat_id}")
    except Exception as e:
        logger.error(f"Error processing chat history for {chat_id}: {e}")

async def handle_bot_commands(client, message):
    cmd = message.command[0].lower()

    if cmd in ["start"]:
        await message.reply_text(
            "**👋 Hello! I'm your Group Auto-Cleaner Bot.**\n\n"
            "I automatically **delete all messages** in groups after a fixed time interval to keep things **clean, clutter-free, and spam-free**."
        )

    elif cmd == "status":
        uptime = str(datetime.now() - start_time).split('.')[0]
        active_jobs = len(scheduler.get_jobs())
        await message.reply_text(
            f"**Bot Status**\n\n"
            f"• Uptime: `{uptime}`\n"
            f"• Active deletion jobs: `{active_jobs}`\n"
            f"• Monitored chats: `{len(CHAT_IDS)}`"
        )
    elif cmd == "ping":
        start = datetime.now()
        msg = await message.reply_text("Pinging...")
        latency = (datetime.now() - start).total_seconds()
        await msg.edit_text(f"🏓 Pong!\nLatency: `{latency:.3f}s`")

async def handle_user_commands(client, message):
    cmd = message.command[0].lower()

    if cmd == "delete":
        reply = await message.reply_text("Processing messages...")
        await delete_messages(reply)

    elif cmd == "update":
        try:
            msg = await message.reply_text("🔄 Checking for updates...")
            process = subprocess.run(["git", "pull"], capture_output=True, text=True)

            if process.returncode != 0:
                return await msg.edit_text(f"❌ Update failed:\n`{process.stderr}`")

            await msg.edit_text("✅ Update successful! Restarting bot...")
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            await message.reply_text(f"❌ Error occurred: {str(e)}")

    elif cmd == "restart":
        await message.reply_text("🔄 Restarting...")
        os.execl(sys.executable, sys.executable, *sys.argv)

    elif cmd == "chats":
        if not CHAT_IDS:
            await message.reply_text("⚠️ No chats are currently being monitored.")
        else:
            text = "**📝 Monitored Chats:**\n" + "\n".join([f"`{cid}`" for cid in CHAT_IDS])
            await message.reply_text(text)

async def delete_messages(reply=None):
    time_limit = datetime.now() - timedelta(hours=24)
    tasks = [process_chat_history(chat_id, time_limit) for chat_id in CHAT_IDS]
    await asyncio.gather(*tasks, return_exceptions=True)

    if reply:
        await reply.edit_text("Processing completed")

async def heartbeat():
    while not shutdown_event.is_set():
        try:
            uptime = str(datetime.now() - start_time).split('.')[0]
            active_jobs = len(scheduler.get_jobs())
            logger.info(f"Heartbeat - Bot running for {uptime}, active jobs: {active_jobs}")
            await asyncio.sleep(300)
        except Exception as e:
            logger.error(f"Heartbeat error: {e}")
            await asyncio.sleep(60)

async def main():
    global app, user, scheduler, shutdown_event

    loop = asyncio.get_running_loop()
    shutdown_event = asyncio.Event()

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: shutdown_event.set())

    scheduler = AsyncIOScheduler(event_loop=loop)
    scheduler.start()
    scheduler.add_job(delete_messages, 'interval', minutes=4, id="regular_cleanup")

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
        filters.private & filters.command(["delete", "update", "restart", "chats"]) & filters.private
    ))

    await app.start()
    await user.start()

    try:
        me = await user.get_me()
        await user.send_message(me.id, "✅ Bot has started and is running on your VPS.")
    except Exception as e:
        logger.error(f"Failed to send startup message: {e}")

    heartbeat_task = loop.create_task(heartbeat())

    try:
        await delete_messages()
        logger.info("Bot is now running on your VPS!")

        if not CHAT_IDS:
            logger.warning("No channels configured - bot will do nothing")

        await shutdown_event.wait()
    finally:
        if 'heartbeat_task' in locals() and not heartbeat_task.done():
            heartbeat_task.cancel()
            try:
                await heartbeat_task
            except asyncio.CancelledError:
                pass

        await asyncio.gather(
            app.stop() if app and app.is_connected else asyncio.sleep(0),
            user.stop() if user and user.is_connected else asyncio.sleep(0),
            return_exceptions=True
        )

        if scheduler and scheduler.running:
            scheduler.shutdown()

        logger.info("Cleanup complete. Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass