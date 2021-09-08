import logging

logging.getLogger("telethon").setLevel(logging.WARNING)
torlog = logging.getLogger(__name__)

async def restore_single_file(e):
    if not e.is_reply:
        await e.reply("Reply to Backup Channel Message.")
    elif not await check_for_media(e):
        await e.reply("No Media In Replied Message.")
    else:
        e.reply("media found")
          
          
          
          
async def check_for_media(e):
    if (await e.get_reply_message()).media is None:
        return False
    else:
        return True
