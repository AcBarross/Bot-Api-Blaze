import requests
import time


def get_color_name(color_code):
    if color_code == 0:
        return 'Branco'
    elif color_code == 1:
        return 'Vermelho'
    elif color_code == 2:
        return 'Preto'
    else:
        return 'Desconhecido'


def update_color_list(colors):
    url = 'https://blaze.com/api/roulette_games/recent'
    initial_length = len(colors)
    print(f'Tamanho inicial da lista: {initial_length}')
    updated = False
    while not updated:
        time.sleep(2)
        response = requests.get(url)
        r = response.json()
        if len(r) > 0:
            for item in r:
                color = get_color_name(item['color'])
                if color != colors[-1]:
                    colors.insert(0,color)
                    updated = True
                    break
    final_length = len(colors)
    print(f'Tamanho final da lista: {final_length}')
    print(f'Lista após a atualização: {colors}')


def send_message(message):
    bot_token = '5793864346:AAEq4Z6lKXzXumyMw-CxVLMJs8vXOKBB8Mo'
    chat_id = '6290068374'
    url_blaze = '🎰 [Blaze](https://blaze.com/pt/games/double)'
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}\n{url_blaze}&parse_mode=Markdown'
    requests.get(url)
    time.sleep(2)


def check_sequence(colors, sequence):
    if len(colors) < len(sequence):
        return False
    return colors[:len(sequence)] == sequence


def process_combination(colors, sequence, expected_color):
    send_message(f'Aposte em: {expected_color}')
    time.sleep(15)  # Aumentado o tempo de espera para receber a cor atualizada
    update_color_list(colors)
    new_color = colors[-1]
    if new_color == expected_color:
        send_message(f'✅ GREEN no {expected_color}')

    elif new_color == 'Branco':
        send_message('✅ GREEN no Branco')

    else:
        send_message('✅ LOSS')


def main():
    colors = []
    while True:
        try:
            url = 'https://blaze.com/api/roulette_games/recent'
            response = requests.get(url)
            r = response.json()

            if len(r) > 0:
                for item in r:
                    color = get_color_name(item['color'])
                    colors.insert(0, color)

                sequence = colors[-3:]

                if check_sequence(sequence, ['Vermelho', 'Vermelho']):
                    if process_combination(colors, sequence, 'Vermelho'):
                        colors = colors[:-3]
                elif check_sequence(sequence, ['Preto', 'Preto']):
                    if process_combination(colors, sequence, 'Preto'):
                        colors = colors[:-3]
                elif check_sequence(sequence, ['Preto', 'Vermelho', 'Preto']):
                    if process_combination(colors, sequence, 'Vermelho'):
                        colors = colors[:-3]
                else:
                    if process_combination(colors, sequence, 'Preto'):
                        colors = colors[:-3]

                update_color_list(colors)

            time.sleep(10)

        except Exception as e:
            print(f"Erro ao obter resultado da API da Blaze: {str(e)}")


if __name__ == '__main__':
    main()
