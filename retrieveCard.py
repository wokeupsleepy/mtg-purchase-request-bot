from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog

bolts = Card.where(name="Lightning Bolt").all()

# NOTE: This demonstrates that we can use wildcard characters to make a search, it doesn't need to be an exact name
uro = Card.where(name="Uro%Titan%").all()

secondStopper="fasdfasdf"