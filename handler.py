from datetime import datetime
from src.apis import Binance, Telegram
from src.db import Mongo, PriceNowRepository, Statistics24hRepository

binance = Binance()


def handler(event, context):
    try:
        save_trades_24h()
        save_prices_now()
        send_message(f'Execução finalizada com sucesso - {datetime.now().isoformat()}')
        return {'status': 'success'}
    except Exception as ex:
        send_message(f'Execução finalizada com erro: {str(ex)} - {datetime.now().isoformat()}')
        return {'status': 'error', 'message': str(ex)}


def save_trades_24h():
    statistics_24h_repo = Statistics24hRepository(Mongo('trades', 'statistics_24hr_by_usdt'))
    trades_24h = binance.statistics_24hr_by_usdt()
    statistics_24h_repo.save(trades_24h)


def save_prices_now():
    price_now_repo = PriceNowRepository(Mongo('trades', 'price_now_by_usdt'))
    prices_now = binance.price_now_by_usdt()
    price_now_repo.save(prices_now)


def send_message(message: str):
    telegram = Telegram()
    telegram.send_message(message)
