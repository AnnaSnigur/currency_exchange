CURR_USD, CURR_EUR = range(1, 3)

CURRENCY_CHOICES = (
    (CURR_USD, 'USD'),
    (CURR_EUR, 'EUR'),
)

SR_PRIVAT, SR_MONO, SR_VKURSE, SR_NBU, = range(1, 5)

SOURCE_CHOICES = (
    (SR_PRIVAT, 'privat'),
    (SR_MONO, 'mono'),
    (SR_VKURSE, 'vkurse'),
    (SR_NBU, 'nbu'),
)