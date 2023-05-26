import requests
import telegram
import asyncio
import aiohttp


TOKEN = '5793864346:AAEq4Z6lKXzXumyMw-CxVLMJs8vXOKBB8Mo'

bot = telegram.Bot(TOKEN)

chat_id = '6290068374'

color_list = []

def get_color_name(color_code):
    if color_code == 0:
        return 'Branco'
    elif color_code in range(1, 8):
        return 'Vermelho'
    elif color_code in range(8, 15):
        return 'Preto'
    else:
        return 'Desconhecido'

async def send_message_with_delay(message, delay=0):
    await asyncio.sleep(delay)
    await bot.send_message(chat_id=chat_id, text=message)

async def analyze_colors(colors):
    if colors[:3] == ['Preto', 'Preto', 'Preto']:
        await send_message_with_delay('✅ Entrada confirmada, entrar no primeiro Gale')
        if colors[3] == 'Vermelho' or colors[3] == 'Branco':
            await send_message_with_delay('✅ GREEN no Vermelho')
        else:
            await send_message_with_delay('✅ Entrada confirmada, entrar no primeiro Gale')
            if colors[4] == 'Vermelho' or colors[4] == 'Branco':
                await send_message_with_delay('✅ GREEN no Vermelho')
            else:
                await send_message_with_delay('✅ Entrada confirmada, entrar no segundo Gale')
                if colors[5] == 'Vermelho' or colors[5] == 'Branco':
                    await send_message_with_delay('✅ GREEN no Vermelho')
                else:
                    await send_message_with_delay('✅ LOSS')
    elif colors[:3] == ['Vermelho', 'Vermelho', 'Vermelho']:
        if colors[3] == 'Preto' or colors[3] == 'Branco':
            await send_message_with_delay('✅ GREEN no Preto')
        else:
            await send_message_with_delay('✅ Entrada confirmada, entrar no primeiro Gale')
            if colors[4] == 'Preto' or colors[4] == 'Branco':
                await send_message_with_delay('✅ GREEN no Preto')
            else:
                await send_message_with_delay('✅ Entrada confirmada, entrar no segundo Gale')
                if colors[5] == 'Preto' or colors[5] == 'Branco':
                    await send_message_with_delay('✅ GREEN no Preto')
                else:
                    await send_message_with_delay('✅ LOSS')

async def fetch_latest_color():
    url = 'https://blaze.com/api/roulette_games/recent'  # Substitua pela URL correta da API da Blaze

    while True:
        try:
            response = requests.get(url)
            results = response.json()

            if isinstance(results, list):
                colors = []
                for result in results:
                    color = get_color_name(result['color'])
                    colors.append(color)
                    print(colors)

                if len(colors) >= 6:
                    await analyze_colors(colors[-6:])  # Analisar as últimas 6 cores
        except Exception as e:
            print(f"Erro ao obter resultado da API da Blaze: {str(e)}")

        await asyncio.sleep(2)  # Aguardar 2 segundos antes de fazer a próxima requisição

async def main():
    await asyncio.sleep(10)  # Esperar 10 segundos antes de iniciar a análise
    await fetch_latest_color()

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()