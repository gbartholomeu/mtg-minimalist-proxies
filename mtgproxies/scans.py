from __future__ import annotations

from tqdm import tqdm

import scryfall
from mtgproxies.decklists.decklist import Decklist, Card
from minimalistproxies.proxies import get_minimalist_proxies
from collections import Iterable


def fetch_scans_scryfall(decklist: Decklist) -> list[str]:
    """Search Scryfall for scans of a decklist.

    Args:
        decklist: List of (count, name, set_id, collectors_number)-tuples

    Returns:
        List: List of image files
    """
    return [
        scan for card in tqdm(decklist.cards, desc="Fetching artwork") for image_uri in card.image_uris
        for scan in [scryfall.get_image(image_uri["png"], silent=True)] * card.count
    ]

def flatten(lis):
     for item in lis:
         if isinstance(item, Iterable) and not isinstance(item, str):
             for x in flatten(item):
                 yield x
         else:        
             yield item

def fetch_minimalist_images(decklist: Decklist) -> list[str]:
    """Create a minimalist proxy for each card in the Decklist object.

    Args:
        decklist: List of (count, name, set_id, collectors_number)-tuples

    Returns:
        List: List of image files
    """
    file_paths = []
    for card in tqdm(decklist.cards, desc="Creating minimalist proxies"):
        if card.__contains__('card_faces') and card['layout'].lower() not in ['split', 'flip']:
            file_paths.append([get_minimalist_proxies(Card(card.count, card['card_faces'][0]), Card(card.count, card['card_faces'][1]), card)] * card.count)
            file_paths.append([get_minimalist_proxies(Card(card.count, card['card_faces'][1]), Card(card.count, card['card_faces'][0]), card)] * card.count)
        elif card.__contains__('card_faces') and card['layout'].lower() in ['split', 'flip']:
            file_paths.append([get_minimalist_proxies(Card(card.count, card['card_faces'][0]), Card(card.count, card['card_faces'][1]), card)] * card.count)
        else:
            file_paths.append([get_minimalist_proxies(card)] * card.count)
    return list(flatten(file_paths))