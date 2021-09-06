import asyncio
import logging


logging.getLogger("telethon").setLevel(logging.WARNING)
torlog = logging.getLogger(__name__)


async def backup_file(e):
  if not e.is_reply:
        await e.reply("Reply to Drive Upload Successfull Message.")
  elif not check_for_index(e):
        await e.reply("Index URL Button Not Present.")
  else:
    
    
    
def check_for_index(e):
  if (await e.get_reply_message()).buttons is None:
        return False
  for i in (await e.get_reply_message()).buttons:
        
  
