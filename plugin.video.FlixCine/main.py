# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib
import urllib2
import re
import os
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
try:
    import json
except:
    import simplejson as json


if sys.argv[1] == 'limparMinhaLista':
    Path = xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('profile')).decode("utf-8")
    arquivo = os.path.join(Path, "favorites.dat")
    exists = os.path.isfile(arquivo)
    if exists:
        try:
            os.remove(arquivo)
        except:
            pass
        xbmcgui.Dialog().ok('Sucesso', '[B][COLOR white]Meus Favoritos limpo com sucesso![/COLOR][/B]')
        xbmc.sleep(2000)
    exit()


addon_handle = int(sys.argv[1])
__addon__ = xbmcaddon.Addon()
addon = __addon__
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
addon_version = __addon__.getAddonInfo('version')
profile = xbmc.translatePath(__addon__.getAddonInfo('profile').decode('utf-8'))
home = xbmc.translatePath(__addon__.getAddonInfo('path').decode('utf-8'))
icon_menu = home+'/icon_menu.png'
favorites = os.path.join(profile, 'favorites.dat')
favoritos = xbmcaddon.Addon().getSetting("favoritos")
if os.path.exists(favorites)==True:
    FAV = open(favorites).read()
else:
    FAV = []


def notify(message,name=False,iconimage=False,timeShown=5000):
    if name and iconimage:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (name, message, timeShown, iconimage))
    else:
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (__addonname__, message, timeShown, __icon__))


def _get_keyboard(default="",heading="",hidden=False ):
	""" shows a keyboard and returns a value """
	keyboard = xbmc.Keyboard(default,heading,hidden )
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		return unicode(keyboard.getText(),"utf-8")
	return default


def cat_principal(rec=False):
    lista=[
		("series", "Séries", "https://netcine.info/tvshows/"),
		("filmes", "Filmes", "https://netcine.info/?filmes")
		]
    if rec:
        for cat, name, url in lista:
            if cat == "series":
                name_resolve = "[B][COLOR white]"+name+" em DESTAQUE[/COLOR][/B]"
            else:
                name_resolve = "[B][COLOR white]"+name+" em DESTAQUE[/COLOR][/B]"
            addDir(name_resolve.encode('utf-8', 'ignore'),url.encode('utf-8'),6,'',icon_menu,'','',cat.encode('utf-8', 'ignore'), '')
    else:
        for cat, name, url in lista:
            if cat == "series":
                name_resolve = "[B][COLOR white]Pesquise FILMES e SÉRIES[/COLOR][/B]"
                addDir(name_resolve.encode('utf-8', 'ignore'),url.encode('utf-8'),7,'',icon_menu,'','',cat.encode('utf-8', 'ignore'), '')
                name_resolve2 = "[B][COLOR white]Meus Favoritos[/COLOR][/B]"
                desc2 = 'Pressione a tecla OK nas Séries ou Filmes ou clique o direito para Adicionar em Meus Favoritos e clique\nem Adicionar em Meus Favoritos.'
                addDir(name_resolve2.encode('utf-8', 'ignore'),url.encode('utf-8'),14,'',icon_menu,'',desc2,cat.encode('utf-8', 'ignore'), '')
            name_resolve = "[B][COLOR white]"+name+"[/COLOR][/B]"
            addDir(name_resolve.encode('utf-8', 'ignore'),url.encode('utf-8'),1,'',icon_menu,'','',cat.encode('utf-8', 'ignore'), '')
        cat_principal(rec=True)
        name_resolve1 = "[B][COLOR white]Gênero[/COLOR][/B]"
        addDir(name_resolve1.encode('utf-8', 'ignore'),'',8,'',icon_menu,'','','', '')
        name_resolve2 = "[B][COLOR white]Outros[/COLOR][/B]"
        name_resolve3 = "[B][COLOR white]=============[/COLOR][/B]"
        name_resolve4 = "[B][COLOR white]Configurações[/COLOR][/B]"
        try:
            url_outros = str(lista[0][2])
        except:
            url_outros = ''
        addDir(name_resolve2.encode('utf-8', 'ignore'),url_outros.encode('utf-8'),9,'',icon_menu,'','','', '')
        addDir(name_resolve3.encode('utf-8', 'ignore'),url_outros.encode('utf-8'),15,'',icon_menu,'','','', '')
        addDir(name_resolve4.encode('utf-8', 'ignore'),'',11,'',icon_menu,'','','', '')




def cat_genero():
    lista=[
		("acao", "Ação", "https://netcine.info/category/acao/"),
		("animacao", "Animação", "https://netcine.info/category/animacao/"),
        ("aventura", "Aventura", "https://netcine.info/category/aventura/"),
        ("biografia", "Biografia", "https://netcine.info/category/biografia/"),
        ("comedia", "Comédia", "https://netcine.info/category/comedia/"),
        ("crime", "Crime", "https://netcine.info/category/crime/"),
        ("documentario", "Documentário", "https://netcine.info/category/documentario/")
		]
    for cat, name, url in lista:
        name_resolve = "[B][COLOR white]"+name+"[/COLOR][/B]"
        addDir(name_resolve.encode('utf-8', 'ignore'),url.encode('utf-8'),1,'',icon_menu,'','',cat.encode('utf-8', 'ignore'), '')
    SetView('WideList')
    xbmcplugin.endOfDirectory(addon_handle)
    

def cat_outros(url):
    lista=[
		("vistos", "Filmes mais vistos"),
		("lancamento", "Ano de Lançamento"),
		]
    for cat, name in lista:
        name_resolve = "[B][COLOR white]"+name+"[/COLOR][/B]"
        addDir(name_resolve.encode('utf-8', 'ignore'),url.encode('utf-8'),10,'',icon_menu,'','',cat.encode('utf-8', 'ignore'), '')
    SetView('WideList')
    xbmcplugin.endOfDirectory(addon_handle)
        
        
    


def getRequest(url, ref):
    try:
        try:
            import urllib.request as urllib2
        except ImportError:
            import urllib2
        if ref > '':
            ref2 = ref
        else:
            ref2 = url
        request_headers = {
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": ref2
        }
        request = urllib2.Request(url, headers=request_headers)
        response = urllib2.urlopen(request).read().decode('utf-8')
        return response
    except:
        #pass
        response = ''
        return response



def fix_Synopsis(value):
    result = value.replace('&#8220;','“').replace('&#8221;','”').replace('&#8216;','"').replace('&#8217;','"').replace('&#8230;','…').replace('<span>','').replace('<span','').replace('class="yZlgBd">','').replace('style="color: #333333; font-family: Arial, sans-serif; font-size: 16px; background-color: #ffffff;">','').replace('</span>','').replace('\n\n\n','').replace('<p style="text-align: justify;">','').replace('</p>','').replace('\n\n','').replace('<p>','')
    return result


def convert_charactere(value, output):
    if output == "ascii":
        convert = value.encode("ascii", "xmlcharrefreplace").decode('utf-8')
        result = convert.replace("...","&#8230;").replace("&","&#038;").replace("–","&#8211;").replace("'","&#8217;").replace(" \n\n\t\t \n\t\t", "").replace("\n\t\t \n\t\t ", "").replace("\n", "").replace("\t", "")
    elif output == "utf-8":
        convert = value.encode("utf-8", "xmlcharrefreplace").decode('utf-8')
        result = convert.replace("#038;","").replace("&#192;","À").replace("&#193;","Á").replace("&#194;","Â").replace("&#195;","Ã").replace("&#196;","Ä").replace("&#224;","à").replace("&#225;","á").replace("&#226;","â").replace("&#227;","ã").replace("&#228;","ä").replace("&#200;","È").replace("&#201;","È").replace("&#202;","Ê").replace("&#203;","Ë").replace("&#232;","è").replace("&#233;","é").replace("&#234;","ê").replace("&#235;","ë").replace("&#204;","Ì").replace("&#205;","Í").replace("&#206;","Î").replace("&#207;","Ï").replace("&#236;","ì").replace("&#237;","í").replace("&#238;","î").replace("&#239;","ï").replace("&#211;","Ó").replace("&#243;","ó").replace("&#212;","Ô").replace("&#244;","ô").replace("&#244;","ô").replace("&#213;","Õ").replace("&#245;","õ").replace("&#217;","Ù").replace("&#218;","Ú").replace("&#219;","Û").replace("&#220;","Ü").replace("&#249;","ù").replace("&#250;","ú").replace("&#251;","û").replace("&#252;","ü").replace("&#199;","Ç").replace("&#231;","ç").replace("&#8230;","...").replace("&#038;","&").replace("&#8211;","–").replace("&#8217;","'").replace('&#147;','“').replace('&#148;','”').replace('&#34;','"').replace(" \n\n\t\t \n\t\t", "").replace("\n\t\t \n\t\t ", "").replace(r"\xc1","Á").replace(r"\xea","ê").replace(r"\xe7","ç").replace(r"\xe3","ã").replace(r"\xe9","é").replace(r"\xed","í").replace(r"\xe1","á").replace(r"\xe3","ó").replace(r"\xe0","à").replace(r"\xe0","à").replace(r"\xe2","â").replace("&#039;","'")
    else:
        result = value
    return result


