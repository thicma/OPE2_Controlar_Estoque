from PIL import Image

nome = input('nome da imagem buscada: )')

im = None

try:
    im = Image.open(f'{nome}.jpg')
    im.show()
except:
    print('Imagem não encontrada')