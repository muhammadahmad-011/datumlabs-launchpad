import logging
import os
from datetime import datetime, timezone

import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator
from dotenv import load_dotenv
from requests.exceptions import HTTPError, RequestException
from requests_ratelimiter import LimiterSession
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_random_exponential,
)

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


MAX_CALLS_PER_MINUTE = 30
INITIAL_START_TIME = int(datetime(2026, 1, 1, tzinfo=timezone.utc).timestamp())


def _require_api_key() -> str:
    api_key = os.getenv("COINGECKO_API_KEY_USAGE")
    if not api_key:
        raise ValueError("Missing COINGECKO_API_KEY_USAGE in environment or .env file")
    return api_key


def create_rest_client() -> RESTClient:
    return RESTClient(
        base_url="https://api.coingecko.com/api/v3",
        session=LimiterSession(per_minute=MAX_CALLS_PER_MINUTE),
        paginator=PageNumberPaginator(base_page=1, page_param="page", total_path=None),
        headers={"x-cg-demo-api-key": _require_api_key()},
    )


def is_retryable_error(exception: Exception) -> bool:
    if isinstance(exception, RequestException):
        if isinstance(exception, HTTPError) and exception.response is not None:
            return exception.response.status_code in {429, 500, 502, 503, 504}
        return True
    return False


@retry(
    stop=stop_after_attempt(5),
    wait=wait_random_exponential(min=2, max=60),
    retry=retry_if_exception(is_retryable_error),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)

def fetch(client: RESTClient, endpoint: str, params: dict = None):
    response = client.get(endpoint, params=params)
    response.raise_for_status()

    if not response.text.strip():
        logger.warning("Empty response for %s", endpoint)
        return None

    try:
        return response.json()
    except ValueError:
        logger.warning("Invalid JSON for %s", endpoint)
        return None


def get_history_time_window(last_ts: int) -> tuple[int, int]:
    now_ts = int(datetime.now(timezone.utc).timestamp())
    start_ts = max(last_ts, INITIAL_START_TIME)
    return start_ts, now_ts


def process_chart_data(coin_id: str, data: dict) -> list[dict]:
    if not data or not data.get("prices"):
        return []

    caps = dict(data.get("market_caps", []))
    vols = dict(data.get("total_volumes", []))

    by_date = {}
    for ts_ms, price in data.get("prices", []):
        ts_sec = int(ts_ms / 1000)
        date_str = datetime.fromtimestamp(ts_sec, tz=timezone.utc).strftime("%Y-%m-%d")

        by_date[date_str] = {
            "coin_id": coin_id,
            "date": date_str,
            "date_ts": ts_sec,
            "price_usd": price,
            "market_cap_usd": caps.get(ts_ms),
            "volume_usd": vols.get(ts_ms),
        }

    return list(by_date.values())


@dlt.source
def coingecko_source(top_n_pages: int = 1):
    client = create_rest_client()

    @dlt.resource(
        name="markets",
        primary_key="id",
        write_disposition="merge",
        columns={"roi": {"data_type": "complex", "nullable": True}},
    )
    def markets(vs_currency: str = "usd", per_page: int = 250):
        logger.info("Fetching markets (vs_currency=%s, per_page=%s)", vs_currency, per_page)
        params = {"vs_currency": vs_currency, "per_page": per_page}

        for page_num, page in enumerate(client.paginate("/coins/markets", params=params), start=1):
            for coin in page:
                yield coin
            if top_n_pages and page_num >= top_n_pages:
                break

    @dlt.transformer(data_from=markets,name="history",write_disposition="merge",primary_key=["coin_id", "date"],)
    def history(coin: dict):
        coin_id = coin.get("id")
        if not coin_id:
            return

        state = dlt.current.resource_state().setdefault("last_ts", {})
        last_ts = state.get(coin_id, 0)

        start, end = get_history_time_window(last_ts)
        if start >= end:
            logger.info("NOTHING TO FETCH ALREADY UP-TO-DATE %s ", coin_id)
            return

        logger.info("Fetching for %s starting from %s...", coin_id, start)

        data = fetch(
            client,
            f"/coins/{coin_id}/market_chart/range",
            params={"vs_currency": "usd", "from": start, "to": end},)

        records = process_chart_data(coin_id, data)
        if records:
            state[coin_id] = max(r["date_ts"] for r in records)
            yield records

    return markets, history


pipeline = dlt.pipeline(
    pipeline_name="coingecko_pipeline",
    destination="duckdb",
    dataset_name="coingecko_data",
)

if __name__ == "__main__":
    load_info = pipeline.run(coingecko_source())
    print(load_info)