def exibir_pagina(url,page,cat,pesquisa=False):
    if url > '':
        if cat == 'series':
            pageUrl = url + "page/" + str(int(page)) + "/"
        elif cat == 'filmes':
            pageUrl = url.replace('?filmes','') + "/page/" + str(int(page)) + "/?filmes"
        elif cat == 'lancamento':
            pageUrl = url + "/page/" + str(int(page)) + "/"
        elif pesquisa:
            pageUrl = url + "page/" + str(int(page)) + "/?s=" + pesquisa
        else:
            pageUrl = url + "page/" + str(int(page)) + "/"
        if int(page) == 1:
            if pesquisa:
                status,total = exibir_lista(url+"?s="+pesquisa)
            else:
                status,total = exibir_lista(url)
        else:           
            status,total = exibir_lista(pageUrl)
        if pesquisa and status == 'true' and int(page) < 3 and int(total) > 36:
            name = "[B][COLOR white]Pagina "+str(int(page) + 1)+"[/COLOR][/B]"
            li=xbmcgui.ListItem(name)
            u=sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + \
            "&url=" + urllib.quote_plus(url) + "&page=" + str(int(page) + 1) + "&pesquisa=" + urllib.quote_plus(pesquisa)
            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)            
        elif cat == 'series' and status == 'true' and int(page) < 7 and int(total) > 21:
            name = "[B][COLOR white]Pagina "+str(int(page) + 1)+"[/COLOR][/B]"
            li=xbmcgui.ListItem(name)
            u=sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + \
            "&url=" + urllib.quote_plus(url) + "&page=" + str(int(page) + 1) + "&cat=" + urllib.quote_plus(cat)
            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)
        elif cat == 'filmes' and status == 'true' and int(page) < 42 and int(total) > 21:
            name = "[B][COLOR white]Pagina "+str(int(page) + 1)+"[/COLOR][/B]"
            li=xbmcgui.ListItem(name)
            u=sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + \
            "&url=" + urllib.quote_plus(url) + "&page=" + str(int(page) + 1) + "&cat=" + urllib.quote_plus(cat)
            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)
        elif cat == 'acao' and status == 'true' and int(page) < 12 and int(total) > 21:
            name = "[B][COLOR white]Pagina "+str(int(page) + 1)+"[/COLOR][/B]"
            li=xbmcgui.ListItem(name)
            u=sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + \
            "&url=" + urllib.quote_plus(url) + "&page=" + str(int(page) + 1) + "&cat=" + urllib.quote_plus(cat)
            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)
        elif cat == 'animacao' and status == 'true' and int(page) < 5 and int(total) > 21:
            name = "[B][COLOR white]Pagina "+str(int(page) + 1)+"[/COLOR][/B]"
            li=xbmcgui.ListItem(name)
            u=sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + \
            "&url=" + urllib.quote_plus(url) + "&page=" + str(int(page) + 1) + "&cat=" + urllib.quote_plus(cat)
            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)
        elif cat == 'aventura' and status == 'true' and int(page) < 9 and int(total) > 21:
            name = "[B][COLOR white]Pagina "+str(int(page) + 1)+"[/COLOR][/B]"
            li=xbmcgui.ListItem(name)
            u=sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + \
            "&url=" + urllib.quote_plus(url) + "&page=" + str(int(page) + 1) + "&cat=" + urllib.quote_plus(cat)
            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)
        elif cat == 'biografia' and status == 'true' and int(page) < 3 and int(total) > 21:
            name = "[B][COLOR white]Pagina "+str(int(page) + 1)+"[/COLOR][/B]"
            li=xbmcgui.ListItem(name)
            u=sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + \
            "&url=" + urllib.quote_plus(url) + "&page=" + str(int(page) + 1) + "&cat=" + urllib.quote_plus(cat)
            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)
        elif cat == 'comedia' and status == 'true' and int(page) < 12 and int(total) > 21:
            name = "[B][COLOR white]Pagina "+str(int(page) + 1)+"[/COLOR][/B]"
            li=xbmcgui.ListItem(name)
            u=sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + \
            "&url=" + urllib.quote_plus(url) + "&page=" + str(int(page) + 1) + "&cat=" + urllib.quote_plus(cat)
            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)
        elif cat == 'crime' and status == 'true' and int(page) < 5 and int(total) > 21:
            name = "[B][COLOR white]Pagina "+str(int(page) + 1)+"[/COLOR][/B]"
            li=xbmcgui.ListItem(name)
            u=sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + \
            "&url=" + urllib.quote_plus(url) + "&page=" + str(int(page) + 1) + "&cat=" + urllib.quote_plus(cat)
            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)
        elif cat == 'documentario' and status == 'true' and int(page) < 3 and int(total) > 54:
            name = "[B][COLOR white]Pagina "+str(int(page) + 1)+"[/COLOR][/B]"
            li=xbmcgui.ListItem(name)
            u=sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + \
            "&url=" + urllib.quote_plus(url) + "&page=" + str(int(page) + 1) + "&cat=" + urllib.quote_plus(cat)
            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)
        elif cat == 'lancamento' and status == 'true' and int(total) > 55:
            name = "[B][COLOR white]Pagina "+str(int(page) + 1)+"[/COLOR][/B]"
            li=xbmcgui.ListItem(name)
            u=sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + \
            "&url=" + urllib.quote_plus(url) + "&page=" + str(int(page) + 1) + "&cat=" + urllib.quote_plus(cat)
            xbmcplugin.addDirectoryItem(addon_handle, u, li, True)
        xbmcplugin.setContent(addon_handle, 'movies')
        SetView('Wall')
        xbmcplugin.endOfDirectory(addon_handle)


