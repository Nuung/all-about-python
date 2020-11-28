BASE_URL = ["https://stackoverflow.com", "https://weworkremotely.com", "https://remoteok.io"]

CRAWLING_URL = ["https://stackoverflow.com/jobs?r=true&q={}", "https://weworkremotely.com/remote-jobs/search?term={}",
                "https://remoteok.io/remote-dev+{}-jobs"]

DEFAULT_ICON = "https://www.flaticon.com/svg/static/icons/svg/1441/1441180.svg"

HEADERS = { 
    'pragma': "no-cache",
    'cache-control': "no-cache",
    'accept': "application/json, text/javascript, */*; q=0.01",
    'x-requested-with': "XMLHttpRequest",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
    'accept-language': "en,ko-KR;q=0.9,ko;q=0.8,en-US;q=0.7"    
} 