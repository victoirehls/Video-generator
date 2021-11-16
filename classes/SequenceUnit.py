class SequenceUnit:

    """Class defining a SequenceUnit caracterised by :
        - an image
        - its associated text  (list of strings)

        exemple: image4 associated to ["Bienvenue à New York", "Le budget est à new york est de 130"]

         """

    def __init__(self, image, textlist):
        self.image = image
        self.textlist = textlist