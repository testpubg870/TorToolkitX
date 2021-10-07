import logging
import re, time
import urllib.parse

import aiohttp
from bs4 import BeautifulSoup

torlog = logging.getLogger(__name__)


async def generate_directs(url):
    # blocklinks
    if (
        "mega.nz" in url
        or "drive.google.com" in url
        or "uptobox.com" in url
        or "1fiecher.com" in url
        or "googleusercontent.com" in url
    ):
        return "**ERROR:** Unsupported URL!"

    # mediafire.com
    elif "mediafire.com" in url:
        try:
            link = re.findall(r"\bhttps?://.*mediafire\.com\S+", url)[0]
            async with aiohttp.ClientSession() as ttksess:
                resp = await ttksess.get(link)
                restext = await resp.text()

            page = BeautifulSoup(restext, "lxml")
            info = page.find("a", {"aria-label": "Download file"})
            ourl = info.get("href")
            return ourl
        except:
            return "**ERROR:** Cant't download, double check your mediafire link!"

    # disk.yandex.com
    elif "yadi.sk" in url or "disk.yandex.com" in url:
        try:
            link = re.findall(
                r"\b(https?://.*(yadi|disk)\.(sk|yandex)*(|com)\S+)", url
            )[0][0]
            print(link)
        except:
            return "**ERROR:** Cant't download, double check your yadisk link!"

        api = "https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}"
        try:
            async with aiohttp.ClientSession() as ttksess:
                resp = await ttksess.get(api.format(link))
                restext = await resp.json()
                ourl = restext["href"]
                return ourl
        except:
            torlog.exception("Ayee jooo")
            return "**ERROR:** Cant't download, the yadisk file not found or dowmload limit reached!"

    # zippyshare.com
    elif "zippyshare.com" in url:
        try:
            link = re.findall(r"\bhttps?://.*zippyshare\.com\S+", url)[0]
            async with aiohttp.ClientSession() as ttksess:
                resp = await ttksess.get(link)
                restext = await resp.text()
            base_url = re.search("http.+.com", restext).group()
            page_soup = BeautifulSoup(restext, "lxml")
            scripts = page_soup.find_all("script", {"type": "text/javascript"})
            for script in scripts:
                if "getElementById('dlbutton')" in script.text:
                    url_raw = re.search(
                        r"= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);", script.text
                    ).group("url")
                    math = re.search(
                        r"= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);", script.text
                    ).group("math")
                    url = url_raw.replace(math, '"' + str(eval(math)) + '"')
                    break
            ourl = base_url + eval(url)
            urllib.parse.unquote(url.split("/")[-1])
            return ourl
        except:
            return "**ERROR:** Cant't download, double check your zippyshare link!"

    # racaty.net
    elif "racaty.net" in url:
        try:
            link = re.findall(r"\bhttps?://.*racaty\.net\S+", url)[0]
            async with aiohttp.ClientSession() as ttksess:
                resp = await ttksess.get(link)
                restext = await resp.text()
            bss = BeautifulSoup(restext, "html.parser")
            op = bss.find("input", {"name": "op"})["value"]
            id = bss.find("input", {"name": "id"})["value"]

            async with aiohttp.ClientSession() as ttksess:
                rep = await ttksess.post(link, data={"op": op, "id": id})
                reptext = await rep.text()
            bss2 = BeautifulSoup(reptext, "html.parser")
            ourl = bss2.find("a", {"id": "uniqueExpirylink"})["href"]
            return ourl
        except:
            return "**ERROR:** Cant't download, double check your racaty link!"

    elif "pixeldrain.com" in url:
        url = url.strip("/ ")
        file_id = url.split("/")[-1]

        info_link = f"https://pixeldrain.com/api/file/{file_id}/info"
        dl_link = f"https://pixeldrain.com/api/file/{file_id}"

        async with aiohttp.ClientSession() as ttksess:
            resp = await ttksess.get(info_link)
            restext = await resp.json()

        if restext["success"]:
            return dl_link
        else:
            return "**ERROR:** Cant't download, {}.".format(restext["value"])
            
    # bayfiles.com and anonfiles.com
    elif "bayfiles.com" in url or "anonfiles.com" in url:
    	try:
    		async with aiohttp.ClientSession() as ttksess:
    		          resp = await ttksess.get(url)
    		          restext = await resp.text()
    		bss2 = BeautifulSoup(restext, "html.parser")
    		if (ourl := bss2.find(id="download-url")):
    			return ourl["href"]
    		elif (err := bss2.find(id="error-container")):
    			return "**ERROR:** " + (err.get_text()).strip()
    			
    	except:
    		return "**ERROR:** Can't Download, Check Your URL!"
    
    # letsupload.co, letsupload.io, letsupload.to
    elif "letsupload.co" in url or "letsupload.io" in url or "letsupload.to" in url:
    	if "letsupload.co" in url:
    		url = url.replace("letsupload.co", "letsupload.io")
    	if "letsupload.to" in url:
    		url = url.replace("letsupload.to", "letsupload.io")
    	try:
    		async with aiohttp.ClientSession() as ttksess:
    		          resp = await ttksess.get(url)
    		          restext = await resp.text()
    		          nurl = re.search("window.location = '(.*)'", restext).group(1)
    		          resp = await ttksess.get(nurl)
    		          restext = await resp.text()
    		          fileid = re.search("showFileInformation\((.*)\)", restext).group(1)
    		          return 'https://letsupload.io/account/direct_download/' + fileid
    	except:
    		return "**ERROR:** Can't Download, Check Your URL!"
    		
    #clicknupload.cc
    elif "clicknupload." in url:
    	try:
    		async with aiohttp.ClientSession() as ttksess:
    		          resp = await ttksess.get(url)
    		          restext = await resp.text()
    		          bss2 = BeautifulSoup(restext, "html.parser")
    		          form = bss2.find('form').findAll('input')
    		          data = ""
    		          for i in form:
    		          	data += "{}={}".format(i['name'], i['value'])
    		          	if i!=form[len(form)-1]:
    		          		data += "&"
    		          resp = await ttksess.post(url, data=data, headers={'content-type':'application/x-www-form-urlencoded'})
    		          restext = await resp.text()
    		          bss2 = BeautifulSoup(restext, "html.parser")
    		          form = bss2.find('form')
    		          fields = form.findAll('input')
    		          wait = int(form.find('span').find('span').get_text())
    		          ecode = (form.find('td').findAll('td')[1].findAll('span'))
    		          dcode  = {}
    		          for i in ecode:
    		          	dcode[int(re.search("padding-left:(\d+)px", str(i))[1])] = i.get_text()
    		          code = ""
    		          for i in sorted(dcode):
    		          	code +=(dcode[i])
    		          data = ""
    		          for i in fields:
    		          	try:
    		          		val = i['value']
    		          	except:
    		          		val = ""
    		          		if i['name'] == "code":
    		          			val = code
    		          	data += "{}={}".format(i['name'], val)
    		          	if i!=fields[len(fields)-1]:
    		          		data += "&"
    		          time.sleep(wait)
    		          resp = await ttksess.post(url, data=data, headers={'content-type':'application/x-www-form-urlencoded'})
    		          restext = await resp.text()
    		          bss2 = BeautifulSoup(restext, "html.parser")
    		          dlbtn = bss2.find(id="downloadbtn")
    		          return re.search("'(.*)'", dlbtn['onclick']).group(1)
    	except:
    		return "**ERROR:** Can't Download, Check Your URL!"


