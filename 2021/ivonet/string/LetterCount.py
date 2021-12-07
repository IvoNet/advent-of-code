import string


class LetterCounter(object):
    """
    Maak een tekst waarin één letter precies 1x voorkomt, een andere letter
    precies 2x voorkomt, weer een andere letter precies 3x voorkomt, etc. Voorbeeld:

                                    KAAS IS SAAI

    Met vier verschillende letters: 1 x K, 2 x I, 3 x S en 4 x A.
    Iedere inzending met minimaal zes verschillende letters krijgt de volledige
    punten.
    """

    def __init__(self, txt):
        self.count_letters(txt.upper())

    def count_letters(self, txt: str):
        # Count all letters
        letter_count = list()
        alphabet = string.ascii_uppercase
        for letter in alphabet:
            letter_count.append((letter, txt.count(letter)))

        # Remove letters that do not occur
        letter_count = [x for x in letter_count if x[1] > 0]
        self.print_letter_count(letter_count)

    def print_letter_count(self, letter_count_list: list):
        # Sort on occurrence
        sorted_letter_count_list = sorted(letter_count_list, key=lambda k: k[1])
        remaining_letters = ''
        for i, letter_count in enumerate(sorted_letter_count_list):
            letter, count = letter_count
            missing_count = i + 1 - count
            warning = ''
            if missing_count < 0:
                warning = '!!'
            # print('{:>2} - {}:{:>2} - {}{}'.format(i + 1, letter, count, missing_count, warning))
            print('{}:{:>2}'.format(letter, count))
            remaining_letters += letter * missing_count
        print(remaining_letters)


if __name__ == '__main__':
    msg = 'how much wood would a woodchuck chuck if a woodchuck would chuck wood'
    msg = 'via aivd van vandaag vangt vinnig'  # Werkt
    msg = 'lange slangen slagen in slageieren leggen'  # Werkt
    msg = 'de langste slang ligt niet graag lang in glas, maar gaat liever in aanvalsstelling liggen'
    msg = 'toen de krasse stoker stoer stond te kotsen, stonk het helaas naar koeienstront'
    msg = 'de heer in het verkeer is vaak een vrouw, maar het verkeer in de vrouw is vaak een heer'
    msg = 'in vuur en vlam staan begint met naar kaarsen staren. kaarsen vatten vlam als het kan'
    msg = 'het is zonde met je gezin in de zon te zitten zonder je zonen die nooit in de zon zitten'
    msg = 'ik stortte in toen ik me stootte'
    msg = 'de politie die liep, slipte en stopte op de stoep'
    msg = 'ik kan niet strikt naar kraaien en kanaries kijken'
    msg = 'hakken: ik ken het, maar kan het niet'
    msg = 'andersdenkenden denken anders dan ik: kaas'  # Werkt
    msg = 'tuin uitbreiden en truien breien in een uur'  # Werkt
    msg = 'wie nooit iets weet, weet niet dat hij niets weet'
    msg = 'kaas is saai, suiker is stukken saaier'
    msg = 'toen de torens instortten, stortte ik ook in'
    msg = 'kleine kinderen knikkerden erin'  # Werkt
    msg = 'toen de drankstoker stinkend stond te kotsen het stonk naar koeienstront'
    msg = 'dieren voelen onvrede over vroeger'
    msg = 'via de vinnige aivd vang ik vandaag'
    msg = 'ik ving vanavond vinnig aan'
    msg = 'de aivd vangt vanavond aan'
    msg = 'de grootte in de getto groeit gortig groot'
    msg = 'meesters in amsterdam eten smarties'
    msg = 'ik zoek zotte konijnen die in een konijnenkooi zitten'  # Werkt

    LetterCounter(msg)
