from enum import Enum

class OrderStatus(str, Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    IN_DELIVERY = 'in_delivery'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'