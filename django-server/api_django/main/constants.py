CHARGER_A = 'a'
CHARGER_B = 'b'
CHARGER_C = 'c'

CHARGER_CHOICES = [
                   (CHARGER_A, 'Charger Type A'), 
                   (CHARGER_B, 'Charger Type B'), 
                   (CHARGER_C, 'Charger Type C')
                  ]

AVAILABLE = 'AVAILABLE'
RESERVED = 'RESERVED'
UNAVAILABLE = 'UNAVAILABLE'
OUT_OF_SERVICE = 'OUT_OF_SERVICE'
CANCELED = 'CANCELED'
COMPLETED = 'COMPLETED'

STATUS_CHOICES  = (
                   (AVAILABLE, 'Available'),
                   (RESERVED, 'Reserved'),
                   (UNAVAILABLE, 'Unavailable'),
                   (OUT_OF_SERVICE, 'Out of Service'),
                   (CANCELED, 'Canceled'),
                   (COMPLETED, 'Completed')
                  )
