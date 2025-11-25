import os, time, datetime, json, traceback
import boto3, requests
from card_labo import CardListPageManager


def _load_env():
    target_domain = os.environ["TARGET_DOMAIN"]

    return {
        "TARGET_DOMAIN": target_domain,
        "BUCKET_NAME": os.environ['BUCKET_NAME'],
        "AWS_REGION": 'ap-northeast-1',
    }

def lambda_handler(event, context):
    try:
        cfg = _load_env()
        now_dt = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=9))
        )
        target_uris = event["target_uris"]
        if isinstance(event, str):
            target_uris = json.loads(event["target_uris"])
        records = []
        for uri in target_uris:
            html = fetch(f'{cfg["TARGET_DOMAIN"]}{uri}')
            records.extend(
                parse_cards(html, cfg["TARGET_DOMAIN"])
            )
            if not html: 
                continue
            # スクレイピングのクールタイム（取り除かないこと！！）
            time.sleep(1)

        if records:
            import csv, io
            buf = io.StringIO()
            writer = csv.DictWriter(buf, fieldnames=sorted(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)
            key = f'cardlabo/card_type=ws/dt={now_dt.strftime("%Y-%m-%d-%H-%M")}/data.csv'
            boto3.client("s3").put_object(Bucket=cfg["BUCKET_NAME"], Key=key, Body=buf.getvalue().encode("utf-8"))
    except Exception as e:
        print("ERROR:", repr(e))
        traceback.print_exc()
    return {"count": len(records)}

def fetch(url, headers, tries=3):
    for i in range(tries):
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.text
        if r.status_code in (403, 429, 503):
            time.sleep(2*(i+1))
            continue
        break
    raise Exception(f'FetchError URL:{url}, RecentStatusCode:{r.status_code}')

def parse_cards(html, domain):
    items = []
    card_list_pages = CardListPageManager(domain).fetch_card_list_pages(html)
    for card_list_page in card_list_pages:
        for card_element in card_list_page.card_elements():
            items.append({
                'card_id': card_element.card_id,
                'card_name': card_element.card_name,
                'price': card_element.price,
                'rarity': card_element.rarity,
                'card_detail_page_url': card_element.card_detail_page_url,
            })
    return items

