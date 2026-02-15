from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from SONALI_MUSIC import app
from config import BOT_USERNAME
from SONALI_MUSIC.utils.errors import capture_err
import httpx 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_txt = """**
<u>❃ 𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐢𝐠𝐧𝐨𝐫𝐞 𝐑𝐞𝐩𝐨𝐬 ❃</u>
 
✼ 𝙍𝙚𝙥𝙤 𝙏𝙤 𝙉𝙝𝙞 𝙈𝙞𝙡𝙚𝙜𝙖 😁
 
❉  पत्थर की मूरत के आगे सिर मत झुका जब कुछ ना बचे तो शैतान से नाता बाना !!  

✼ || [ꜰ𐓘ʟ𐓘ᴋ 𔘓 ᴍᴜꜱɪᴄ™♪ [ 𐓘𔘓ꜰ ](https://t.me/FalaqMusicbot?start=_tgr_I548BOJjYTg1)) ||
 
❊ ʀᴜη 24x7 ʟᴧɢ ϝʀєє ᴡɪᴛʜσᴜᴛ sᴛσᴘ**
"""




@app.on_message(filters.command("repo"))
async def start(_, msg):
    buttons = [
        [ 
          InlineKeyboardButton("✙ ᴧᴅᴅ ϻє вᴧʙʏ ✙", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
        ],
        [
          InlineKeyboardButton("• Update •", url="https://t.me/FalakAbout"),
          InlineKeyboardButton("• Support •", url="https://t.me/falakUpdate"),
          ],
[
InlineKeyboardButton("• ϻᴧɪη ʙσᴛ •", url=f"https://t.me/FalaqMusicbot"),

        ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await msg.reply_photo(
        photo="https://litter.catbox.moe/k2zjdk.jpg",
        caption=start_txt,
        reply_markup=reply_markup
    )
