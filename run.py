from undetected_playwright.sync_api import sync_playwright, Playwright
from playwright_stealth import stealth_sync
import requests
import time

def run(playwright: Playwright, address):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=True)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    }

    context = browser.new_context(
        user_agent=user_agent,
        viewport={"width": 1920, "height": 1080},
        locale="en-US",
        timezone_id="America/Los_Angeles",
        java_script_enabled=True,
        extra_http_headers=headers,
    )
    page = context.new_page()
    
    stealth_sync(page)
    page.goto(f"https://www.google.com/search?q={address}+realtor")
    first_link_element = page.query_selector("h3")
    first_link_url = first_link_element.evaluate("el => el.parentElement.href")
    building_id= first_link_url[-11:]
    if "realtor" in first_link_url:
        print(f"First link URL: {first_link_url}")
        building_id = building_id.replace("-", "")
        print(building_id)
        browser.close()
    else:
        page.goto(f"https://www.google.com/search?q={address}+zillow")
        first_snippet_element = page.query_selector("div[data-sncf='1,2']")  # Google's description div
        first_snippet_text = first_snippet_element.inner_text() if first_snippet_element else "Snippet not found"
        print(f"First zillow? URL: {first_link_url}")
        print(f"First snippet: {first_snippet_text}")
        browser.close()
        return

    #send the request if realtor link is found
    cookies = {
    'split': 'n',
    'split_tcv': '166',
    '__vst': '7669faf4-fcc6-4efc-a6a6-ed85801a757b',
    '__ssn': '790803eb-a0b9-45ed-bdde-948ce48851f4',
    '__ssnstarttime': '1726687380',
    '__bot': 'false',
    'isAuth0EnabledOnGnav': 'C1',
    '_lr_retry_request': 'true',
    '_lr_env_src_ats': 'false',
    'G_ENABLED_IDPS': 'google',
    '__split': '12',
    'AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg': '1',
    'mdLogger': 'false',
    'kampyle_userid': '8d7b-08cd-0777-42ca-a07b-90ca-ae95-6890',
    'kampyleUserSession': '1726687382993',
    'kampyleUserSessionsCount': '1',
    'kampyleSessionPageCounter': '1',
    '_lr_geo_location_state': 'CA',
    '_lr_geo_location': 'US',
    'criteria': 'city%3DPorter%2520Ranch%26state_id%3DCA%26zip%3D91326%26neighborhood%3D',
    'srchID': 'f3a28f5b96414250a409d6138958927d',
    'AMCV_8853394255142B6A0A4C98A4%40AdobeOrg': '-1124106680%7CMCIDTS%7C19985%7CMCMID%7C70893633824382597689144772522562046633%7CMCAID%7CNONE%7CMCOPTOUT-1726694598s%7CNONE%7CvVersion%7C5.2.0',
    }

    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    # 'cookie': 'split=n; split_tcv=166; __vst=7669faf4-fcc6-4efc-a6a6-ed85801a757b; __ssn=790803eb-a0b9-45ed-bdde-948ce48851f4; __ssnstarttime=1726687380; __bot=false; isAuth0EnabledOnGnav=C1; _lr_retry_request=true; _lr_env_src_ats=false; G_ENABLED_IDPS=google; __split=12; AMCVS_8853394255142B6A0A4C98A4%40AdobeOrg=1; mdLogger=false; kampyle_userid=8d7b-08cd-0777-42ca-a07b-90ca-ae95-6890; kampyleUserSession=1726687382993; kampyleUserSessionsCount=1; kampyleSessionPageCounter=1; _lr_geo_location_state=CA; _lr_geo_location=US; criteria=city%3DPorter%2520Ranch%26state_id%3DCA%26zip%3D91326%26neighborhood%3D; srchID=f3a28f5b96414250a409d6138958927d; AMCV_8853394255142B6A0A4C98A4%40AdobeOrg=-1124106680%7CMCIDTS%7C19985%7CMCMID%7C70893633824382597689144772522562046633%7CMCAID%7CNONE%7CMCOPTOUT-1726694598s%7CNONE%7CvVersion%7C5.2.0',
    'origin': 'https://www.realtor.com',
    'priority': 'u=1, i',
    'rdc-client-name': 'RDC_WEB_DETAILS_PAGE',
    'rdc-client-version': '2.0.1324',
    'referer': 'https://www.realtor.com/realestateandhomes-detail/M2225896423',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'x-rdc-visitor-id': '7669faf4-fcc6-4efc-a6a6-ed85801a757b',
    }

    json_data = {
    'operationName': 'SpotOfferEvaluation',
    'variables': {
        'propertyId': '',
        'requestOrigin': 'pdp_spot_offer',
        'partners': [
            'homeward',
            'offerpad',
        ],
    },
    'query': 'query SpotOfferEvaluation($propertyId: ID!, $requestOrigin: String!, $partners: [String]) {\n  spot_offer_evaluation(property_id: $propertyId) {\n    property_id\n    spot_offer(request_origin: $requestOrigin, partners: $partners) {\n      component_type\n      cta_url\n      evaluation {\n        is_qualified\n        provider_id\n        product_id\n        partner_logo\n        offer {\n          value\n          __typename\n        }\n        __typename\n      }\n      property_details {\n        status\n        description {\n          property_type\n          beds\n          baths_full\n          baths_half\n          sqft\n          lot_sqft\n          year_built\n          __typename\n        }\n        address {\n          line\n          city\n          state_code\n          postal_code\n          __typename\n        }\n        last_sold_price\n        last_sold_date\n        home_estimate {\n          value\n          source\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}',
    }
    json_data['variables']['propertyId'] = building_id
    response = requests.post('https://www.realtor.com/frontdoor/graphql', cookies=cookies, headers=headers, json=json_data)
    data=response.json()
    sqft = data['data']['spot_offer_evaluation']['spot_offer']['property_details']['description']['sqft']
    return sqft