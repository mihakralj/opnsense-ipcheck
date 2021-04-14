{#
This file is Copyright © 2021 by Miha Kralj
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1.  Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

2.  Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

#}
Active APIs:<br/>
<span id="checkvpnapi" class="label">Vpnapi</span> 
<span id="checkproxy" class="label">Proxycheck</span>
<span id="checkip2loc" class="label">ip2location</span> 
<span id="checkip2proxy" class="label">ip2proxy</span> 
<span id="checkipqs" class="label">IpQualityScore</span> 
<span id="checkipbl" class="label">IpBlacklist</span> 
<span id="checkscamalytics" class="label">Scamalytics</span> 
<span id="checkipvoid" class="label">Ipvoid</span> 
<span id="checkonionoo" class="label">Onionoo</span> 

<br/><br/>

<button class="btn btn-primary" id="runAct" type="button">
    <b>{{ lang._('call APIs') }}</b> <i id="runAct_progress"></i></button>


<table id="ipcheck_widget_table" class="table table-striped table-condensed">
    <tr>
        <th width=25%> </th>
        <th id="ipv4hdr"></th>
        <th id="ipv6hdr"></th>
    </tr>
    <tr>
        <td>Public IP address:</td>
        <td id="ipv4address"></td>
        <td id="ipv6address"></td>
    </tr>
    <tr>
        <td>json dump:</td>
        <td id="ipv4json"></td>
        <td id="ipv6json"></td>
    </tr>
  </table>


<script>
    $(document).ready(function() {
        ajaxCall(url = "/api/ipcheck/run/list", {}, function(chck, status) {
            $('#checkvpnapi').addClass((chck.vpnapi==true)?'label-success':'label')
            $('#checkproxy').addClass((chck.proxycheck==true)?"label-success":"label")
            $('#checkip2loc').addClass((chck.ip2loc==true)?"label-success":"label")
            $('#checkip2proxy').addClass((chck.ip2proxy==true)?"label-success":"label") 
            $('#checkipqs').addClass((chck.ipqs==true)?"label-success":"label")
            $('#checkipbl').addClass((chck.ipbl==true)?"label-success":"label")
            $('#checkscamalytics').addClass((chck.scamalytics==true)?"label-success":"label")
            $('#checkipvoid').addClass((chck.ipvoid==true)?"label-success":"label")
            $('#checkonionoo').addClass((chck.onionoo==true)?"label-success":"label")
        });
    });

    $(function() {
        $("#runAct").click(function() {
            $("#runAct_progress").addClass("fa fa-spinner fa-pulse");
            ajaxCall(url = "/api/ipcheck/run/all", {}, function(r, status) {
                $("#runAct_progress").removeClass("fa fa-spinner fa-pulse");

                if(r.ipv4.ip) {
                    $('#ipv4hdr').text("IPv4");
                    $('#ipv4address').text(r.ipv4.ip);
                    $('#ipv4json').html("<small><pre>"+JSON.stringify(r.ipv4, null, 4)+"</pre></small>");
                }                
                if(r.ipv6.ip) {
                    $('#ipv6hdr').text("IPv6");
                    $('#ipv6address').text(r.ipv6.ip);
                    $('#ipv6json').html("<pre>"+JSON.stringify(r.ipv6, null, 4)+"</pre>");  
                }
            });
        });
    });
</script>