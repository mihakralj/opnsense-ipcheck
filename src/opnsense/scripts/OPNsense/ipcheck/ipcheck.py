#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
'''
 * Copyright 2021 Miha Kralj
 *    All rights reserved.
 *
 *    Redistribution and use in source and binary forms, with or without
 *    modification, are permitted provided that the following conditions are met:
 *
 *    1. Redistributions of source code must retain the above copyright notice,
 *       this list of conditions and the following disclaimer.
 *
 *    2. Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *
 *    THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES,
 *    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
 *    AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 *    AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
 *    OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 *    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 *    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 *    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 *    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *    POSSIBILITY OF SUCH DAMAGE.
'''

import requests, json, sys
import xml.dom.minidom
import subprocess
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

config = xml.dom.minidom.parse('/conf/config.xml')
arg=''
if len(sys.argv)>1:
    arg=str(sys.argv[1])

def getconfigelement(path):
    try:
        tree = config
        for node in path.split('/'):
            tree = tree.getElementsByTagName(node)
            if len(tree) == 0: return False
            tree = tree[0]
        return tree.firstChild.nodeValue
    except: return False

def vpnapi():
    key = getconfigelement('OPNsense/ipcheck/vpnapikey')
    apikey= "?key="+key if key else ""
    if ipv4:
        try:
            url = Request("https://vpnapi.io/api/"+ipv4+apikey)
            url.add_header('User-Agent', 'Mozilla/5.0')
            out['ipv4']['vpnapi'] = json.load(urlopen(url, timeout=4))
            out['ipv4']['vpnapi']['apikey'] = key
        except:
            pass
    if ipv6:
        try:
            url = Request("https://vpnapi.io/api/"+ipv6+apikey)
            url.add_header('User-Agent', 'Mozilla/5.0')
            out['ipv6']['vpnapi'] = json.load(urlopen(url, timeout=4))
            out['ipv6']['vpnapi']['apikey'] = key            
        except:
            pass
    return

def proxycheck():
    key = getconfigelement('OPNsense/ipcheck/proxycheckkey')
    apikey= 'key='+key+'&' if key else ""
    if ipv4:
        try:
            url = Request("http://proxycheck.io/v2/"+ipv4+"?"+apikey+"vpn=1&risk=1&port=1&seen=1")
            url.add_header('User-Agent', 'Mozilla/5.0')
            out['ipv4']['proxycheck'] = json.load(urlopen(url, timeout=4))
            out['ipv4']['proxycheck']['apikey'] = key
        except:
            pass
    if ipv6:
        try:
            url = Request("http://proxycheck.io/v2/"+ipv6+"?"+apikey+"vpn=1&risk=1&port=1&seen=1")
            url.add_header('User-Agent', 'Mozilla/5.0')
            out['ipv6']['proxycheck'] = json.load(urlopen(url, timeout=4))
            out['ipv6']['proxycheck']['apikey'] = key            
        except:
            pass
    return    

def ip2loc():
    key = getconfigelement('OPNsense/ipcheck/ip2lockey')
    apikey= key if key else "demo"
    if ipv4:
        try:
            url = Request("https://api.ip2location.com/v2/?ip="+ipv4+"&key="+apikey+"&package=WS24")
            out['ipv4']['ip2location'] = json.load(urlopen(url, timeout=4))
            out['ipv4']['ip2location']['apikey'] = key
        except:
            pass
    if ipv6:
        try:
            pass
            url = Request("https://api.ip2location.com/v2/?ip="+ipv6+"&key="+apikey+"&package=WS24")
            out['ipv6']['ip2location'] = json.load(urlopen(url, timeout=4))
            out['ipv6']['ip2location']['apikey'] = key
        except:
            pass
    return    