def exibir_lista(pageUrl):
    data = getRequest(pageUrl, '')
    listRE_movies = re.compile('<div.+?class="movie">.+?<img src="(.+?)".+?<a href="(.+?)">.+?<div.+?class="imdb">.+?</span>(.+?)</div>.+?<h2>(.+?)</h2>.+?<span.+?class="year">(.+?)</span>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    if listRE_movies !=[]:
        for img, url, imdb, name, years in listRE_movies:
            thumbnail = img.replace('-120x170','')
            imdb_votes = imdb.replace(' ', '').replace('-', '')
            year = years.replace(' -','').replace('- ', '').replace('2020–', '2020').replace('2015–', '2015').replace('2016–', '2016').replace('1989–', '1989').replace('2013–', '2013').replace('2014–', '2014').replace('2010–', '2010').replace('1997–', '1997').replace('20142015', '2014-2015').replace('2011–', '2011').replace('2012–', '2012')
            title = '[B][COLOR white]'+convert_charactere(name, 'utf-8')+' - '+year+'[/COLOR]'+' [COLOR yellow] (Imdb '+imdb_votes+')[/COLOR][/B]'
            addDir(title.encode('utf-8', 'ignore'),url.encode('utf-8'),2,'',thumbnail.encode('utf-8'),'','','','',True,True)
            #addDir(name,url,mode,subtitle,iconimage,fanart,description,cat,episodes,folder=True)
        total = len(listRE_movies)
        status = 'true'
        return status,total 
    else:
        total = 0
        status = 'false'
        return status,total


def exibir_outros(url,cat,iconimage):
    data = getRequest(url, '')
    listRE_visto = re.compile('<li>.+?<b>(.+?)</b>.+?<a.+?href="(.+?)">(.+?)</a>.+?<i>(.+?)</i>.+?</li>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    listRE_lancamento = re.compile('<li><a.+?class="ito".+?HREF="(.+?)">(.+?)</a></li>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    if listRE_visto !=[] and cat == 'vistos':
        for number, url_movie, movie, years in listRE_visto:
            year = years.replace(' -','').replace('- ', '').replace('2020–', '2020').replace('2015–', '2015').replace('2016–', '2016').replace('1989–', '1989').replace('2013–', '2013').replace('2014–', '2014').replace('2010–', '2010').replace('1997–', '1997').replace('20142015', '2014-2015').replace('2011–', '2011').replace('2012–', '2012')
            title = '[B][COLOR white]'+number+' - '+convert_charactere(movie, 'utf-8')+' - '+year+'[/COLOR][/B]'
            addDir(title.encode('utf-8', 'ignore'),url_movie.encode('utf-8'),4,'',iconimage.encode('utf-8'),'','',cat.encode('utf-8', 'ignore'),'')
    elif listRE_lancamento !=[] and cat == 'lancamento':
        for url_year, years in listRE_lancamento:
            year = years.replace(' -','').replace('- ', '').replace('2020–', '2020').replace('2015–', '2015').replace('2016–', '2016').replace('1989–', '1989').replace('2013–', '2013').replace('2014–', '2014').replace('2010–', '2010').replace('1997–', '1997').replace('20142015', '2014-2015').replace('2011–', '2011').replace('2012–', '2012')
            title = '[B][COLOR white]'+year+'[/COLOR][/B]'
            addDir(title.encode('utf-8', 'ignore'),url_year.encode('utf-8'),1,'',iconimage.encode('utf-8'),'','',cat.encode('utf-8', 'ignore'),'')
    SetView('WideList')
    xbmcplugin.endOfDirectory(addon_handle)
            


def pesquisar(url):
    vq = _get_keyboard(heading="Digite algo para pesquisar")
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    exibir_pagina(url,1,'',title)
    

def exibir_recomendados(url):
    data = getRequest(url, '')
    listRE_rec = re.compile('<div.+?class="item">.+?<a href="(.+?)">.+?<img src="(.+?)".+?<div class="imdb">.+?</span>(.+?)</div>.+?<span class="ttps">(.+?)</span>.+?<span.+?class="ytps">(.+?)</span>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    if listRE_rec !=[]:
        for url, img, imdb, name, years in listRE_rec:
            thumbnail = img.replace('-120x170','')
            imdb_votes = imdb.replace(' ', '').replace('-', '')
            year = years.replace(' -','').replace('- ', '').replace('2020–', '2020').replace('2015–', '2015').replace('2016–', '2016').replace('1989–', '1989').replace('2013–', '2013').replace('2014–', '2014').replace('2010–', '2010').replace('1997–', '1997').replace('20142015', '2014-2015').replace('2011–', '2011').replace('2012–', '2012').replace('20152019', '2015-2019')
            title = '[B][COLOR white]'+convert_charactere(name, 'utf-8')+' - '+year+'[/COLOR]'+' [COLOR yellow] (Imdb '+imdb_votes+')[/COLOR][/B]'
            addDir(title.encode('utf-8', 'ignore'),url.encode('utf-8'),2,'',thumbnail.encode('utf-8'),'','','','',True,True)
    xbmcplugin.setContent(addon_handle, 'movies')
    SetView('Wall')
    xbmcplugin.endOfDirectory(addon_handle)




def exibir_temporadas(url,iconimage,fanart):
    data = getRequest(url, '')
    seasonRE = re.compile("<li.+?class='has-sub'><a.+?href='#'><span>.+?</b> (.+?)</span></a>", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    episodesRE = re.compile('<li>.+?<a href="(.+?)".+?target.+?<span class="datex">.+?- (.+?)</span>.+?<span class="datix"><b class="icon-chevron-right"></b>(.+?)</span>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    SynopsisRE_1 = re.compile('<div.+?class="dataplus">.+?<h2>Synopsis</h2>.+?style="text-align: justify;">(.+?)</p>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    SynopsisRE_2 = re.compile('<div.+?class="dataplus">.+?<h2>Synopsis</h2>.+?<p>.+?</p>.+?<p>(.+?)</p>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)    
    SynopsisRE_3 = re.compile('<div.+?class="dataplus">.+?<h2>Synopsis</h2>.+?<p>(.+?)</p>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    if SynopsisRE_1 !=[]:
        sinopse = str(SynopsisRE_1[0])
    elif SynopsisRE_2 !=[]:
        sinopse = str(SynopsisRE_2[0])
    elif SynopsisRE_3 !=[]:
        sinopse = str(SynopsisRE_3[0])
    else:
        sinopse = ''
    if episodesRE !=[]:
        list_episodes1 = []
        list_episodes2 = []
        list_episodes3 = []
        list_episodes4 = []
        list_episodes5 = []
        list_episodes6 = []
        list_episodes7 = []
        list_episodes8 = []
        list_episodes9 = []
        list_episodes10 = []
        list_episodes11 = []
        list_episodes12 = []
        list_episodes13 = []
        list_episodes14 = []
        list_episodes15 = []
        list_episodes16 = []
        list_episodes17 = []
        list_episodes18 = []
        list_episodes19 = []
        list_episodes20 = []
        list_episodes21 = []
        list_episodes22 = []
        list_episodes23 = []
        list_episodes24 = []
        list_episodes25 = []
        list_episodes26 = []
        list_episodes27 = []
        list_episodes28 = []
        list_episodes29 = []
        list_episodes30 = []
        list_episodes31 = []
        list_episodes32 = []
        list_episodes33 = []
        list_episodes34 = []
        list_episodes35 = []
        list_episodes36 = []
        list_episodes37 = []
        list_episodes38 = []
        list_episodes39 = []
        list_episodes40 = []
        list_episodes41 = []
        list_episodes42 = []
        list_episodes43 = []
        list_episodes44 = []
        list_episodes45 = []
        list_episodes46 = []
        list_episodes47 = []
        list_episodes48 = []
        for url, number, name in episodesRE:
            if url.find('1x') >=0 and not url.find('10x') >=0 and not url.find('11x') >=0 and not url.find('12x') >=0 and not url.find('13x') >=0 and not url.find('14x') >=0 and not url.find('15x') >=0 and not url.find('16x') >=0 and not url.find('17x') >=0 and not url.find('18x') >=0 and not url.find('19x') >=0 and not url.find('21x') >=0 and not url.find('31x') >=0 and not url.find('41x') >=0 and not url.find('51x') >=0 and not url.find('61x') >=0 and not url.find('71x') >=0:                
                list_episodes1.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('2x') >=0 and not url.find('12x') >=0 and not url.find('20x') >=0 and not url.find('21x') >=0 and not url.find('22x') >=0 and not url.find('23x') >=0 and not url.find('24x') >=0 and not url.find('25x') >=0 and not url.find('26x') >=0 and not url.find('27x') >=0 and not url.find('28x') >=0 and not url.find('29x') >=0 and not url.find('32x') >=0 and not url.find('42x') >=0 and not url.find('52x') >=0 and not url.find('62x') >=0 and not url.find('72x') >=0:                
                list_episodes2.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('3x') >=0 and not url.find('13x') >=0 and not url.find('23x') >=0 and not url.find('30x') >=0 and not url.find('31x') >=0 and not url.find('32x') >=0 and not url.find('33x') >=0 and not url.find('34x') >=0 and not url.find('35x') >=0 and not url.find('36x') >=0 and not url.find('37x') >=0 and not url.find('38x') >=0 and not url.find('39x') >=0 and not url.find('43x') >=0 and not url.find('53x') >=0 and not url.find('63x') >=0 and not url.find('73x') >=0:                
                list_episodes3.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('4x') >=0 and not url.find('14x') >=0 and not url.find('24x') >=0 and not url.find('34x') >=0 and not url.find('40x') >=0 and not url.find('41x') >=0 and not url.find('42x') >=0 and not url.find('43x') >=0 and not url.find('44x') >=0 and not url.find('45x') >=0 and not url.find('46x') >=0 and not url.find('47x') >=0 and not url.find('48x') >=0 and not url.find('49x') >=0 and not url.find('54x') >=0 and not url.find('64x') >=0 and not url.find('74x') >=0:                
                list_episodes4.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('5x') >=0 and not url.find('15x') >=0 and not url.find('25x') >=0 and not url.find('35x') >=0 and not url.find('45x') >=0 and not url.find('50x') >=0 and not url.find('51x') >=0 and not url.find('52x') >=0 and not url.find('53x') >=0 and not url.find('54x') >=0 and not url.find('55x') >=0 and not url.find('56x') >=0 and not url.find('57x') >=0 and not url.find('58x') >=0 and not url.find('59x') >=0 and not url.find('65x') >=0 and not url.find('75x') >=0:                
                list_episodes5.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('6x') >=0 and not url.find('16x') >=0 and not url.find('26x') >=0 and not url.find('36x') >=0 and not url.find('46x') >=0 and not url.find('56x') >=0 and not url.find('60x') >=0 and not url.find('61x') >=0 and not url.find('62x') >=0 and not url.find('63x') >=0 and not url.find('64x') >=0 and not url.find('65x') >=0 and not url.find('66x') >=0 and not url.find('67x') >=0 and not url.find('68x') >=0 and not url.find('69x') >=0 and not url.find('76x') >=0:                
                list_episodes6.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('7x') >=0 and not url.find('17x') >=0 and not url.find('27x') >=0 and not url.find('37x') >=0 and not url.find('47x') >=0 and not url.find('57x') >=0 and not url.find('67x') >=0 and not url.find('70x') >=0 and not url.find('71x') >=0 and not url.find('72x') >=0 and not url.find('73x') >=0 and not url.find('74x') >=0 and not url.find('75x') >=0 and not url.find('76x') >=0 and not url.find('77x') >=0 and not url.find('78x') >=0 and not url.find('79x') >=0:                
                list_episodes7.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('8x') >=0 and not url.find('18x') >=0 and not url.find('28x') >=0 and not url.find('38x') >=0 and not url.find('48x') >=0 and not url.find('58x') >=0 and not url.find('68x') >=0 and not url.find('78x') >=0 and not url.find('80x') >=0 and not url.find('81x') >=0 and not url.find('82x') >=0 and not url.find('83x') >=0 and not url.find('84x') >=0 and not url.find('85x') >=0 and not url.find('86x') >=0 and not url.find('87x') >=0 and not url.find('88x') >=0:                
                list_episodes8.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('9x') >=0 and not url.find('19x') >=0 and not url.find('29x') >=0 and not url.find('39x') >=0 and not url.find('49x') >=0 and not url.find('59x') >=0 and not url.find('69x') >=0 and not url.find('79x') >=0 and not url.find('89x') >=0 and not url.find('90x') >=0 and not url.find('91x') >=0 and not url.find('92x') >=0 and not url.find('93x') >=0 and not url.find('94x') >=0 and not url.find('95x') >=0 and not url.find('96x') >=0 and not url.find('97x') >=0:                
                list_episodes9.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('10x') >=0:
                list_episodes10.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('11x') >=0:
                list_episodes11.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('12x') >=0:
                list_episodes12.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('13x') >=0:
                list_episodes13.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('14x') >=0:
                list_episodes14.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('15x') >=0:
                list_episodes15.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('16x') >=0:
                list_episodes16.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('17x') >=0:
                list_episodes17.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('18x') >=0:
                list_episodes18.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('19x') >=0:
                list_episodes19.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('20x') >=0:
                list_episodes20.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('21x') >=0:
                list_episodes21.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('22x') >=0:
                list_episodes22.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('23x') >=0:
                list_episodes23.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('24x') >=0:
                list_episodes24.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('25x') >=0:
                list_episodes25.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('26x') >=0:
                list_episodes26.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('27x') >=0:
                list_episodes27.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('28x') >=0:
                list_episodes28.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('29x') >=0:
                list_episodes29.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('30x') >=0:
                list_episodes30.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('31x') >=0:
                list_episodes31.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('32x') >=0:
                list_episodes32.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('33x') >=0:
                list_episodes33.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('34x') >=0:
                list_episodes34.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('35x') >=0:
                list_episodes35.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('36x') >=0:
                list_episodes36.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('37x') >=0:
                list_episodes37.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('38x') >=0:
                list_episodes38.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('39x') >=0:
                list_episodes39.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('40x') >=0:
                list_episodes40.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('41x') >=0:
                list_episodes41.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('42x') >=0:
                list_episodes42.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('43x') >=0:
                list_episodes43.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('44x') >=0:
                list_episodes44.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('45x') >=0:
                list_episodes45.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('46x') >=0:
                list_episodes46.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('47x') >=0:
                list_episodes47.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
            elif url.find('48x') >=0:
                list_episodes48.append(('episode_name#'+convert_charactere(number+' -'+name, 'ascii')+'#episode_url#'+url+'#'))
    if seasonRE !=[] and episodesRE !=[]:
        for season in seasonRE:
            if season.find('1') >=0 and not season.find('10') >=0 and not season.find('11') >=0 and not season.find('12') >=0 and not season.find('13') >=0 and not season.find('14') >=0 and not season.find('15') >=0 and not season.find('16') >=0 and not season.find('17') >=0 and not season.find('18') >=0 and not season.find('19') >=0 and not season.find('21') >=0 and not season.find('31') >=0 and not season.find('41') >=0 and not season.find('51') >=0 and not season.find('61') >=0 and not season.find('71') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes1))
            elif season.find('2') >=0 and not season.find('12') >=0 and not season.find('20') >=0 and not season.find('21') >=0 and not season.find('22') >=0 and not season.find('23') >=0 and not season.find('24') >=0 and not season.find('25') >=0 and not season.find('26') >=0 and not season.find('27') >=0 and not season.find('28') >=0 and not season.find('29') >=0 and not season.find('32') >=0 and not season.find('42') >=0 and not season.find('52') >=0 and not season.find('62') >=0 and not season.find('72') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes2))
            elif season.find('3') >=0 and not season.find('13') >=0 and not season.find('23') >=0 and not season.find('30') >=0 and not season.find('31') >=0 and not season.find('32') >=0 and not season.find('33') >=0 and not season.find('34') >=0 and not season.find('35') >=0 and not season.find('37') >=0 and not season.find('38') >=0 and not season.find('39') >=0 and not season.find('43') >=0 and not season.find('53') >=0 and not season.find('63') >=0 and not season.find('73') >=0 and not season.find('83') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes3))
            elif season.find('4') >=0 and not season.find('14') >=0 and not season.find('24') >=0 and not season.find('34') >=0 and not season.find('40') >=0 and not season.find('41') >=0 and not season.find('42') >=0 and not season.find('43') >=0 and not season.find('44') >=0 and not season.find('45') >=0 and not season.find('46') >=0 and not season.find('47') >=0 and not season.find('48') >=0 and not season.find('49') >=0 and not season.find('54') >=0 and not season.find('64') >=0 and not season.find('74') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes4))
            elif season.find('5') >=0 and not season.find('15') >=0 and not season.find('25') >=0 and not season.find('35') >=0 and not season.find('45') >=0 and not season.find('50') >=0 and not season.find('51') >=0 and not season.find('52') >=0 and not season.find('53') >=0 and not season.find('54') >=0 and not season.find('55') >=0 and not season.find('56') >=0 and not season.find('57') >=0 and not season.find('58') >=0 and not season.find('59') >=0 and not season.find('65') >=0 and not season.find('75') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes5))
            elif season.find('6') >=0 and not season.find('16') >=0 and not season.find('26') >=0 and not season.find('36') >=0 and not season.find('46') >=0 and not season.find('56') >=0 and not season.find('60') >=0 and not season.find('61') >=0 and not season.find('62') >=0 and not season.find('63') >=0 and not season.find('64') >=0 and not season.find('65') >=0 and not season.find('66') >=0 and not season.find('67') >=0 and not season.find('68') >=0 and not season.find('69') >=0 and not season.find('76') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes6))
            elif season.find('7') >=0 and not season.find('17') >=0 and not season.find('27') >=0 and not season.find('37') >=0 and not season.find('47') >=0 and not season.find('57') >=0 and not season.find('67') >=0 and not season.find('70') >=0 and not season.find('71') >=0 and not season.find('72') >=0 and not season.find('73') >=0 and not season.find('74') >=0 and not season.find('75') >=0 and not season.find('76') >=0 and not season.find('77') >=0 and not season.find('78') >=0 and not season.find('79') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes7))
            elif season.find('8') >=0 and not season.find('18') >=0 and not season.find('28') >=0 and not season.find('38') >=0 and not season.find('48') >=0 and not season.find('58') >=0 and not season.find('68') >=0 and not season.find('78') >=0 and not season.find('80') >=0 and not season.find('81') >=0 and not season.find('82') >=0 and not season.find('83') >=0 and not season.find('84') >=0 and not season.find('85') >=0 and not season.find('86') >=0 and not season.find('87') >=0 and not season.find('88') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes8))
            elif season.find('9') >=0 and not season.find('19') >=0 and not season.find('29') >=0 and not season.find('39') >=0 and not season.find('49') >=0 and not season.find('59') >=0 and not season.find('69') >=0 and not season.find('79') >=0 and not season.find('89') >=0 and not season.find('90') >=0 and not season.find('91') >=0 and not season.find('92') >=0 and not season.find('93') >=0 and not season.find('94') >=0 and not season.find('95') >=0 and not season.find('96') >=0 and not season.find('97') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes9))
            elif season.find('10') >=0 and not season.find('100') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes10))
            elif season.find('11') >=0 and not season.find('111') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes11))
            elif season.find('12') >=0 and not season.find('112') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes12))
            elif season.find('13') >=0 and not season.find('113') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes13))
            elif season.find('14') >=0 and not season.find('114') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes14))
            elif season.find('15') >=0 and not season.find('115') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes15))
            elif season.find('16') >=0 and not season.find('116') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes16))
            elif season.find('17') >=0 and not season.find('117') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes17))
            elif season.find('18') >=0 and not season.find('118') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes18))
            elif season.find('19') >=0 and not season.find('119') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes19))
            elif season.find('20') >=0 and not season.find('119') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes20))
            elif season.find('21') >=0 and not season.find('121') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes21))
            elif season.find('22') >=0 and not season.find('122') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes22))
            elif season.find('23') >=0 and not season.find('123') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes23))
            elif season.find('24') >=0 and not season.find('124') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes24))
            elif season.find('25') >=0 and not season.find('125') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes25))
            elif season.find('26') >=0 and not season.find('126') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes26))
            elif season.find('27') >=0 and not season.find('127') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes27))
            elif season.find('28') >=0 and not season.find('128') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes28))
            elif season.find('29') >=0 and not season.find('129') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes29))
            elif season.find('30') >=0 and not season.find('130') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes30))
            elif season.find('31') >=0 and not season.find('131') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes31))
            elif season.find('32') >=0 and not season.find('132') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes32))
            elif season.find('33') >=0 and not season.find('133') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes33))
            elif season.find('34') >=0 and not season.find('134') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes34))
            elif season.find('35') >=0 and not season.find('135') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes35))
            elif season.find('36') >=0 and not season.find('136') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes36))
            elif season.find('37') >=0 and not season.find('137') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes37))
            elif season.find('38') >=0 and not season.find('138') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes38))
            elif season.find('39') >=0 and not season.find('139') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes39))
            elif season.find('40') >=0 and not season.find('140') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes40))
            elif season.find('41') >=0 and not season.find('141') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes41))
            elif season.find('42') >=0 and not season.find('142') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes42))
            elif season.find('43') >=0 and not season.find('143') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes43))
            elif season.find('44') >=0 and not season.find('144') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes44))
            elif season.find('45') >=0 and not season.find('145') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes45))
            elif season.find('46') >=0 and not season.find('146') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes46))
            elif season.find('47') >=0 and not season.find('147') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes47))
            elif season.find('48') >=0 and not season.find('148') >=0:
                season_resolve = "[B][COLOR white]"+season+"[/COLOR][/B]"
                addDir(season_resolve.encode('utf-8', 'ignore'),'',3,'',iconimage.encode('utf-8'),'',fix_Synopsis(sinopse).encode('utf-8'),'',str(list_episodes48))
    else:
        exibir_idioma(url,iconimage,fix_Synopsis(sinopse).encode('utf-8'),data)
    xbmcplugin.setContent(addon_handle, 'movies')
    SetView('InfoWall')
    xbmcplugin.endOfDirectory(addon_handle)
    

