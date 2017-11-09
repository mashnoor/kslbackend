import requests

ps = "b2e64b4e_1f28e889d104"
link = "https://portal.kslbd.net/_chief/server/controller/regloginpostgresql.ashx?ps=" + ps
link2 = "https://portal.kslbd.net/_chief/server/controller/ReportExecute.ashx?ps=" + ps
link3 = "https://portal.kslbd.net/account/portfolio/statement.aspx"

link5 = "https://portal.kslbd.net/market/cse/"
'''
ksl portal
User Id- reza49
paswrd- 14789632
'''
loginid = "forhad82"
loginpassword = "123456"
cliendid = "H7882"
params = {
    'param': '[{"id":"login_id","title":"login_id","type":22,"length":0,"precesion":0,"rules":"required; datatype=userid","value":"' + loginid + '","parameterName":"_login_id","parameterDirection":1},{"id":"password","title":"password","type":22,"length":0,"precesion":0,"rules":"required;","value":"' + loginpassword + '","parameterName":"_password","parameterDirection":1},{"id":"ret_type","title":"ret_type","type":22,"length":0,"precesion":0,"rules":"","value":"login","parameterName":"_ret_type","parameterDirection":3},{"id":"ret_val","title":"","type":1,"length":0,"precesion":0,"rules":"required","value":null,"format":"","errors":[],"ignoreValidation":false,"hasError":false,"parameterName":"_ret_val","parameterDirection":2},{"id":"ret_msg","title":"","type":22,"length":0,"precesion":0,"rules":"","value":null,"format":"","errors":[],"ignoreValidation":false,"hasError":false,"parameterName":"_ret_msg","parameterDirection":2}]',
    'sqlCommand': 'portal.login__authenticate', 'sqlCommandType': '4', 'security': '767938178'}
s = requests.session()
r = s.post(link, data=params)
# print(r.cookies)

ck = {}
cks_name = []
cks_ck = []

for c in r.cookies:
    cks_name.append(c.name)

    cks_ck.append(c.value)

ck[cks_name[0]] = cks_ck[0]

ck[cks_name[1]] = cks_ck[1]

r = s.post(link3)

for c in r.cookies:
    cks_name.append(c.name)
    cks_ck.append(c.value)

ck[cks_name[2]] = cks_ck[2]
r = s.post(link5)
print(ck)

req_headers = {}
req_headers['origin'] = 'https://portal.kslbd.net'
req_headers['encoding'] = 'gzip, deflate, br'
req_headers['x-requested-with'] = 'XMLHttpRequest'
req_headers['accept-language'] = 'en-US,en;q=0.8,bn;q=0.6'
req_headers['x-powered-by'] = 'https://www.chieferp.com'
req_headers[
    'user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
req_headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
req_headers['accept'] = 'application/json, text/javascript, */*; q=0.01'
req_headers['referer'] = 'https://portal.kslbd.net/account/portfolio/statement.aspx'
req_headers['authority'] = 'portal.kslbd.net'
req_headers['cookie'] = 'ps=' + ps + '; __cfduid=' + ck['__cfduid'] + '; ASP.NET_SessionId=' + ck[
    'ASP.NET_SessionId'] + '; .ASPXAUTH=' + ck['.ASPXAUTH']

r = s.post(link2, headers=req_headers, data={"portfolio_date": "2017-09-27", "client_id": cliendid, "report_id": "ps"})
print(r.headers)
print(r.content)
'''
curl 'https://portal.kslbd.net/_chief/server/controller/ReportExecute.ashx?ps=a6804846_9751f3fd1630'
-H 'origin: https://portal.kslbd.net'
-H 'accept-encoding: gzip, deflate, br'
-H 'x-requested-with: XMLHttpRequest'
-H 'accept-language: en-US,en;q=0.8,bn;q=0.6'
-H 'x-powered-by: https://www.chieferp.com'
-H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
-H 'content-type: application/x-www-form-urlencoded; charset=UTF-8'
-H 'accept: application/json, text/javascript, */*; q=0.01'
-H 'referer: https://portal.kslbd.net/account/portfolio/statement.aspx'
-H 'authority: portal.kslbd.net'
-H 'cookie: ps=a6804846_9751f3fd1630; __cfduid=d0d9bbe50a7f3c6dd3575f34717ce3c361506496815; ASP.NET_SessionId=ipacz3vcbfxdewbsghkd3jcq; .ASPXAUTH=D7CCF3C67BD459CCC1716026623721F02DC8F5318A5D3CBCF40AE5B6E36171AEE37BD580980E2B1A8D64640DAA27A7BA7DBBFB60E825CAF603AE1A7BD3023FC9D6DE881E36AC3835A573F77757C248A6C95230AC58F5D48F59035BD871C7196E5C323A89502D8B7F950DC83E192F308FBB16B8B2795E99D1D8E00BF83C858D4C927C13D7B7900C26CA025502F5F022CF8F2012D1'
--data 'portfolio_date=2017-09-28&client_id=H7882&report_id=ps'\
       --compressed
'''
