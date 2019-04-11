CHARGER_CHOICES = [
                   ('a', 'Charger Type A'), 
                   ('b', 'Charger Type B'), 
                   ('c', 'Charger Type C')
                  ]

AVAILABLE = 'AVAILABLE'
RESERVED = 'RESERVED'
UNAVAILABLE = 'UNAVAILABLE'
OUT_OF_SERVICE = 'OUT_OF_SERVICE'
COMPLETED = 'COMPLETED'

STATUS_CHOICES  = (
                   (AVAILABLE, 'Available'),
                   (RESERVED, 'Reserved'),
                   (UNAVAILABLE, 'Unavailable'),
                   (OUT_OF_SERVICE, 'Out of Service'),
                   (COMPLETED, 'Completed')
                  )
