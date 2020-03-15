from wordcloud_fa import WordCloudFa
from telethon import TelegramClient
import numpy as np
from PIL import Image
import config


api_id = config.api_id
api_hash = config.api_hash
phone = config.phone
my_username = config.my_username
client = TelegramClient(my_username, api_id, api_hash)


def create_word_cloud():
    """ create the cloud of word with wordcloud_fa module"""
    # mask.jpg is a image in black and white picture that word will write in that
    mask_array = np.array(Image.open("mask.jpg"))
    wc = WordCloudFa(persian_normalize=True, include_numbers=False, mask=mask_array, background_color="white",
                     collocations=False)
    with open('telegramtxt.txt', 'r') as file:
        text = file.read()
    frequencies = wc.process_text(text)
    avr = 0
    count = 0
    frequencies = {k: v for k, v in frequencies.items() if v > 1}
    for k, v in frequencies.items():
        count += 1
        avr += v
    avr = avr // count
    print(f'avr of word count : {avr}')
    frequencies = {k: v for k, v in frequencies.items() if v > avr}
    frequencies = {k: v for k, v in sorted(frequencies.items(), key=lambda item: item[1], reverse=True)}
    word_cloud = wc.generate_from_frequencies(frequencies)
    image = word_cloud.to_image()
    image.save('cloud.png')

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except:
            await client.sign_in(password=input('Password: '))
    end_username = config.end_username
    msgs = client.iter_messages(end_username)
    with open('telegramtxt.txt', 'w') as file:
        message = """"""
        async for msg in msgs:
            try:
                message += str(msg.message) + '\n'
            except:
                pass
        file.write(message)

if __name__ == '__main__':
    try:
        with open('telegramtxt.txt','r') as file:
            if len(file.readlines()) > 1:
                create_word_cloud()
            else:
                raise FileNotFoundError
    except FileNotFoundError:
        with client:
            client.loop.run_until_complete(main())

