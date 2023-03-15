# timer | 2023
# by zebra

import base64
import io
import requests
from PIL import Image
from telebot.async_telebot import AsyncTeleBot

async def Req2neuro(url_:str='http://127.0.0.1:7860', prompt:str='test', negative_prompt:str=' ', width:int=512, height:int=512, cfg_scale:float=7.5, model:str='HD-22.ckpt', sampler:str='DPM2', steps:int=25, n_iter:int=1, func=lambda x:x, bot:AsyncTeleBot=AsyncTeleBot, message=None):
        json_settings = {
            'sd_model_checkpoint': model,
        }

        json_payload = {
            'sampler_index': sampler,
            'prompt': prompt,
            'negative_prompt': negative_prompt,
            'steps': steps,
            'width': width,
            'height': height,
            'cfg_scale': cfg_scale,
            'n_iter': n_iter,
            'override_settings': json_settings
        }
        
        response = requests.post(url=f'{url_}/sdapi/v1/txt2img',json=json_payload, timeout=900)
        for n, i in enumerate(response.json()['images']):
            await func(bot, message, Image.open(io.BytesIO(base64.b64decode(i.split(',',1)[0]))))