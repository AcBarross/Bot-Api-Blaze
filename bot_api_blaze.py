import requests
import telegram
import asyncio
import aiohttp


TOKEN = '5793864346:AAEq4Z6lKXzXumyMw-CxVLMJs8vXOKBB8Mo'

bot = telegram.Bot(TOKEN)

chat_id = '6290068374'

def get_color_name(color_code):
    if color_code == 0:
        return 'Branco'
    elif color_code in range(1, 8):
        return 'Vermelho'
    elif color_code in range(8, 15):
        return 'Preto'
    else:
        return 'Desconhecido'

async def send_message_with_delay(message, delay=40):
    messages = await bot.send_message(chat_id=chat_id, text=message)
    await asyncio.sleep(delay)

async def analyze_results(results):
    colors = [get_color_name(result['color']) for result in results]
    print("Cores:", colors)

    if colors[:3] == ['Preto', 'Preto', 'Preto']:
        await send_message_with_delay('✅ Entrada confirmada, entrar no Vermelho\nBuscar apoio no Branco')

        if colors[3] == 'Vermelho' or colors[3] == 'Branco':
            await send_message_with_delay('✅ GREEN no Vermelho')
        else:
            await send_message_with_delay('✅ Entrar no primeiro Gale')
            if colors[4] == 'Vermelho' or colors[4] == 'Branco':
                await send_message_with_delay('✅ GREEN no Vermelho')
            else:
                await send_message_with_delay('✅ Entrar no segundo Gale')
                if colors[5] == 'Vermelho' or colors[5] == 'Branco':
                    await send_message_with_delay('✅ GREEN no Vermelho')
                else:
                    await send_message_with_delay('✅ LOSS')

    elif colors[:3] == ['Vermelho', 'Vermelho', 'Vermelho']:
        await send_message_with_delay('✅ Entrada confirmada, entrar no Preto\nBuscar apoio no Branco')

        if colors[3] == 'Preto' or colors[3] == 'Branco':
            await send_message_with_delay('✅ GREEN no Preto')
        else:
            await send_message_with_delay('✅ Entrar no primeiro Gale')
            if colors[4] == 'Preto' or colors[4] == 'Branco':
                await send_message_with_delay('✅ GREEN no Preto')
            else:
                await send_message_with_delay('✅ Entrar no segundo Gale')
                if colors[5] == 'Preto' or colors[5] == 'Branco':
                    await send_message_with_delay('✅ GREEN no Preto')
                else:
                    await send_message_with_delay('✅ LOSS')

    # Adicione mais combinações aqui...

async def fetch_data(session, url):
    async with session.get(url, ssl=False) as response:
        return await response.json()

async def main():
    await asyncio.sleep(20)  # Esperar 60 segundos antes de iniciar a análise

    async with aiohttp.ClientSession() as session:
        while True:
            url = 'https://blaze.com/api/roulette_games/recent'
            results = await fetch_data(session, url)
            await analyze_results(results)
            await asyncio.sleep(5)

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