def exibir_idioma(url,iconimage,description,data=False):
    if data:
        infoRE = re.compile('<div.+?class="datos.+?episodio">.+?<h1>(.+?)</h1>.+?<p><span>(.+?)</span>.+?<span>(.+?)</span>.+?<a.+?href.+?>(.+?)</a>.+?</p>(.+?)</div>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        info2RE = re.compile('<div.+?class="dataplus">.+?<h1>(.+?)</h1>.+?<div.+?id="dato-1".+?<p>.+?<span.+?<span>.+?<a.+?href.+?rel="tag">(.+?)</a>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        info_img_extra = re.compile('meta.+?property="og:image".+?content="(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        info_synopsis_extra = re.compile('div.+?id="dato-2".+?<h2>Synopsis</h2>.+?<p>(.+?)</p>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if infoRE !=[]:
            try:
                title_info = convert_charactere(str(infoRE[0][0]), 'utf-8')
                season_info = str(infoRE[0][1])
                episode_info = str(infoRE[0][2])
                tvshow_info = str(infoRE[0][3])
                Synopsis_info = fix_Synopsis(str(infoRE[0][4]))
                title_legendado = '[B][COLOR white]'+tvshow_info+' - '+season_info+episode_info+' - '+title_info+' - Legendado[/COLOR][/B]'
                title_dublado = '[B][COLOR white]'+tvshow_info+' - '+season_info+episode_info+' - '+title_info+' - Dublado[/COLOR][/B]'
                desc_info = Synopsis_info
            except:
                title_legendado = '[B][COLOR white]Legendado[/COLOR][/B]'
                title_dublado = '[B][COLOR white]Dublado[/COLOR][/B]'
                if description == '' or description == None:
                    try:
                        if info_synopsis_extra !=[]:
                            desc_info = fix_Synopsis(str(info_synopsis_extra[0]))
                        else:
                            desc_info = ''
                    except:
                        desc_info = ''
                else:
                    try:
                        desc_info = description
                    except:
                        desc_info = ''
        elif info2RE !=[]:
            try:
                title_info = convert_charactere(str(info2RE[0][0]), 'utf-8')
                year1 = str(info2RE[0][1])
                year = year1.replace(' -','').replace('- ', '').replace('2020–', '2020').replace('2015–', '2015').replace('2016–', '2016').replace('1989–', '1989').replace('2013–', '2013').replace('2014–', '2014').replace('2010–', '2010').replace('1997–', '1997').replace('20142015', '2014-2015').replace('2011–', '2011').replace('2012–', '2012').replace('20152019', '2015-2019')
                title_legendado = '[B][COLOR white]'+title_info+' - '+year+' - Legendado[/COLOR][/B]'
                title_dublado = '[B][COLOR white]'+title_info+' - '+year+' - Dublado[/COLOR][/B]'
                if description == '' or description == None:
                    try:
                        if info_synopsis_extra !=[]:
                            desc_info = fix_Synopsis(str(info_synopsis_extra[0]))
                        else:
                            desc_info = ''
                    except:
                        desc_info = ''
                else:
                    try:
                        desc_info = description
                    except:
                        desc_info = ''
            except:
                title_legendado = '[B][COLOR white]Legendado[/COLOR][/B]'
                title_dublado = '[B][COLOR white]Dublado[/COLOR][/B]'
                if description == '' or description == None:
                    try:
                        if info_synopsis_extra !=[]:
                            desc_info = fix_Synopsis(str(info_synopsis_extra[0]))
                        else:
                            desc_info = ''
                    except:
                        desc_info = ''
                else:
                    try:
                        desc_info = description
                    except:
                        desc_info = ''       
        else:
            title_legendado = '[B][COLOR white]Legendado[/COLOR][/B]'
            title_dublado = '[B][COLOR white]Dublado[/COLOR][/B]'
            if description == '' or description == None:
                try:
                    if info_synopsis_extra !=[]:
                        desc_info = fix_Synopsis(str(info_synopsis_extra[0]))
                    else:
                        desc_info = ''
                except:
                    desc_info = ''
            else:
                try:
                    desc_info = description
                except:
                    desc_info = ''
        if iconimage > '' and not iconimage.find(icon_menu) >=0:
            thumb = iconimage
        else:
            try:
                if info_img_extra !=[]:
                    thumb = str(info_img_extra[0])
                else:
                    thumb = ''
            except:
                thumb = ''
        idiomaRE_id = re.compile('<iframe.+?src="(.+?)".+?</iframe>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if idiomaRE_id !=[]:
            for url_idioma in idiomaRE_id:
                if re.search("Dub",url_idioma,re.IGNORECASE):
                    addDir(title_dublado.replace("&amp;","&").replace("&#039;","'").encode('utf-8', 'ignore'),url_idioma,5,'',thumb.encode('utf-8'),'',desc_info.encode('utf-8'),'','',False)
                elif re.search("Leg",url_idioma,re.IGNORECASE) and not int(url_idioma.count("LEG")) > 1 and not int(url_idioma.count("leg")) > 1:
                    addDir(title_legendado.replace("&amp;","&").replace("&#039;","'").encode('utf-8', 'ignore'),url_idioma,5,'',thumb.encode('utf-8'),'',desc_info.encode('utf-8'),'','',False)
                elif re.search("Leg",url_idioma,re.IGNORECASE) and not re.search("Dub",url_idioma,re.IGNORECASE):
                    addDir(title_legendado.replace("&amp;","&").replace("&#039;","'").encode('utf-8', 'ignore'),url_idioma,5,'',thumb.encode('utf-8'),'',desc_info.encode('utf-8'),'','',False)
                else:
                    addDir(title_dublado.replace("&amp;","&").replace("&#39;","'").encode('utf-8', 'ignore'),url_idioma,5,'',thumb.encode('utf-8'),'',desc_info.encode('utf-8'),'','',False)
    elif url > '':
        data = getRequest(url, '')
        infoRE = re.compile('<div.+?class="datos.+?episodio">.+?<h1>(.+?)</h1>.+?<p><span>(.+?)</span>.+?<span>(.+?)</span>.+?<a.+?href.+?>(.+?)</a>.+?</p>(.+?)</div>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        info2RE = re.compile('<div.+?class="dataplus">.+?<h1>(.+?)</h1>.+?<div.+?id="dato-1".+?<p>.+?<span.+?<span>.+?<a.+?href.+?rel="tag">(.+?)</a>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        info_img_extra = re.compile('meta.+?property="og:image".+?content="(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        info_synopsis_extra = re.compile('div.+?id="dato-2".+?<h2>Synopsis</h2>.+?<p>(.+?)</p>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if infoRE !=[]:
            try:
                title_info = convert_charactere(str(infoRE[0][0]), 'utf-8')
                season_info = str(infoRE[0][1])
                episode_info = str(infoRE[0][2])
                tvshow_info = str(infoRE[0][3])
                Synopsis_info = fix_Synopsis(str(infoRE[0][4]))
                title_legendado = '[B][COLOR white]'+tvshow_info+' - '+season_info+episode_info+' - '+title_info+' - Legendado[/COLOR][/B]'
                title_dublado = '[B][COLOR white]'+tvshow_info+' - '+season_info+episode_info+' - '+title_info+' - Dublado[/COLOR][/B]'
                desc_info = Synopsis_info
            except:
                title_legendado = '[B][COLOR white]Legendado[/COLOR][/B]'
                title_dublado = '[B][COLOR white]Dublado[/COLOR][/B]'
                if description == '' or description == None:
                    try:
                        if info_synopsis_extra !=[]:
                            desc_info = fix_Synopsis(str(info_synopsis_extra[0]))
                        else:
                            desc_info = ''
                    except:
                        desc_info = ''
                else:
                    try:
                        desc_info = description
                    except:
                        desc_info = ''
        elif info2RE !=[]:
            try:
                title_info = convert_charactere(str(info2RE[0][0]), 'utf-8')
                year1 = str(info2RE[0][1])
                year = year1.replace(' -','').replace('- ', '').replace('2020–', '2020').replace('2015–', '2015').replace('2016–', '2016').replace('1989–', '1989').replace('2013–', '2013').replace('2014–', '2014').replace('2010–', '2010').replace('1997–', '1997').replace('20142015', '2014-2015').replace('2011–', '2011').replace('2012–', '2012').replace('20152019', '2015-2019')
                title_legendado = '[B][COLOR white]'+title_info+' - '+year+' - Legendado[/COLOR][/B]'
                title_dublado = '[B][COLOR white]'+title_info+' - '+year+' - Dublado[/COLOR][/B]'
                if description == '' or description == None:
                    try:
                        if info_synopsis_extra !=[]:
                            desc_info = fix_Synopsis(str(info_synopsis_extra[0]))
                        else:
                            desc_info = ''
                    except:
                        desc_info = ''
                else:
                    try:
                        desc_info = description
                    except:
                        desc_info = ''
            except:
                title_legendado = '[B][COLOR white]Legendado[/COLOR][/B]'
                title_dublado = '[B][COLOR white]Dublado[/COLOR][/B]'
                if description == '' or description == None:
                    try:
                        if info_synopsis_extra !=[]:
                            desc_info = fix_Synopsis(str(info_synopsis_extra[0]))
                        else:
                            desc_info = ''
                    except:
                        desc_info = ''
                else:
                    try:
                        desc_info = description
                    except:
                        desc_info = ''       
        else:
            title_legendado = '[B][COLOR white]Legendado[/COLOR][/B]'
            title_dublado = '[B][COLOR white]Dublado[/COLOR][/B]'
            if description == '' or description == None:
                try:
                    if info_synopsis_extra !=[]:
                        desc_info = fix_Synopsis(str(info_synopsis_extra[0]))
                    else:
                        desc_info = ''
                except:
                    desc_info = ''
            else:
                try:
                    desc_info = description
                except:
                    desc_info = ''
        if iconimage > '' and not iconimage.find(icon_menu) >=0:
            thumb = iconimage
        else:
            try:
                if info_img_extra !=[]:
                    thumb = str(info_img_extra[0])
                else:
                    thumb = ''
            except:
                thumb = ''
        idiomaRE_id = re.compile('<iframe.+?src="(.+?)".+?</iframe>', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if idiomaRE_id !=[]:
            for url_idioma in idiomaRE_id:
                if re.search("Dub",url_idioma,re.IGNORECASE):
                    addDir(title_dublado.replace("&amp;","&").replace("&#039;","'").encode('utf-8', 'ignore'),url_idioma,5,'',thumb.encode('utf-8'),'',desc_info.encode('utf-8'),'','',False)
                elif re.search("Leg",url_idioma,re.IGNORECASE) and not int(url_idioma.count("LEG")) > 1 and not int(url_idioma.count("leg")) > 1:
                    addDir(title_legendado.replace("&amp;","&").replace("&#039;","'").encode('utf-8', 'ignore'),url_idioma,5,'',thumb.encode('utf-8'),'',desc_info.encode('utf-8'),'','',False)
                elif re.search("Leg",url_idioma,re.IGNORECASE) and not re.search("Dub",url_idioma,re.IGNORECASE):
                    addDir(title_legendado.replace("&amp;","&").replace("&#039;","'").encode('utf-8', 'ignore'),url_idioma,5,'',thumb.encode('utf-8'),'',desc_info.encode('utf-8'),'','',False)
                else:
                    addDir(title_dublado.replace("&amp;","&").replace("&#039;","'").encode('utf-8', 'ignore'),url_idioma,5,'',thumb.encode('utf-8'),'',desc_info.encode('utf-8'),'','',False)
    else:
        xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Falha ao obter os dados!')
        


def exibir_episodios(episodes,iconimage,description):
    list_episodes = re.compile('episode_name#([\s\S]*?)#episode_url#([\s\S]*?)#', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(episodes)
    if list_episodes !=[]:
        for name, url in list_episodes:
            name_resolve = '[B][COLOR white]'+convert_charactere(name, 'utf-8')+'[/COLOR][/B]'
            addDir(name_resolve.encode('utf-8', 'ignore'),url.encode('utf-8'),4,'',iconimage.encode('utf-8'),'',description.encode('utf-8'),'','')
    xbmcplugin.setContent(addon_handle, 'movies')
    SetView('InfoWall')
    xbmcplugin.endOfDirectory(addon_handle)


def urlresolve(url,LOG=False):
    data = getRequest(url, '')
    if LOG:
        try:
            f = open(xbmc.translatePath(home+'/LOG-URLRESOLVE.txt'),'w')
            f.write(data)
            f.close()
        except:
            pass
    page_select = re.compile('iframe.+?src="(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    page1 = re.compile("location.href='(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    page2 = re.compile('<div.+?class="itens">.+?<a.+?href.+?=".+?data=(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
    if page_select !=[]:
        for url_iframe in page_select:
            if url_iframe.find('selec') >= 0:
                data_iframe = getRequest(url_iframe, '')
                data_iframe_RE = re.compile('data=(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data_iframe)
                if data_iframe_RE !=[]:
                    try:
                        player = data_iframe_RE[0]
                        resolved = urlresolve(player)
                    except:
                        resolved = ''
                else:
                    resolved = ''
            elif url_iframe.find('camp') >= 0:
                data_iframe = getRequest(url_iframe, '')
                data_iframe_RE = re.compile('data=(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data_iframe)
                if data_iframe_RE !=[]:
                    try:
                        player = data_iframe_RE[0]
                        resolved = urlresolve(player)
                    except:
                        resolved = ''
                else:
                    resolved = ''            
            else:
                data_iframe = getRequest(url_iframe, '')
                data_iframe_RE = re.compile('data=(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data_iframe)
                if data_iframe_RE !=[]:
                    try:
                        player = data_iframe_RE[0]
                        resolved = urlresolve(player)
                    except:
                        resolved = ''
                else:
                    resolved = ''       
    elif page1 !=[]:
        for player_url in page1:
            if player_url.find('desktop') >= 0:
                page2 = getRequest(player_url, '')
                video_url_RE = re.compile("file':'(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(page2)
                if video_url_RE !=[]:
                    for video_url in video_url_RE:
                        if video_url.find('-ALTO') >= 0:
                            resolved = video_url
                        else:
                            resolved = ''
                else:
                    resolved = ''
            else:
                try:
                    resolved = urlresolve(page1[0])
                except:
                    resolved = ''
    elif page2 !=[]:
        try:
            player = page2[0]
            data = getRequest(player, '')
            video_url_RE = re.compile('file:.+?"(.+?)"', re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
            if video_url_RE !=[]:
                    for video_url in video_url_RE:
                        if video_url.find('-ALTO') >= 0:
                            resolved = video_url
                        else:
                            resolved = ''
            else:
                resolved = ''
        except:
            resolved = '' 
    else:
        video_url_RE = re.compile("file':'(.+?)'", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
        if video_url_RE !=[]:
            for video_url in video_url_RE:
                if video_url.find('-ALTO') >= 0:
                    resolved = video_url
                else:
                    resolved = ''
        else:
            resolved = ''
    return resolved


def srt_browser():
    dialog = xbmcgui.Dialog()
    q = dialog.yesno('Legenda Externa', 'Deseja Adicionar legenda externa antes da reprodução?')
    if int(q)==1:
        try:
            file_srt = dialog.browseSingle(1, 'Selecione uma legenda srt', 'files', '', False, False)
        except:
            file_srt = ''
    else:
        file_srt = ''  
    return file_srt


def getFavorites():
    try:
        try:
            items = json.loads(open(favorites).read())
        except:
            items = ''
        total = len(items)
        if int(total) > 0:
            for i in items:
                name = i[0]
                url = i[1]
                mode = i[2]
                subtitle = i[3]
                iconimage = i[4]
                fanArt = i[5]
                description = i[6]
                cat = i[7]
                episodes = i[8]
                
                addDir(name.encode('utf-8', 'ignore'),url.encode('utf-8'),mode,subtitle,iconimage.encode('utf-8'),fanArt.encode('utf-8'),description.encode('utf-8', 'ignore'),cat.encode('utf-8'),episodes.encode('utf-8'),True,True)
            xbmcplugin.setContent(addon_handle, 'movies')
            SetView('Wall')
            xbmcplugin.endOfDirectory(addon_handle)
        else:
            xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Nenhuma Série ou Filme Adicionado em Meus Favoritos')
                
    except:
        xbmcplugin.setContent(addon_handle, 'movies')
        SetView('Wall')
        xbmcplugin.endOfDirectory(addon_handle)
            

def addFavorite(name,url,fav_mode,subtitle,iconimage,fanart,description,cat,episodes):
    favList = []
    try:
        # seems that after
        name = name.encode('utf-8', 'ignore')
    except:
        pass
    if os.path.exists(favorites)==False:
        addonID = xbmcaddon.Addon().getAddonInfo('id')
        addon_data_path = xbmc.translatePath(os.path.join('special://home/userdata/addon_data', addonID))
        if os.path.exists(addon_data_path)==False:
            os.mkdir(addon_data_path)
        xbmc.sleep(7)
        favList.append((name,url,fav_mode,subtitle,iconimage,fanart,description,cat,episodes))
        a = open(favorites, "w")
        a.write(json.dumps(favList))
        a.close()
        notify('Adicionado em Meus Favoritos!',name,iconimage)
        #xbmc.executebuiltin("XBMC.Container.Refresh")
    else:
        a = open(favorites).read()
        data = json.loads(a)
        data.append((name,url,fav_mode,subtitle,iconimage,fanart,description,cat,episodes))
        b = open(favorites, "w")
        b.write(json.dumps(data))
        b.close()
        notify('Adicionado em Meus Favoritos!',name,iconimage)
        #xbmc.executebuiltin("XBMC.Container.Refresh")


def rmFavorite(name):
    data = json.loads(open(favorites).read())
    for index in range(len(data)):
        if data[index][0]==name:
            del data[index]
            b = open(favorites, "w")
            b.write(json.dumps(data))
            b.close()
            break
    notify('Removido dos Meus Favoritos!')
    #xbmc.executebuiltin("XBMC.Container.Refresh")



def play_video(name,url,iconimage,fanart,description,subtitle=False):
    #log = urlresolve(url,True)
    url_resolved = urlresolve(url)
    if url_resolved > '':
        legenda = xbmcaddon.Addon().getSetting("legenda")
        if legenda == 'true':
            file_srt = srt_browser()
        else:
            file_srt = ''
        li = xbmcgui.ListItem(name, path=url_resolved, iconImage=iconimage, thumbnailImage=iconimage)
        li.setInfo(type='video', infoLabels={'Title': name, 'plot': description })
        if subtitle:
            li.setSubtitles([subtitle])
        elif file_srt > '':
            li.setSubtitles([file_srt])
        xbmc.Player().play(item=url_resolved, listitem=li)
    else:
        xbmcgui.Dialog().ok('[B][COLOR white]AVISO[/COLOR][/B]','Não foi possivel reproduzir o video')
    

def addDir(name,url,mode,subtitle,iconimage,fanart,description,cat,episodes,folder=True,favorite=False):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)+"&iconimage="+urllib.quote_plus(iconimage)+"&subtitle="+urllib.quote_plus(subtitle)+"&description="+urllib.quote_plus(description)+"&cat="+urllib.quote_plus(cat)+"&episodes="+urllib.quote_plus(episodes)
    if folder:
        li=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    else:
        li=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    li.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
    if fanart > '':
        li.setProperty('fanart_image', fanart)
    else:
        li.setProperty('fanart_image', home+'/fanart.jpg')
    if favorite:
        try:
            name_fav = json.dumps(name)
        except:
            name_fav =  name
        try:
            contextMenu = []
            if name_fav in FAV:
                try:
                    contextMenu.append(('Remover dos Meus Favoritos','XBMC.RunPlugin(%s?mode=13&name=%s)'%(sys.argv[0], urllib.quote_plus(name))))
                except:
                    contextMenu.append(('Remover dos Meus Favoritos','XBMC.RunPlugin(%s?mode=13&name=%s)'%(sys.argv[0], urllib.quote_plus(name.encode('utf-8', 'ignore')))))
            else:
                try:
                    fav_params = ('%s?mode=12&name=%s&url=%s&subtitle=%s&iconimage=%s&fanart=%s&description=%s&cat=%s&episodes=%s&fav_mode=%s'%(sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url.encode('utf-8')), urllib.quote_plus(subtitle.encode('utf-8')), urllib.quote_plus(iconimage), urllib.quote_plus(fanart), urllib.quote_plus(description), urllib.quote_plus(cat), urllib.quote_plus(episodes), str(mode)))
                except:
                    fav_params = ('%s?mode=12&name=%s&url=%s&subtitle=%s&iconimage=%s&fanart=%s&description=%s&cat=%s&episodes=%s&fav_mode=%s'%(sys.argv[0], urllib.quote_plus(name.encode('utf-8', 'ignore')), urllib.quote_plus(url.encode('utf-8')), urllib.quote_plus(subtitle.encode('utf-8')), urllib.quote_plus(cleaname.encode("utf-8")), urllib.quote_plus(iconimage.encode("utf-8")), urllib.quote_plus(fanart.encode("utf-8")), urllib.quote_plus(description.encode("utf-8")), urllib.quote_plus(cat.encode("utf-8")), urllib.quote_plus(episodes.encode("utf-8")), str(mode)))
                contextMenu.append(('Adicionar a Meus Favoritos','XBMC.RunPlugin(%s)' %fav_params))
            li.addContextMenuItems(contextMenu)
        except:
            pass
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=u, listitem=li, isFolder=folder)



def doacao():
    import xbmc
    import webbrowser
    dialog = xbmcgui.Dialog()
    link = dialog.select('[B][COLOR white]FAÇA UMA DOAÇÃO AO[/COLOR] [COLOR yellow]Flix[/COLOR][COLOR lime]Cine[/COLOR][/B]', ['[COLOR yellow]Flix[/COLOR][COLOR lime]Cine[/COLOR]: DOAÇÃO [COLOR steelblue]MERCADO[/COLOR][COLOR skyblue]PAGO[/COLOR] R$10,00','[COLOR yellow]Flix[/COLOR][COLOR lime]Cine[/COLOR]: DOAÇÃO [COLOR lime]PYCPAY[/COLOR]', '[COLOR yellow]Flix[/COLOR][COLOR lime]Cine[/COLOR]: [B][COLOR white]CONTINUAR NO ADDON[/COLOR][/B]'])
    if link == 0:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://www.mercadopago.com.br' ))
        else:
            webbrowser.open('https://www.mercadopago.com.br')
    if link == 1:
        if xbmc.getCondVisibility('system.platform.android'):
            xbmc.executebuiltin('StartAndroidActivity(,android.intent.action.VIEW,,%s)' %('https://app.picpay.com' ))
        else:
            webbrowser.open('https://app.picpay.com')


def SetView(name):
    if name == 'Wall':
        try:
            xbmc.executebuiltin('Container.SetViewMode(500)')
        except:
            pass
    if name == 'List':
        try:
            xbmc.executebuiltin('Container.SetViewMode(50)')
        except:
            pass
    if name == 'Poster':
        try:
            xbmc.executebuiltin('Container.SetViewMode(51)')
        except:
            pass
    if name == 'Shift':
        try:
            xbmc.executebuiltin('Container.SetViewMode(53)')
        except:
            pass
    if name == 'InfoWall':
        try:
            xbmc.executebuiltin('Container.SetViewMode(54)')
        except:
            pass
    if name == 'WideList':
        try:
            xbmc.executebuiltin('Container.SetViewMode(55)')
        except:
            pass
    if name == 'Fanart':
        try:
            xbmc.executebuiltin('Container.SetViewMode(502)')
        except:
            pass


def contador():
    try:
        request_headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
        "Referer": "FlixCine-10.0.3",
        "Connection": "close",
        }
        request = urllib2.Request("https://whos.amung.us/pingjs/?k=6gjsucgcje", headers=request_headers)
        response = urllib2.urlopen(request).read()
        #tempo_delay = 0
        #xbmc.sleep(tempo_delay*0)
    except:
        pass
contador()


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]

    return param



def main():
    params=get_params()
    url=None
    name=None
    mode=None
    iconimage=None
    fanart=None
    description=None
    subtitle=None
    cat=None
    episodes=None
    pesquisa=None
    fav_mode=None
    page=1

    #xbmcplugin.setContent(addon_handle, 'movies')
    #SetView('List')

    try:
        #url=urllib.unquote(params["url"])
        url=urllib.unquote_plus(params["url"])
    except:
        pass
    try:
        name=urllib.unquote_plus(params["name"])
    except:
        pass
    try:
        iconimage=urllib.unquote_plus(params["iconimage"])
    except:
        pass
    try:
        mode=int(params["mode"])
    except:
        pass
    try:
        fanart=urllib.unquote_plus(params["fanart"])
    except:
        pass
    try:
        description=urllib.unquote_plus(params["description"])
    except:
        pass

    try:
        subtitle=urllib.unquote_plus(params["subtitle"])
    except:
        pass
    try:
        cat=urllib.unquote_plus(params["cat"])
    except:
        pass        
    try:
        episodes=urllib.unquote_plus(params["episodes"])
    except:
        pass
    try:
        pesquisa=urllib.unquote_plus(params["pesquisa"])
    except:
        pass
    try:
        page=int(params["page"])
    except:
        pass
    try:
        fav_mode=int(params["fav_mode"])
    except:
        pass

    if mode==None:
        cat_principal()
        SetView('WideList')
        xbmcplugin.endOfDirectory(addon_handle)
    elif mode==1:
        if pesquisa and pesquisa !=None:
            exibir_pagina(url,page,'',pesquisa)
        else:
            exibir_pagina(url,page,cat)
    elif mode==2:
        exibir_temporadas(url,iconimage,fanart)
    elif mode==3:
        exibir_episodios(episodes,iconimage,description)
    elif mode==4:
        exibir_idioma(url,iconimage,description)
        xbmcplugin.setContent(addon_handle, 'movies')
        SetView('InfoWall')
        xbmcplugin.endOfDirectory(addon_handle)
    elif mode==5:
        play_video(name,url,iconimage,fanart,description,subtitle)
    elif mode==6:
        exibir_recomendados(url)
    elif mode==7:
        pesquisar(url)
    elif mode==8:
        cat_genero()
    elif mode==9:
        cat_outros(url)
    elif mode==10:
        exibir_outros(url,cat,iconimage)
    elif mode==11:
        xbmcaddon.Addon().openSettings()
    elif mode==12:
        try:
            name = name.split('\\ ')[1]
        except:
            pass
        try:
            name = name.split('  - ')[0]
        except:
            pass
        addFavorite(name,url,fav_mode,subtitle,iconimage,fanart,description,cat,episodes)
    elif mode==13:
        try:
            name = name.split('\\ ')[1]
        except:
            pass
        try:
            name = name.split('  - ')[0]
        except:
            pass
        rmFavorite(name)
    elif mode==14:
        getFavorites()
    elif mode==15:
        doacao()


if __name__ == "__main__":
	main()    