def ip2proxy():
    key = getconfigelement('OPNsense/ipcheck/ip2proxykey')
    apikey= key if key else "demo"
    if ipv4:
        try:
            url = Request("https://api.ip2proxy.com/?ip="+ipv4+"&key="+apikey+"&package=PX10")
            out['ipv4']['ip2proxy'] = json.load(urlopen(url, timeout=4))
            out['ipv4']['ip2proxy']['apikey'] = key            
        except:
            pass
    if ipv6:
        try:
            url = Request("https://api.ip2proxy.com/?ip="+ipv6+"&key="+apikey+"&package=PX10")
            out['ipv6']['ip2proxy']  = json.load(urlopen(url, timeout=4))
            out['ipv6']['ip2proxy']['apikey'] = key
        except:
            pass
    return  

def onionoo():
    if ipv4:
        try:
            out['ipv4']['onionoo']={}
            url = Request("https://onionoo.torproject.org/details?limit=4&search="+ipv4)
            ret = json.load(urlopen(url, timeout=4))
            if len(ret['relays']): out['ipv4']['onionoo']['relay'] = (ret['relays'][0])
            if len(ret['bridges']): out['ipv4']['onionoo']['bridge'] = (ret['relays'][0])
        except:
            pass
    if ipv6:
        try:
            out['ipv6']['onionoo']={}
            url = Request("https://onionoo.torproject.org/details?limit=4&search="+ipv6)
            ret = json.load(urlopen(url, timeout=4))
            if len(ret['relays']): out['ipv6']['onionoo']['relay'] = (ret['relays'][0])
            if len(ret['bridges']): out['ipv6']['onionoo']['bridge'] = (ret['relays'][0])
        except:
            pass
    return

def ipqs():
    key = getconfigelement('OPNsense/ipcheck/ipqskey')
    apikey= key if key else "false"
    if ipv4:
        try:
            url = Request("https://ipqualityscore.com/api/json/ip/"+apikey+"/"+ipv4+"?strictness=0")
            url.add_header('User-Agent', 'Mozilla/5.0')
            out['ipv4']['ipqs'] = json.load(urlopen(url, timeout=4))
            out['ipv4']['ipqs']['apikey'] = key
        except:
            pass
    if ipv6:
        try:
            url = Request("https://ipqualityscore.com/api/json/ip/"+apikey+"/"+ipv6+"?strictness=0")
            url.add_header('User-Agent', 'Mozilla/5.0')
            out['ipv6']['ipqs'] = json.load(urlopen(url, timeout=4))
            out['ipv6']['ipqs']['apikey'] = key
        except:
            pass
    return

def ipbl():
    key = getconfigelement('OPNsense/ipcheck/ipblkey')
    apikey= key if key else "false"
    if ipv4:
        try:
            url = Request("https://api.ipblacklist.ai/checkIP")
            data = str(json.dumps({'apikey':apikey, 'ip':ipv4})).encode('utf-8')
            out["ipv4"]['ipbl'] = json.load(urlopen(url, data=data, timeout=4))
            out['ipv4']['ipbl']['apikey'] = key
        except:
            pass
    if ipv6:
        try:
            url = Request("https://api.ipblacklist.ai/checkIP")
            data = str(json.dumps({'apikey':apikey, 'ip':ipv6})).encode('utf-8')
            out["ipv6"]['ipbl'] = json.load(urlopen(url, data=data, timeout=4))
            out['ipv6']['ipbl']['apikey'] = key
        except:
            pass
    return

def scam():
    key = getconfigelement('OPNsense/ipcheck/scamalyticskey')
    apikey= key if key else "false"
    name = getconfigelement('OPNsense/ipcheck/scamalyticsname')
    apiname= name if name else "false"
    if ipv4:
        try:
            url = Request("https://api11.scamalytics.com/"+apiname+"/?ip="+ipv4+"&key="+apikey+"&test=1")
            out["ipv4"]['scamalytics'] = json.load(urlopen(url, timeout=4))
        except:
            out['ipv4']['scamalytics']={}
        out['ipv4']['scamalytics']['apiusername'] = name
        out['ipv4']['scamalytics']['apikey'] = key
    if ipv6:
        try:
            url = Request("https://api11.scamalytics.com/"+apiname+"/?ip="+ipv6+"&key="+apikey+"&test=1")
            out["ipv6"]['scamalytics'] = json.load(urlopen(url, timeout=4))
        except:
            out['ipv6']['scamalytics']={}
        out['ipv6']['scamalytics']['apiusername'] = name
        out['ipv6']['scamalytics']['apikey'] = key
    return

