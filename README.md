# opnsense-ipcheck
ipcheck plugin for OPNsense verifies what various APIs on the internet know about public IPv4 and IPv6 address.

## install
```
sudo pkg add https://github.com/mihakralj/opnsense-ipcheck/raw/main/os-ipcheck-devel-0.1_1.txz
```

## remove
`sudo pkg delete os-ipcheck-devel`

## feedback
https://github.com/mihakralj/opnsense-ipcheck/discussions

## Version 0.1
Enabled 9 API services:
### Vpnapi
100 requests per day without an API key. API key increases daily limit of requests from 100 to 1,000. Get a free API key at https://vpnapi.io/signup
### Proxycheck
100 requests per day without an API key. The API key increases daily limit from 100 to 1,000 requests. Get a free API key at https://proxycheck.io/dashboard/
### ip2location
ip2location allows 20 requests per day without an API key. API key grants 5,000 credits (about 300 requests). Get a free API key at https://ip2location.com/register?id=1005
### ip2proxy
ip2proxy allows 50 requests total (not daily, TOTAL) without an API key. API key grants 5,000 credits TOTAL. Get a free API key at https://www.ip2location.com/web-service/ip2proxy
### IpQualityScore
ipqualityscore.com allows 5,000 requsts per month with a free API key. Get a free API key at https://www.ipqualityscore.com/
### IpBlacklist
Allows 1,000 requsts per day with a free API key. Get a free API key at https://ipblacklist.ai/
### Scamalytics
Allows 5,000 requsts per month with a free API key. Get a free API key (and username) at https://scamalytics.com/ip/api/enquiry
### Ipvoid
Allows 25 credits (~310 requests) with a free API key. Get a free API key athttps://www.apivoid.com/api/ip-reputation/
### Onionoo
TOR relay directory API - unlimited requests
