import requests


def separate_full_name(full_name: str):
    full_name_separated = full_name.strip().split(' ')
    first_name = full_name_separated[0]
    last_name = ' '.join(full_name_separated[1:]) if len(full_name_separated) > 1 else ''
    return first_name, last_name


def get_address_by_cep(cep: str):
    payload = requests.get('http://viacep.com.br/ws/{cep}/json'.format(cep=cep.strip().replace('-', '')))
    try:
        payload.raise_for_status()
    except requests.HTTPError:
        raise requests.HTTPError('Invalid CEP')
    address = payload.json()
    if address.get('erro'):
        raise requests.HTTPError('Invalid CEP')
    return {
        'cep': address.get('cep'),
        'street': address.get('logradouro'),
        'number': '',
        'complement': '',
        'neighborhood': address.get('bairro'),
        'city': address.get('localidade'),
        'state': address.get('uf'),
        'country': 'BR',
    }