def ipvoid():
    key = getconfigelement('OPNsense/ipcheck/ipvoidkey')
    apikey= "key="+key+"&ip=" if key else "ip="
    if ipv4:
        try:
            #print("https://endpoint.apivoid.com/iprep/v1/pay-as-you-go/?"+apikey+ipv4)
            url = Request("https://endpoint.apivoid.com/iprep/v1/pay-as-you-go/?"+apikey+ipv4)
            url.add_header('User-Agent', 'Mozilla/5.0')
            out["ipv4"]['ipvoid'] = json.load(urlopen(url, timeout=4))
        except:
            out['ipv4']['ipvoid']={}
        out['ipv4']['ipvoid']['apikey'] = key
    if ipv6:
        try:
            url = Request("https://endpoint.apivoid.com/iprep/v1/pay-as-you-go/?"+apikey+ipv6)
            url.add_header('User-Agent', 'Mozilla/5.0')
            out["ipv6"]['ipvoid'] = json.load(urlopen(url, timeout=4))
            out["ipv6"]['ipvoid']['message'] = 'IPv6 not supported by ipvoid'
        except:
            out['ipv6']['ipvoid']={}
        out['ipv6']['ipvoid']['apikey'] = key
    return

# Main stuff
out={}
ivpnapi = getconfigelement('OPNsense/ipcheck/vpnapi')
iproxycheck = getconfigelement('OPNsense/ipcheck/proxycheck')
iip2proxy = getconfigelement('OPNsense/ipcheck/ip2proxy')
iip2loc = getconfigelement('OPNsense/ipcheck/ip2loc')
iipqs = getconfigelement('OPNsense/ipcheck/ipqs')
iipbl = getconfigelement('OPNsense/ipcheck/ipbl')
iscamalytics = getconfigelement('OPNsense/ipcheck/scamalytics')
iipvoid = getconfigelement('OPNsense/ipcheck/ipvoid')
ionionoo = getconfigelement('OPNsense/ipcheck/onionoo')

if arg == '':
    out['vpnapi'] = ivpnapi
    out['proxycheck'] = iproxycheck
    out['ip2proxy'] = iip2proxy
    out['ip2loc'] = iip2loc
    out['ipqs'] = iipqs
    out['ipbl'] = iipbl
    out['scamalytics'] = iscamalytics
    out['ipvoid'] = iipvoid
    out['onionoo'] = ionionoo
    print(json.dumps(out, indent=3))
    exit()
    
try:
    out['ipv4'] = {}
    ipv4 = json.load(urlopen("https://ip4.seeip.org/json", timeout=2))['ip']
except URLError as error:
    ipv4 = False
out['ipv4']['ip'] = ipv4

try:
    ipv6 = json.load(urlopen("https://ip6.seeip.org/json", timeout=2))['ip']
    out['ipv6'] = {}
    out['ipv6']['ip'] = ipv6
except URLError as error:
    ipv6 = False

if arg == 'all':
    if ivpnapi =='1': vpnapi()
    if iproxycheck =='1': proxycheck()
    if iip2proxy =='1': ip2proxy()
    if iip2loc =='1': ip2loc()
    if ionionoo == '1': onionoo()
    if iipqs == '1': ipqs()
    if iipbl == '1': ipbl()
    if iscamalytics == '1': scam()
    if iipvoid == '1': ipvoid()

elif arg == 'vpnapi': vpnapi()
elif arg == 'proxycheck': proxycheck()
elif arg == 'ip2proxy': ip2proxy()
elif arg == 'ip2loc': ip2loc()
elif arg == 'onionoo': onionoo()
elif arg == 'ipqs': ipqs()
elif arg == 'ipbl': ipbl()
elif arg == 'scamalytics': scam()
elif arg == 'ipvoid': ipvoid()

print(json.dumps(out, indent=3))