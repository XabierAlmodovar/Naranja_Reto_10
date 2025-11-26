class LookieroColors:
    """
    Paleta de colores inspirada en la identidad visual de Lookiero.
    Cada color está definido como un atributo de clase en formato HEX.
    """

    # Colores principales
    PINK = "#EEC7C0"     # Rosa piel / nude característico
    PEACH = "#F4D5CC"    # Melocotón suave
    BLUSH = "#F7E9E5"    # Rosa casi blanco (fondos)

    # Colores secundarios
    TEAL = "#6BA6A9"     # Verde azulado suave
    MINT = "#9ECBCF"     # Menta pastel
    GREY = "#4A4A4A"     # Gris elegante para tipografías

    @classmethod
    def all(cls):
        """
        Devuelve un diccionario con todos los colores definidos.
        """
        return {
            "pink": cls.PINK,
            "peach": cls.PEACH,
            "blush": cls.BLUSH,
            "teal": cls.TEAL,
            "mint": cls.MINT,
            "grey": cls.GREY
        }
