import asyncio as aio
import logging
import shutil
import os

from .. import transfer
from . import ariatools
from .backup_tele_upload import upload_handel
from ..functions.Leech_Module import check_link
from ..core.status.upload import TGUploadTask
from ..core.status.status import ARTask, MegaDl


logging.getLogger("telethon").setLevel(logging.WARNING)
torlog = logging.getLogger(__name__)


async def backup_file(e):
    if not e.is_reply:
        await e.reply("Reply to Drive Upload Successfull Message.")
    #elif not await check_for_index(e):
        #await e.reply("Index URL Button Not Present.")
    else:
        if await check_for_index(e):
            url = await index_url(e)
        else: #".*http.*" in (await e.get_reply_message()).raw_text:
            url = (await e.get_reply_message()).raw_text
        #url = await index_url(e)
        rmsg = await e.reply("**Processing the link...**")
        
        torlog.info("The aria2 Downloading:\n{}".format(url))
        await aio.sleep(1)
        
        rmsg = await e.client.get_messages(ids=rmsg.id, entity=rmsg.chat_id)
        
        re_name = None
        
        stat, dl_task = await ariatools.aria_dl(url, "", rmsg, e)
        
        if isinstance(dl_task, (ARTask, MegaDl)) and stat:
            path = await dl_task.get_path()
            ul_size = calculate_size(path)
            transfer[1] += ul_size  # for aria2 downloads
            
            
            try:
                rdict = await upload_handel(
                    path,
                    rmsg,
                    e.from_id,
                    dict(),
                    user_msg=e,
                    url=url
                   #task=ul_task,
                )
                await e.reply("Backup Complete.)
            except:
                rdict = dict()
                torlog.exception("Exception in Direct links.")

                
                await print_files(e, rdict, path=path, size=ul_size)
                torlog.info("Here are the files to be uploaded {}".format(rdict))
                
            
                
        elif stat is False:
                reason = await dl_task.get_error()
                await rmsg.edit("Failed to download this file.\n" + str(reason))
                await errored_message(e, rmsg)
        
        await clear_stuff(path)
    return None
     
    
    
async def check_for_index(e):
    if (await e.get_reply_message()).buttons is None:
        return False
    for i in (await e.get_reply_message()).buttons:
        for s in i:
            if s.text=="Index URL":
                return True
    return False
  
  
async def index_url(e):
    for i in (await e.get_reply_message()).buttons:
        for s in i:
            if s.text=="Index URL":
                return s.url
            
async def errored_message(e, reason):
    msg = f"<a href='tg://user?id={e.sender_id}'>Done</a>\nYour Download Failed."
    if reason is not None:
        await reason.reply(msg, parse_mode="html")
    else:
        await e.reply(msg, parse_mode="html")
            
def calculate_size(path):
    if path is not None:
        try:
            if os.path.isdir(path):
                return get_size_fl(path)
            else:
                return os.path.getsize(path)
        except:
            torlog.warning("Size Calculation Failed.")
            return 0
    else:
        return 0
            
def get_size_fl(start_path="."):
    total_size = 0
    for dirpath, _, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

async def clear_stuff(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except:
        pass
