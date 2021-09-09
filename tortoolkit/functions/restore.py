import logging
import os
import time
import asyncio as aio


logging.getLogger("telethon").setLevel(logging.WARNING)
torlog = logging.getLogger(__name__)

from .restore_progress import progress_for_pyrogram
from ..core.getVars import get_val

async def restore_single_file(e):
    if not e.is_reply:
        await e.reply("Reply to Backup Channel Message.")
    elif not await check_for_media(e):
        await e.reply("No Media In Replied Message.")
    else:
        rmsg = await e.reply("Processing Media.")
        start_time = time.time()
        tout = get_val("EDIT_SLEEP_SECS")
        path = (await e.get_reply_message()).raw_text
        file_id = (await e.get_reply_message()).file.id
        send_message = await reply_message.client.pyro.download_media(file_id,
                                                                      file_name=path,
                                                                      progress=progress_for_pyrogram,
                                                                      progress_args=(os.path.basename(path),
                                                                                     rmsg,
                                                                                     start_time,
                                                                                     tout,
                                                                                     e.client.pyro
                                                                                     ))
        
        
        await clear_stuff(path)
          
          
          
          
async def check_for_media(e):
    if (await e.get_reply_message()).media is None:
        return False
    else:
        return True
    
async def clear_stuff(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        torlog.warning("File(s) Deleted.")
    except:
        torlog.warning("Failed to Delete File(s).")
        pass
